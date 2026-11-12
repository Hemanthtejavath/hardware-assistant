
from hardware_info import (
    get_cpu_info,
    get_memory_info,
    get_storage_info,
    get_gpu_info
)


def get_cpu_details():
    """Get CPU model, architecture, physical cores and logical CPUs."""
    return get_cpu_info()


def get_memory_details():
    """Get total, used, free and available system memory in bytes."""
    return get_memory_info()


def get_storage_details():
    """Get detected storage devices, capacity, model and device properties."""
    return get_storage_info()


def get_gpu_details():
    """Get NVIDIA GPU model, memory usage, temperature and utilization."""
    return get_gpu_info()
