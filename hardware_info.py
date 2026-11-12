
import subprocess
import json


# --------------------------------------------------
# COMMON COMMAND EXECUTION
# --------------------------------------------------

def run_command(command):

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )

        return {
            "status": "success",
            "output": result.stdout,
            "error": None
        }

    except FileNotFoundError:
        return {
            "status": "error",
            "output": None,
            "error": "command_not_found"
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "output": None,
            "error": "command_timeout"
        }

    except subprocess.CalledProcessError as error:
        return {
            "status": "error",
            "output": None,
            "error": "command_failed",
            "details": error.stderr.strip() if error.stderr else None
        }


# --------------------------------------------------
# CPU INFORMATION
# --------------------------------------------------

def get_cpu_info():

    result = run_command(["lscpu"])

    if result["status"] == "error":
        return {
            "status": "unavailable",
            "message": "Unable to retrieve CPU information",
            "error": result["error"]
        }

    cpu_data = {}

    for line in result["output"].splitlines():

        if ":" in line:
            key, value = line.split(":", 1)
            cpu_data[key.strip()] = value.strip()

    try:

        logical_cpus = int(cpu_data["CPU(s)"])
        cores_per_socket = int(cpu_data["Core(s) per socket"])
        sockets = int(cpu_data["Socket(s)"])

        return {
            "status": "success",
            "model": cpu_data.get("Model name"),
            "architecture": cpu_data.get("Architecture"),
            "logical_cpus": logical_cpus,
            "cores_per_socket": cores_per_socket,
            "sockets": sockets,
            "threads_per_core": int(
                cpu_data["Thread(s) per core"]
            ),
            "physical_cores": cores_per_socket * sockets
        }

    except (ValueError, TypeError, KeyError):
        return {
            "status": "error",
            "message": "Unable to parse CPU information"
        }


# --------------------------------------------------
# MEMORY INFORMATION
# --------------------------------------------------

def get_memory_info():

    result = run_command(["free", "-b"])

    if result["status"] == "error":
        return {
            "status": "unavailable",
            "message": "Unable to retrieve memory information",
            "error": result["error"]
        }

    for line in result["output"].splitlines():

        if line.startswith("Mem:"):

            values = line.split()

            try:

                return {
                    "status": "success",
                    "total_bytes": int(values[1]),
                    "used_bytes": int(values[2]),
                    "free_bytes": int(values[3]),
                    "available_bytes": int(values[6])
                }

            except (ValueError, IndexError):
                return {
                    "status": "error",
                    "message": "Unable to parse memory information"
                }

    return {
        "status": "error",
        "message": "Memory information not found"
    }


# --------------------------------------------------
# STORAGE INFORMATION
# --------------------------------------------------

def get_storage_info():

    result = run_command([
        "lsblk",
        "-b",
        "-J",
        "-o",
        "NAME,SIZE,TYPE,MODEL,ROTA,TRAN"
    ])

    if result["status"] == "error":
        return {
            "status": "unavailable",
            "message": "Unable to retrieve storage information",
            "error": result["error"],
            "devices": []
        }

    try:

        data = json.loads(result["output"])

        devices = []

        for disk in data.get("blockdevices", []):

            devices.append({
                "name": disk.get("name"),
                "size_bytes": disk.get("size"),
                "type": disk.get("type"),
                "model": disk.get("model"),
                "rotational": disk.get("rota"),
                "transport": disk.get("tran"),
                "drive_type": (
                    "Rotational"
                    if disk.get("rota") is True
                    else "Non-rotational"
                    if disk.get("rota") is False
                    else "Unknown"
                )
            })

        return {
            "status": "success",
            "devices": devices
        }

    except (json.JSONDecodeError, TypeError, AttributeError):
        return {
            "status": "error",
            "message": "Unable to parse storage information",
            "devices": []
        }


# --------------------------------------------------
# GPU INFORMATION
# --------------------------------------------------

def get_gpu_info():

    result = run_command([
        "nvidia-smi",
        "--query-gpu=name,memory.total,memory.used,temperature.gpu,utilization.gpu",
        "--format=csv,noheader,nounits"
    ])

    if result["status"] == "error":
        return {
            "status": "unavailable",
            "message": "GPU information unavailable",
            "error": result["error"],
            "devices": []
        }

    gpu_devices = []

    try:

        for line in result["output"].strip().splitlines():

            values = [v.strip() for v in line.split(",")]

            if len(values) != 5:
                continue

            gpu_devices.append({
                "name": values[0],
                "memory_total_mb": int(values[1]),
                "memory_used_mb": int(values[2]),
                "temperature_c": int(values[3]),
                "utilization_percent": int(values[4])
            })

        return {
            "status": "success" if gpu_devices else "no_gpu_detected",
            "devices": gpu_devices
        }

    except (ValueError, IndexError):
        return {
            "status": "error",
            "message": "Unable to parse GPU information",
            "devices": []
        }


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

if __name__ == "__main__":

    hardware_info = {
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "storage": get_storage_info(),
        "gpu": get_gpu_info()
    }

    print(json.dumps(hardware_info, indent=4))
