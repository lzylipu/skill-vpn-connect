# VPN Connect Skill

**[English](./README.md) | [中文](./README.zh-CN.md)**

Smart IKEv2 VPN connection management for accessing LAN services and international network.

## Features

- Auto-detect VPN status before LAN operations
- Auto-connect when needed (wake-pc, redial)
- Manual connect/disconnect/status

## Prerequisites

| Variable | Description |
|----------|-------------|
| VPN_SERVER | VPN server address |
| VPN_CONNECTION_NAME | IKEv2 connection name |
| VPN_NETWORK | LAN network CIDR (e.g. 10.10.0.0/24) |

## Triggers

- 启动vpn / 连接vpn
- 停止vpn
- vpn状态

## License

MIT
