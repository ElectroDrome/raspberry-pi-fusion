# ------ built-in modules ------ #
import os
import subprocess as sp
from datetime import timedelta

# ------ pip modules ------ #
import psutil

# ------ General ------ #
# ------ Board ------ #
# ------ CPU ------ #
# ------ SoC ------ #
# ------ Disk ------ #
# ------ Memory ------ #
# ------ Network ------ #
# ------ System ------ #

# import os
    # tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])

    # linux_filepath = "/proc/meminfo"
    # meminfo = dict(
    #     (i.split()[0].rstrip(":"), int(i.split()[1]))
    #     for i in open(linux_filepath).readlines()
    # )

#########################
# ------ General ------ #
#########################

def bytes2human(n):
    # Convert a number of bytes into a human readable format
    symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.3f%s' % (value, s)    # 3 digits
    return "%sB" % n

#######################
# ------ Board ------ #
#######################

def board_model():
    process = sp.run('cat /sys/firmware/devicetree/base/model', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    result = process.stdout
    result = result[:-1]
    return result

#####################
# ------ CPU ------ #
#####################

def cpu_freq():
    freq = psutil.cpu_freq()
    result = {}
    result['current'] = freq[0],
    result['min'] = freq[1],
    result['max'] = freq[2],
    result['pct'] = round((freq[0] / freq[2] * 100), 1),   # global
    return result

def cpu_load():
    result = psutil.cpu_percent(interval=1)    # freeze 1 sec
    return result

def cpu_load_avg_pct():    # v02 percentage representation with CPU count
    result = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
    return result

# def cpu_load_avg_pct():    # v01
#     l1m, l5m, l15m = os.getloadavg()
#     return l1m, l5m, l15m

def cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = round((float(f.read()) / 1000.0), 2)
        temp_max = round(85.0, 1)    # need further info for temp issues
        temp_pct = round((temp / temp_max * 100), 1)
    return temp, temp_max, temp_pct

def cpu_times():
    # user, nice, system, idle, iowait, irq, softirq, steal, guest, guest_nice
    result = dict(psutil.cpu_times()._asdict())

    result['CPU time user'] = result.pop('user')
    time_temp = result['CPU time user']
    result['CPU time user'] = "{:0>8}".format(str(timedelta(seconds=time_temp)))

    result['CPU time nice'] = result.pop('nice')
    time_temp = result['CPU time nice']
    result['CPU time nice'] = "{:0>8}".format(str(timedelta(seconds=time_temp)))

    result['CPU time system'] = result.pop('system')
    time_temp = result['CPU time system']
    result['CPU time system'] = "{:0>8}".format(str(timedelta(seconds=time_temp)))

    result['CPU time idle'] = result.pop('idle')
    time_temp = result['CPU time idle']
    result['CPU time idle'] = "{:0>8}".format(str(timedelta(seconds=time_temp)))

    result['CPU time iowait'] = result.pop('iowait')
    time_temp = result['CPU time iowait']
    result['CPU time iowait'] = "{:0>8}".format(str(timedelta(seconds=time_temp)))

    result['CPU time irq'] = result.pop('irq')
    time_temp = result['CPU time irq']
    result['CPU time irq'] = "{:0>8}".format(str(timedelta(seconds=time_temp)))

    result['CPU time softirq'] = result.pop('softirq')
    time_temp = result['CPU time softirq']
    result['CPU time softirq'] = "{:0>8}".format(str(timedelta(seconds=time_temp)))

    result['CPU time steal'] = result.pop('steal')
    time_temp = result['CPU time steal']
    result['CPU time steal'] = "{:0>8}".format(str(timedelta(seconds=time_temp)))

    result['CPU time guest'] = result.pop('guest')
    time_temp = result['CPU time guest']
    result['CPU time guest'] = "{:0>8}".format(str(timedelta(seconds=time_temp)))

    result['CPU time guest_nice'] = result.pop('guest_nice')
    time_temp = result['CPU time guest_nice']
    result['CPU time guest_nice'] = "{:0>8}".format(str(timedelta(seconds=time_temp)))

    return result

def cpu_details1():
    # Architecture, Byte Order, CPU(s), On-line CPU(s) list, Thread(s) per core, Core(s) per socket, Socket(s), Vendor ID, Model, Model name, Stepping, CPU max MHz, CPU min MHz, BogoMIPS, Flags
    process = sp.run('lscpu', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    # result = dict(line.split(':', 1)
    result = dict(map(str.strip, line.split(':', 1))
        for line in output.split('\n') if ':' in line)
    return result

def cpu_details2():
    # Hardware, Revision, Serial, Model, freq, temp
    process = sp.run('cat /proc/cpuinfo', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    result1 = dict(map(str.strip, line.split(':', 1))
        for line in output.split('\n') if ':' in line)
    # result = {key: val for key, val in result1.items() if key == 'Hardware' or key == 'Revision' or key == 'Serial' or key == 'Model'}
    result = {key: val for key, val in result1.items() if key == 'Hardware' or key == 'Revision' or key == 'Serial'}
    result['CPU frequency MHz'] = cpu_freq().get('current')[0]
    result['CPU temperature °C'] = cpu_temp()[0]
    result['CPU load %'] = cpu_load_avg_pct()[0]
    return result

def cpu_stats():
    # ctx_switches, interrupts, soft_interrupts, syscalls
    result = dict(psutil.cpu_stats()._asdict())
    return result

#####################
# ------ SoC ------ #
#####################

def soc_clocks():
    # https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md
    # https://elinux.org/RPI_vcgencmd_usage

    # clocks = ['arm', 'core', 'h264', 'isp', 'v3d', 'uart', 'pwm', 'emmc', 'pixel', 'vec', 'hdmi', 'dpi']
    process = sp.run('for src in arm core h264 isp v3d uart pwm emmc pixel vec hdmi dpi ; do echo "$src: $(/opt/vc/bin/vcgencmd measure_clock $src)" ; done', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    result = dict(map(str.strip, line.split(':'))
        for line in output.split('\n') if ':' in line
        )
    for key in result.keys():
        result[key] = result[key].split("=", 1)
        result[key] = str(int(result[key][1]) / 1000000) + str(' MHz')     # calc/add MHz
    return result

def soc_codecs():
    # https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md
    # https://elinux.org/RPI_vcgencmd_usage

    # codecs = ['AGIF', 'FLAC', 'H263', 'H264', 'MJPA', 'MJPB', 'MJPG', 'MPG2', 'MPG4', 'MVC0', 'PCM', 'THRA', 'VORB', 'VP6', 'VP8', 'WMV9', 'WVC1']
    process = sp.run('for codec in AGIF FLAC H263 H264 MJPA MJPB MJPG MPG2 MPG4 MVC0 PCM THRA VORB VP6 VP8 WMV9 WVC1 ; do echo "$codec: $(/opt/vc/bin/vcgencmd codec_enabled $codec)" ; done', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    result = dict(map(str.strip, line.split(':'))
        for line in output.split('\n') if ':' in line
        )
    for key in result.keys():
        result[key] = result[key].split("=", 1)
        result[key] = result[key][1]
    return result

def soc_config():
    # https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md
    # https://elinux.org/RPI_vcgencmd_usage

    process = sp.run('vcgencmd get_config int', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    result = dict(map(str.strip, line.split('='))
        for line in output.split('\n') if '=' in line
        )
    return result

def soc_volts():
    # https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md
    # https://elinux.org/RPI_vcgencmd_usage

    # volts = ['core', 'sdram_c', 'sdram_i', 'sdram_p']
    process = sp.run('for volt in core sdram_c sdram_i sdram_p ; do echo "$volt: $(/opt/vc/bin/vcgencmd measure_volts $volt)" ; done',
        shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    result = dict(map(str.strip, line.split(':'))
        for line in output.split('\n') if ':' in line
        )
    for key in result.keys():
        result[key] = result[key].split("=", 1)
        result[key] = result[key][1]
    return result

########################
# ------ Memory ------ #
########################

def mem_info():     # v02
    # total, available, percent, used, free, active, inactive, buffers, cached, shared, slab
    result = dict(psutil.virtual_memory()._asdict())
    result['total'] = bytes2human(result['total'])
    result['available'] = bytes2human(result['available'])
    result['used'] = bytes2human(result['used'])
    result['free'] = bytes2human(result['free'])
    result['active'] = bytes2human(result['active'])
    result['inactive'] = bytes2human(result['inactive'])
    result['buffers'] = bytes2human(result['buffers'])
    result['cached'] = bytes2human(result['cached'])
    result['shared'] = bytes2human(result['shared'])
    result['slab'] = bytes2human(result['slab'])
    return result

# def mem_info():    # v01
#     mem = psutil.virtual_memory()
#     result = {}
#     result['total'] = mem[0],
#     result['available'] = mem[1],
#     result['percent'] = mem[2],
#     result['used'] = mem[3],
#     result['free'] = mem[4],
#     result['active'] = mem[5],
#     result['inactive'] = mem[6],
#     result['buffers'] = mem[7],
#     result['cached'] = mem[8],
#     result['shared'] = mem[9],
#     result['slab'] = mem[10]
#     return result

def mem_meminfo():
    process = sp.run('cat /proc/meminfo', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    result = dict(map(str.strip, line.split(':', 1))
        for line in output.split('\n') if ':' in line)
    return result

def mem_swap():
    # total, used, free, percent, sin, sout
    result = dict(psutil.swap_memory()._asdict())
    result['total'] = bytes2human(result['total'])
    result['used'] = bytes2human(result['used'])
    result['free'] = bytes2human(result['free'])
    return result

######################
# ------ Disk ------ #
######################

def disk_info():
    # total, used, free, percent
    result = dict(psutil.disk_usage('/')._asdict())
    result['total'] = bytes2human(result['total'])
    result['used'] = bytes2human(result['used'])
    result['free'] = bytes2human(result['free'])
    return result

def disk_io_counters():
    # read_count, write_count, read_bytes, write_bytes, read_time, write_time, read_merged_count, write_merged_count, busy_time, total_bytes
    result = dict(psutil.disk_io_counters()._asdict())
    result['total_bytes'] = result['read_bytes'] + result['write_bytes']
    result['total_bytes'] = bytes2human(result['total_bytes'])
    result['read_bytes'] = bytes2human(result['read_bytes'])
    result['write_bytes'] = bytes2human(result['write_bytes'])
    return result

#########################
# ------ Network ------ #
#########################

def net_io_counters():
    # bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout, total_bytes
    result = dict(psutil.net_io_counters()._asdict())
    result['total_bytes'] = result['bytes_recv'] + result['bytes_sent']
    result['total_bytes'] = bytes2human(result['total_bytes'])
    result['bytes_recv'] = bytes2human(result['bytes_recv'])
    result['bytes_sent'] = bytes2human(result['bytes_sent'])
    return result

def net_connections():
    process = sp.run('netstat -nta --inet | wc -l', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    result = process.stdout
    return result

########################
# ------ System ------ #
########################

def sys_runstart():
    # runstart -> Sa 20. Jun 12:46:44 CEST 2020
    process = sp.run("date -d @$(( $(date +%s) - $(cut -f1 -d. /proc/uptime) ))", shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    result = process.stdout
    return result

def sys_runtime():
    # runtime -> 0d 02:16:30
    process = sp.run("TZ=UTC date -d@$(cut -d\  -f1 /proc/uptime) +'%j %T' | awk '{print $1-1 \"d\",$2}'", shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    result = process.stdout
    return result

def sys_kernel():
    process = sp.run('uname -mrs', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    result = process.stdout
    return result

def sys_firmware():
    process = sp.run('uname -v', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    result = process.stdout
    return result

def sys_dist():
    process = sp.run('cat /etc/*-release | grep PRETTY_NAME=', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    result = dict(map(str.strip, line.split('=', 1))
        for line in output.split('\n') if '=' in line)
    result = result['PRETTY_NAME'].strip('"')
    return result

def sys_hostname():
    process = sp.run('hostname -f', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    result = process.stdout
    return result

def sys_users_online():
    process = sp.run('who -u | wc -l', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    result = process.stdout
    return result


