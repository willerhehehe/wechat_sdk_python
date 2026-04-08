# OpenClaw Weixin 协议梳理

## 1. 登录流程

登录不是浏览器自动化，而是固定的 HTTP CGI：

1. `GET /ilink/bot/get_bot_qrcode?bot_type=3`
   - 返回 `qrcode`
   - 返回 `qrcode_img_content`
2. `GET /ilink/bot/get_qrcode_status?qrcode=...`
   - 长轮询状态
   - 可能返回：
     - `wait`
     - `scaned`
     - `scaned_but_redirect`
     - `expired`
     - `confirmed`
3. `confirmed` 时重点字段：
   - `bot_token`
   - `ilink_bot_id`
   - `baseurl`
   - `ilink_user_id`

`scaned_but_redirect` 说明轮询 host 需要切到 `https://<redirect_host>`。

## 2. 公共请求头

发送消息、收消息、配置读取都带这些头：

- `iLink-App-Id`
- `iLink-App-ClientVersion`
- `AuthorizationType: ilink_bot_token`
- `Authorization: Bearer <bot_token>`
- `X-WECHAT-UIN`

所有 POST JSON body 都带：

```json
{
  "base_info": {
    "channel_version": "2.1.7"
  }
}
```

## 3. 收消息

### 3.1 长轮询

请求：

```json
POST /ilink/bot/getupdates
{
  "get_updates_buf": "<cached_buf>",
  "base_info": {
    "channel_version": "2.1.7"
  }
}
```

响应重点字段：

- `ret`
- `errcode`
- `errmsg`
- `msgs`
- `get_updates_buf`
- `longpolling_timeout_ms`

### 3.2 context_token

每条入站消息可能带 `context_token`。  
回复同一个用户时要把这个 token 原样回传，否则上下文可能不连续。

建议按 `account_id + from_user_id` 保存最近一次 `context_token`。

## 4. 发消息

文本发送：

```json
POST /ilink/bot/sendmessage
{
  "msg": {
    "from_user_id": "",
    "to_user_id": "<user_id@im.wechat>",
    "client_id": "openclaw-weixin:<timestamp>-<hex>",
    "message_type": 2,
    "message_state": 2,
    "item_list": [
      {
        "type": 1,
        "text_item": {
          "text": "hello"
        }
      }
    ],
    "context_token": "<optional>"
  },
  "base_info": {
    "channel_version": "2.1.7"
  }
}
```

常量：

- `message_type=2` 表示 bot
- `message_state=2` 表示 finish
- `item.type=1` 表示文本

## 5. typing

先获取：

```json
POST /ilink/bot/getconfig
{
  "ilink_user_id": "<user_id>",
  "context_token": "<optional>",
  "base_info": {
    "channel_version": "2.1.7"
  }
}
```

返回 `typing_ticket` 后，可继续：

```json
POST /ilink/bot/sendtyping
{
  "ilink_user_id": "<user_id>",
  "typing_ticket": "<ticket>",
  "status": 1,
  "base_info": {
    "channel_version": "2.1.7"
  }
}
```

`status=1` 为 typing，`status=2` 为 cancel。

## 6. 媒体上传

### 6.1 获取上传地址

```json
POST /ilink/bot/getuploadurl
{
  "filekey": "<random hex>",
  "media_type": 1,
  "to_user_id": "<user_id>",
  "rawsize": 123,
  "rawfilemd5": "<md5>",
  "filesize": 128,
  "no_need_thumb": true,
  "aeskey": "<16-byte hex>",
  "base_info": {
    "channel_version": "2.1.7"
  }
}
```

### 6.2 CDN 上传

原文件先做 `AES-128-ECB + PKCS7` 加密，再以 `application/octet-stream` 上传到：

- `upload_full_url`
- 或客户端拼出来的 `/upload?encrypted_query_param=...&filekey=...`

成功后从响应头读取：

- `x-encrypted-param`

这个值回填到消息体里的 `encrypt_query_param`。

## 7. 媒体下载

下载 URL：

- 服务端给了 `full_url` 就直接用
- 否则退回：
  - `/download?encrypted_query_param=...`

下载后按 `aes_key` 解密：

- 可能是 `base64(raw 16 bytes)`
- 也可能是 `base64(hex string of 16 bytes)`

图片入站时还可能在 `image_item.aeskey` 里直接给十六进制 key。
