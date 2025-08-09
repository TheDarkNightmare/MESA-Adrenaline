# src/definitions.py

import subprocess

def get_smart_access_memory_status():
    """Check if Smart Access Memory (SAM) is enabled."""
    try:
        result = subprocess.run(["sudo", "dmesg"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "[drm] Detected VRAM RAM=" in line:
                if "BAR=256M" in line:
                    return False
                elif "BAR=" in line and "M" in line:
                    bar_size = int(line.split("BAR=")[1].split("M")[0])
                    if bar_size > 256:
                        return True
    except FileNotFoundError:
        pass
    return False

def get_amdgpu_ppfeaturemask_status():
    """Check if the AMDGPU Performance Override parameter is active."""
    try:
        with open("/proc/cmdline", "r") as cmdline_file:
            cmdline = cmdline_file.read()
            return "amdgpu.ppfeaturemask=0xffffffff" in cmdline
    except FileNotFoundError:
        return False


def get_gpu_name():
    """Get the GPU name from the system."""
    try:
        result = subprocess.run(["lspci"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "VGA compatible controller" in line and "AMD" in line:
                gpu_details = line.split(": ")[-1]
                # Extract the GPU name from the details string
                if "Radeon" in gpu_details:
                    return f"AMD {gpu_details.split('Radeon')[-1].strip()}"
                return gpu_details
    except FileNotFoundError:
        return "Unknown GPU"
    return "Unknown GPU"


def get_gpu_temperature():
    """Get the current GPU temperature."""
    try:
        result = subprocess.run(["sensors"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "edge:" in line:
                return line.split()[1]
    except FileNotFoundError:
        return "N/A"
    return "N/A"


def get_gpu_fan_speed():
    """Get the current GPU fan speed."""
    try:
        result = subprocess.run(["sensors"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "fan" in line and "RPM" in line:
                return line.split()[1] + " RPM"
    except FileNotFoundError:
        return "N/A"
    return "N/A"


def get_cpu_name():
    """Get the CPU name from the system."""
    try:
        with open("/proc/cpuinfo", "r") as cpuinfo_file:
            for line in cpuinfo_file:
                if "model name" in line:
                    return line.split(": ")[-1].strip()
    except FileNotFoundError:
        return "Unknown CPU"
    return "Unknown CPU"





def get_cpu_temperature():
    """Get the current CPU temperature (Tdie or Tctl)."""
    try:
        result = subprocess.run(["sensors"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "Tdie:" in line or "Tctl:" in line:  # Check for Tdie or Tctl
                return line.split()[1].strip("+")  # Example: "+35.8°C" -> "35.8°C"
    except FileNotFoundError:
        return "N/A"
    return "N/A"



def get_cpu_mhz():
    """Get the current CPU frequency in MHz."""
    try:
        result = subprocess.run(["cat", "/proc/cpuinfo"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "MHz" in line:  # Look for lines with "MHz"
                return line.split(":")[1].strip() + " MHz"  # Extract the MHz value
    except FileNotFoundError:
        return "N/A"
    return "N/A"

def get_memory_usage():
    """Get the current RAM usage and return as separate values."""
    try:
        # Read memory information from /proc/meminfo
        with open("/proc/meminfo", "r") as meminfo:
            lines = meminfo.readlines()

        # Extract total and available memory
        mem_total = int([line for line in lines if "MemTotal" in line][0].split()[1])  # in kB
        mem_available = int([line for line in lines if "MemAvailable" in line][0].split()[1])  # in kB

        # Calculate used memory
        mem_used = mem_total - mem_available

        # Convert to MB
        mem_total_mb = mem_total // 1024
        mem_used_mb = mem_used // 1024

        return mem_used_mb, mem_total_mb
    except Exception as e:
        return 0, 0  # Return 0 in case of an error



