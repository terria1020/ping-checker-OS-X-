import subprocess
import sys
import time
import configparser

ini = configparser.ConfigParser()
ini.read("setting.ini")

ip = ini['Settings']['ip']
ms_criteria = float(ini['Settings']['ms_criteria'])
cycle_criteria = float(ini['Settings']['cycle_criteria'])
sound_toggle = (ini['Settings']['sound'] == 'True')
message = ini['Settings']['message']

command = ["ping", ip, "-c", "1"]

def beep(level):
    comment = f"{level} ping!"
    if sound_toggle:
        subprocess.call(["say", message])
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
    try:
        while (True):
            output = request()
            if (output.find("time=") < 0):
                beep("dead")
            else:
                ms = get_mil_sec(output)
                if ms > ms_criteria:
                    beep(f"[{ms} ms] high")
                    
                else:
                    print(f"ping: {ms} ms")
            time.sleep(cycle_criteria)
    except KeyboardInterrupt:
        print("\nKeyboard 인터럽트를 통한 프로그램 종료입니다.")

if __name__ == '__main__':
    main()