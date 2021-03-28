import subprocess
import sys
import time

command = ["ping", "192.168.0.1", "-c", "1"]
criteria = 50.0

def beep(level):
    comment = f"{level} ping!"
    subprocess.call(["say", "ping problem!"])
    print(comment)

def get_mil_sec(out):
    s_out = out.split("time=")
    need = s_out[1].split("ms")
    return float(need[0])
    return s_out

def request():
    ping = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = ping.communicate()
    ping.terminate()
    return out.decode()

def main():
    while (True):
        output = request()
        if (output.find("time=") < 0):
            beep("dead")
        else:
            ms = get_mil_sec(output)
            if ms > criteria:
                beep("high")
            else:
                print(f"ping: {ms} ms")
        time.sleep(0.5)

if __name__ == '__main__':
    main()