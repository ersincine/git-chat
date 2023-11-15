
import subprocess


def run_command(command: list[str], critical: bool=True) -> tuple[str, bool]:
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.stdout.read().decode("utf-8")
    success = p.wait() == 0
    if critical:
        assert success, output
    return output, success
