# VPN 连接技能

**[English](./README.md) | [中文](./README.zh-CN.md)**

IKEv2 VPN 智能连接管理，用于访问内网服务和国际网络。

## 功能

- 自动检测 VPN 状态再执行内网操作
- 按需自动连接（唤醒电脑、路由重拨时）
- 手动连接/断开/查看状态

## 前置条件

| 变量 | 说明 |
|------|------|
| VPN_SERVER | VPN 服务器地址 |
| VPN_CONNECTION_NAME | IKEv2 连接名 |
| VPN_NETWORK | 内网 CIDR（如 10.10.0.0/24） |

## 触发词

- 启动vpn / 连接vpn
- 停止vpn
- vpn状态

## License

MIT
