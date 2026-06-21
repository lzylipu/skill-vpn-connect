---
name: vpn-connect
description: VPN 连接管理。自动检测并连接 VPN 以访问内网服务（唤醒电脑、路由重拨）或访问 Google/GitHub 等服务。触发词：启动vpn、连接vpn、vpn状态、停止vpn。
---

# VPN 连接技能

智能管理 IKEv2 VPN 连接，用于访问内网服务（OpenWrt 路由器、网络唤醒）和国际网络服务。

## 触发词

- 启动vpn / 连接vpn / 开vpn
- 停止vpn / 关vpn / 断开vpn
- vpn状态 / vpn状态检查
- 连接内网 / 访问内网

## 依赖场景

此技能应在以下场景**自动触发**：

1. **网络唤醒** - 唤醒电脑前需要 VPN 连接内网
2. **路由重拨** - 重拨 OpenWrt 路由器需要 VPN
3. **访问 Google/GitHub** - 需要国际线路时

## VPN 配置

- **服务器**: `<server-domain>`
- **类型**: IKEv2 证书认证
- **连接名**: `<vpn-connection-name>`
- **内网范围**: `10.10.0.0/24`

## 使用方法

### 手动控制

```
用户: 启动vpn
助手: 正在连接 VPN...
      ✓ VPN 已连接，内网 IP: 10.10.0.x

用户: vpn状态
助手: VPN 状态: 已连接
      内网 IP: 10.10.0.x
      连接时长: 5 分钟

用户: 停止vpn
助手: ✓ VPN 已断开
```

### 自动触发流程

当执行以下操作时，自动检查并启动 VPN：

1. **wake-pc 技能**:
   ```
   用户: 开电脑
   助手: 检查 VPN 状态... 未连接
         正在启动 VPN... ✓
         正在发送唤醒信号... ✓
         电脑已唤醒
   ```

2. **openwrt-redial 技能**:
   ```
   用户: 路由重拨
   助手: 检查 VPN 状态... 已连接
         正在执行重拨... ✓
   ```

3. **访问 Google/GitHub**:
   - 检测到网络请求失败时自动尝试 VPN

## 技术实现

```bash
# 启动 VPN
sudo ipsec start
sudo ipsec up <vpn-connection-name>

# 检查状态
sudo ipsec status

# 断开 VPN
sudo ipsec down <vpn-connection-name>
sudo ipsec stop
```

## 自动化集成

其他技能应在执行前调用此技能：

```markdown
## 前置检查

1. 调用 `vpn-connect` 检查 VPN 状态
2. 如果目标在内网且 VPN 未连接，自动启动
3. 执行主操作
```

## 状态检查函数

检查 VPN 是否已连接：

```bash
# 返回 0 表示已连接，1 表示未连接
sudo ipsec status <vpn-connection-name> 2>/dev/null | grep -q "ESTABLISHED"
```

## 安全说明

- 需要 sudo 权限（已在 TOOLS.md 中配置 NOPASSWD）
- 证书存储在 `skills/vpn-connect/certs/`
- 仅在需要时启动，节省资源