# openclaw-weixin Python 提取版

这是从 `research/openclaw-weixin-plugin` 提取出来的 Python SDK + CLI，目标是把登录、长轮询收消息、文本/媒体发送、媒体下载解密这些核心协议单独跑起来，不依赖 OpenClaw。

## 安装

```bash
python3 -m venv /tmp/weixin-sdk-venv
source /tmp/weixin-sdk-venv/bin/activate
pip install -e .
```

## 快速开始

扫码登录：

```bash
weixin-sdk login
```

持续收消息：

```bash
weixin-sdk poll --account-id <bot_account_id> --forever
```

发送文本：

```bash
weixin-sdk send-text --account-id <bot_account_id> --to <user_id@im.wechat> --text "hello"
```

发送文件：

```bash
weixin-sdk send-file --account-id <bot_account_id> --to <user_id@im.wechat> --path ./demo.pdf
```

## 目录

- `docs/openclaw-weixin-protocol.md`
  - 协议梳理
- `src/weixin_sdk/`
  - SDK 与 CLI 实现
- `tests/`
  - 不依赖真实网络的最小测试

## 默认状态目录

默认保存在 `~/.openclaw-weixin-python`：

- `accounts/`
  - token、base_url、user_id
- `accounts/*.sync.json`
  - `get_updates_buf`
- `accounts/*.context.json`
  - `context_token`
- `login-sessions/`
  - 分步扫码登录会话
