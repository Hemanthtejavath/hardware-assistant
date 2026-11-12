import subprocess

try:
    result = subprocess.run(
        ["fake-nvidia-command"],
        capture_output=True,
        text=True,
        check=True
    )

    print(result.stdout)

except FileNotFoundError:
    print("NVIDIA inspection tool is not installed.")

except subprocess.CalledProcessError:
    print("Unable to retrieve GPU information.")
