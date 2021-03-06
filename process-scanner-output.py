import sys

with open(sys.argv[1]) as kal_input:
    kal_input.readline()

    ppm = sys.argv[2]

    try: 
        int(ppm)
        pass
    except ValueError:
        print("ppm must be an integer when running " + sys.argv[0] + " ,see README")
        raise SystemExit

    try:
        rtl_optional_args = sys.argv[3]
    except:
        rtl_optional_args = ""
    
    print("#!/bin/bash")
    print("")
    
    print("if [[ $(/usr/bin/id -u) -ne 0 ]]; then")
    print("echo 'Not running as root'")
    print("exit")
    print("fi")
    print("")

    print("bash ./stop.sh")
    print("")

    print("echo 'Control-C to stop looping round GSM channels'")
    print("sleep 1 ")
    print("pkill -f grgsm_livemon_headless")
    print("pkill -f tshark")
    print("")

    print("while [ 1 ]")
    print("do")
    print("sudo stdbuf -i0 -o0 -e0 tshark -i lo -Y e212.imsi -T fields -e e212.imsi -e frame.time -E separator=, -E quote=d -E occurrence=f >> imsi.csv 2>/dev/null &")
    average_ppm_offset = 0.
    valid_stations = 0
    for line in kal_input:
        if "ARFCN:" in line:
            frequency=line.split(",")[1][7:]
            print("echo 'Processing " + frequency + "'")            
            print(" grgsm_livemon_headless -p " + ppm + " " + rtl_optional_args + " -g 40 -s 2000000 -f " 
                                + frequency + " > /dev/null 2>&1 < /dev/null &")
            print(" sleep 300")
            print(" pkill -f grgsm_livemon_headless")

    print("done")