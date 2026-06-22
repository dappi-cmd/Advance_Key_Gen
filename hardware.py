import wmi
import winreg
import platform
import subprocess
import re


class HardwareDetector:
    def __init__(self):
        try:
            self.c = wmi.WMI()
        except Exception:
            self.c = None

    def get_motherboard_serial(self):
        if not self.c:
            return "N/A"
        try:
            for board in self.c.Win32_BaseBoard():
                if board.SerialNumber and board.SerialNumber.strip():
                    return board.SerialNumber.strip()
        except Exception:
            pass
        return "N/A"

    def get_ram_serial(self):
        if not self.c:
            return "N/A"
        try:
            for memory in self.c.Win32_PhysicalMemory():
                if memory.SerialNumber and memory.SerialNumber.strip():
                    return memory.SerialNumber.strip()
        except Exception:
            pass
        return "N/A"

    def get_vga_info(self):
        if not self.c:
            return "N/A"
        try:
            for vga in self.c.Win32_VideoController():
                if vga.PNPDeviceID:
                    return vga.PNPDeviceID.strip()
                if vga.Name:
                    return vga.Name.strip()
        except Exception:
            pass
        return "N/A"

    def get_hdd_serial(self):
        if not self.c:
            return "N/A"
        try:
            for disk in self.c.Win32_DiskDrive():
                if disk.Index == 0:
                    if disk.SerialNumber and disk.SerialNumber.strip():
                        return disk.SerialNumber.strip()
        except Exception:
            pass
        try:
            for disk in self.c.Win32_DiskDrive():
                if disk.SerialNumber and disk.SerialNumber.strip():
                    return disk.SerialNumber.strip()
        except Exception:
            pass
        return "N/A"

    def get_windows_product_key(self):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            )
            product_id = winreg.QueryValueEx(key, "ProductId")[0]
            winreg.CloseKey(key)
            if product_id:
                return product_id.strip()
        except Exception:
            pass
        return "N/A"

    def get_cpu_id(self):
        if not self.c:
            return "N/A"
        try:
            for cpu in self.c.Win32_Processor():
                if cpu.ProcessorId and cpu.ProcessorId.strip():
                    return cpu.ProcessorId.strip()
        except Exception:
            pass
        return "N/A"

    def get_mac_address(self):
        if not self.c:
            return "N/A"
        try:
            for nic in self.c.Win32_NetworkAdapterConfiguration():
                if nic.MACAddress and nic.IPEnabled:
                    return nic.MACAddress.strip()
        except Exception:
            pass
        return "N/A"

    def get_all_info(self):
        info = {
            "motherboard": self.get_motherboard_serial(),
            "ram": self.get_ram_serial(),
            "vga": self.get_vga_info(),
            "hdd": self.get_hdd_serial(),
            "windows_key": self.get_windows_product_key(),
            "cpu": self.get_cpu_id(),
            "mac": self.get_mac_address(),
        }
        return info

    def get_os_info(self):
        if not self.c:
            return platform.platform(), "Unknown"
        try:
            for os_info in self.c.Win32_OperatingSystem():
                return os_info.Caption, os_info.Version
        except Exception:
            pass
        return platform.system(), platform.version()

    def get_system_uptime(self):
        if not self.c:
            return "N/A"
        try:
            for os_info in self.c.Win32_OperatingSystem():
                uptime_seconds = int(os_info.LastBootUpTime.strftime("%s")) if hasattr(os_info.LastBootUpTime, "strftime") else 0
                import datetime
                now = datetime.datetime.now()
                boot = os_info.LastBootUpTime
                if isinstance(boot, datetime.datetime):
                    delta = now - boot
                    days = delta.days
                    hours, remainder = divmod(delta.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    return f"{days}d {hours}h {minutes}m"
        except Exception:
            pass
        return "N/A"
