import subprocess
import time


def start_subproc():
    obsproc = subprocess.Popen(
        [
            r"C:\Program Files\Wireshark\tshark.exe",
            "-i",
            "TCP@127.0.0.1:57012",
            "--hexdump",
            "ascii",
            "frames",
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    try:
        for line in iter(obsproc.stdout.readline, b""):
            yield line
    except KeyboardInterrupt:
        try:
            time.sleep(1)
        except:
            pass
        try:
            obsproc.kill()
        except Exception as e:
            print(e)


captured_lines = []
good_lines = []
try:
    for captured_line in start_subproc():
        if not captured_line.strip() and captured_lines:
            if captured_lines[-1].strip().endswith(b";|"):
                for good_captured_line in captured_lines:
                    print(good_captured_line.rstrip()[-16:].decode("utf-8"), end='')
                captured_lines.clear()
                print()
        else:
            captured_lines.append(captured_line)
except KeyboardInterrupt:
    pass
