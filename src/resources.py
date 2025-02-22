import psutil


def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

def get_network_activity():
    network_stats = psutil.net_io_counters(pernic=True)
    network_activity = {}
    for interface, stats in network_stats.items():
        network_activity[interface] = {
            "bytes_sent": stats.bytes_sent,
            "bytes_received": stats.bytes_recv
        }
    return network_activity

def get_memory_usage():
    memory = psutil.virtual_memory()

    total_memory = memory.total
    available_memory = memory.available
    used_memory = memory.used
    memory_usage_percentage = memory.percent
    return {
        "total_memory": to_gigabyte(total_memory),
        "available_memory": to_gigabyte(available_memory),
        "used_memory": to_gigabyte(used_memory),
        "memory_usage_percentage": memory_usage_percentage
    }


def to_gigabyte(bits):
    return round(bits / (1024 * 1024 * 1024), 2)
