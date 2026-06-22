import os
#!/usr/bin/env python3
"""
VPN 连接管理

使用方法：
    from vpn_manager import VPNManager
    
    with VPNManager():
        # 在这里调用内网服务
        ...
"""

import subprocess
import time


class VPNManager:
    """VPN 上下文管理器，自动连接和断开"""
    
    def __init__(self, connection_name: str = os.environ.get("VPN_CONNECTION_NAME", ""), timeout: int = 30):
        self.connection_name = connection_name
        self.timeout = timeout
        self._was_connected = False
    
    def is_connected(self) -> bool:
        """检查 VPN 是否已连接"""
        try:
            result = subprocess.run(
                ["sudo", "ipsec", "status", self.connection_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            return "ESTABLISHED" in result.stdout
        except:
            return False
    
    def connect(self) -> bool:
        """连接 VPN"""
        if self.is_connected():
            self._was_connected = True
            return True
        
        try:
            # 启动 ipsec
            subprocess.run(["sudo", "ipsec", "start"], capture_output=True, timeout=10)
            time.sleep(1)
            
            # 连接 VPN
            result = subprocess.run(
                ["sudo", "ipsec", "up", self.connection_name],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if "established successfully" in result.stdout or self.is_connected():
                return True
            return False
        except Exception as e:
            print(f"VPN 连接失败: {e}")
            return False
    
    def disconnect(self) -> bool:
        """断开 VPN"""
        if self._was_connected:
            return True  # 原本就连接着，不断开
        
        try:
            subprocess.run(
                ["sudo", "ipsec", "down", self.connection_name],
                capture_output=True,
                timeout=10
            )
            subprocess.run(["sudo", "ipsec", "stop"], capture_output=True, timeout=10)
            return True
        except:
            return False
    
    def __enter__(self):
        if self.connect():
            print("✓ VPN 已连接")
        else:
            print("⚠ VPN 连接失败")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        print("✓ VPN 已断开")
        return False


def ensure_vpn():
    """装饰器：确保 VPN 连接"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with VPNManager():
                return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    # 测试
    with VPNManager():
        print("VPN 连接中...")
        time.sleep(5)
    print("测试完成")