# ------ built-in modules ------ #
import os
import subprocess as sp
import gpiozero as gz
import RPi.GPIO as GPIO
from datetime import timedelta

# ------ pip modules ------ #
import psutil

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
    d = {}
    d['current'] = freq[0],
    d['min'] = freq[1],
    d['max'] = freq[2],
    d['pct'] = round((freq[0] / freq[2] * 100), 1),   # global
    return d

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
    d = dict(psutil.cpu_times()._asdict())
    for key in list(d.keys()):
        key2 = str('CPU time ') + str(key)   # new key
        d[str(key2)] = d.pop(key)   # set new key and delete old key
        time_temp = d[key2] # get time
        d[key2] = "{:0>8}".format(str(timedelta(seconds=time_temp)))    # format time
    return d

def cpu_details1():
    # Architecture, Byte Order, CPU(s), On-line CPU(s) list, Thread(s) per core, Core(s) per socket, Socket(s), Vendor ID, Model, Model name, Stepping, CPU max MHz, CPU min MHz, BogoMIPS, Flags
    process = sp.run('lscpu', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    # result = dict(line.split(':', 1)
    d = dict(map(str.strip, line.split(':', 1))
        for line in output.split('\n') if ':' in line)
    return d

def cpu_details2():
    # Hardware, Revision, Serial, Model, freq, temp
    process = sp.run('cat /proc/cpuinfo', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    d1 = dict(map(str.strip, line.split(':', 1))
        for line in output.split('\n') if ':' in line)
    # result = {key: val for key, val in result1.items() if key == 'Hardware' or key == 'Revision' or key == 'Serial' or key == 'Model'}
    d = {key: val for key, val in d1.items() if key == 'Hardware' or key == 'Revision' or key == 'Serial'}
    d['CPU frequency MHz'] = cpu_freq().get('current')[0]
    d['CPU temperature °C'] = cpu_temp()[0]
    d['CPU load %'] = cpu_load_avg_pct()[0]
    return d

def cpu_stats():
    # ctx_switches, interrupts, soft_interrupts, syscalls
    d = dict(psutil.cpu_stats()._asdict())
    return d

#####################
# ------ SoC ------ #
#####################

def soc_clocks():
    # https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md
    # https://elinux.org/RPI_vcgencmd_usage

    # clocks = ['arm', 'core', 'h264', 'isp', 'v3d', 'uart', 'pwm', 'emmc', 'pixel', 'vec', 'hdmi', 'dpi']
    process = sp.run('for src in arm core h264 isp v3d uart pwm emmc pixel vec hdmi dpi ; do echo "$src: $(/opt/vc/bin/vcgencmd measure_clock $src)" ; done', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    d = dict(map(str.strip, line.split(':'))
        for line in output.split('\n') if ':' in line)
    for key in d.keys():
        d[key] = d[key].split("=", 1)
        d[key] = str(int(d[key][1]) / 1000000) + str(' MHz')     # calc/add MHz
    return d

def soc_codecs():
    # https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md
    # https://elinux.org/RPI_vcgencmd_usage

    # codecs = ['AGIF', 'FLAC', 'H263', 'H264', 'MJPA', 'MJPB', 'MJPG', 'MPG2', 'MPG4', 'MVC0', 'PCM', 'THRA', 'VORB', 'VP6', 'VP8', 'WMV9', 'WVC1']
    process = sp.run('for codec in AGIF FLAC H263 H264 MJPA MJPB MJPG MPG2 MPG4 MVC0 PCM THRA VORB VP6 VP8 WMV9 WVC1 ; do echo "$codec: $(/opt/vc/bin/vcgencmd codec_enabled $codec)" ; done', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    d = dict(map(str.strip, line.split(':'))
        for line in output.split('\n') if ':' in line)
    for key in d.keys():
        d[key] = d[key].split("=", 1)
        d[key] = d[key][1]
    return d

def soc_config():
    # https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md
    # https://elinux.org/RPI_vcgencmd_usage

    process = sp.run('vcgencmd get_config int', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    d = dict(map(str.strip, line.split('='))
                for line in output.split('\n') if '=' in line)
    return d

def soc_volts():
    # https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md
    # https://elinux.org/RPI_vcgencmd_usage

    # volts = ['core', 'sdram_c', 'sdram_i', 'sdram_p']
    process = sp.run('for volt in core sdram_c sdram_i sdram_p ; do echo "$volt: $(/opt/vc/bin/vcgencmd measure_volts $volt)" ; done',
        shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    d = dict(map(str.strip, line.split(':'))
        for line in output.split('\n') if ':' in line)
    for key in d.keys():
        d[key] = d[key].split("=", 1)
        d[key] = d[key][1]
    return d

def soc_firmware():
    # https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md
    # https://elinux.org/RPI_vcgencmd_usage

    process = sp.run('vcgencmd version', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    result = output.split('\n')
    result.pop(3)   # delete last trash value ''
    return result
print(soc_firmware())

########################
# ------ Memory ------ #
########################

def mem_info():
    # total, available, percent, used, free, active, inactive, buffers, cached, shared, slab
    d = dict(psutil.virtual_memory()._asdict())
    d['total'] = bytes2human(d['total'])
    d['available'] = bytes2human(d['available'])
    d['used'] = bytes2human(d['used'])
    d['free'] = bytes2human(d['free'])
    d['active'] = bytes2human(d['active'])
    d['inactive'] = bytes2human(d['inactive'])
    d['buffers'] = bytes2human(d['buffers'])
    d['cached'] = bytes2human(d['cached'])
    d['shared'] = bytes2human(d['shared'])
    d['slab'] = bytes2human(d['slab'])
    return d

def mem_meminfo():
    process = sp.run('cat /proc/meminfo', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    d = dict(map(str.strip, line.split(':', 1))
        for line in output.split('\n') if ':' in line)
    return d

def mem_usage():
    # 13.2  1135 pi       /usr/lib/jvm/
    process = sp.run('ps -e -o pmem,pid,user,args --sort=-pmem | sed "/^ 0.0 /d" | grep -v MEM', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    result = output.split('\n')
    i = 0
    for i in range(len(result)):
        mem_percent = result[i][:4].strip()
        pid = result[i][5:11].strip()
        user = result[i][11:19].strip()
        command = result[i][20:100].strip()
        result[i] = [mem_percent, pid, user, command]
    return result

def mem_swap():
    # total, used, free, percent, sin, sout
    d = dict(psutil.swap_memory()._asdict())
    d['total'] = bytes2human(d['total'])
    d['used'] = bytes2human(d['used'])
    d['free'] = bytes2human(d['free'])
    return d

######################
# ------ Disk ------ #
######################

def disk_info():
    # total, used, free, percent
    d = dict(psutil.disk_usage('/')._asdict())
    d['total'] = bytes2human(d['total'])
    d['used'] = bytes2human(d['used'])
    d['free'] = bytes2human(d['free'])
    return d

def disk_io_counters():
    # read_count, write_count, read_bytes, write_bytes, read_time, write_time, read_merged_count, write_merged_count, busy_time, total_bytes
    d = dict(psutil.disk_io_counters()._asdict())
    d['total_bytes'] = d['read_bytes'] + d['write_bytes']
    d['total_bytes'] = bytes2human(d['total_bytes'])
    d['read_bytes'] = bytes2human(d['read_bytes'])
    d['write_bytes'] = bytes2human(d['write_bytes'])
    return d

def disk_partitions():
    # [('/', '/dev/root', 99.1, 'ext4', '/', 'rw,noatime', '1.343TB'),
    partitions = []
    for partition in psutil.disk_partitions(all=True):
        try:
            pdiskusage = psutil.disk_usage(partition.mountpoint)
            partitions.append((partition.mountpoint,
                partition.device,
                100.0 - pdiskusage.percent,
                partition.fstype,
                partition.mountpoint,
                partition.opts,
                bytes2human(pdiskusage.total),
            ))
        except OSError:
            continue
    return partitions

#########################
# ------ Network ------ #
#########################

def net_io_counters():
    # bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout, total_bytes
    d = dict(psutil.net_io_counters()._asdict())
    d['total_bytes'] = d['bytes_recv'] + d['bytes_sent']
    d['total_bytes'] = bytes2human(d['total_bytes'])
    d['bytes_recv'] = bytes2human(d['bytes_recv'])
    d['bytes_sent'] = bytes2human(d['bytes_sent'])
    return d

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
    d = dict(map(str.strip, line.split('=', 1))
        for line in output.split('\n') if '=' in line)
    d = d['PRETTY_NAME'].strip('"')
    return d

def sys_hostname():
    process = sp.run('hostname -f', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    result = process.stdout
    return result

def sys_users_online():
    process = sp.run('who -u | wc -l', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    result = process.stdout
    return result

def sys_modules():
    # btbcm                  16384  1 hci_uart
    process = sp.run('lsmod | grep -v Size', shell=True, check=True, stdout=sp.PIPE, universal_newlines=True)
    output = process.stdout
    result = output.split('\n')
    i = 0
    #for i in range(len(result)):
     #   result[i] = str(result[i].split(' '))
    #     size = result[i][5:11].strip()
    #     used = result[i][11:19].strip()
    #     by = result[i][20:100].strip()
    #     result[i] = module, size, used, by
    return result
# print(sys_modules())

#####################################################################

def test():
    # total, used, free, percent
    gpios = '2,5,7,8,10,11,12,15,16,18,19,21,22,23,24,26'
    process = sp.run('raspi-gpio get ' + gpios, shell=True, check=True, stdout=sp.PIPE,
                     universal_newlines=True)
    output = process.stdout
    d = dict(map(str.strip, line.split(':', 1))
        for line in output.split('\n') if ':' in line
                  )
    for key in list(d.keys()):
        key2 = str(key.replace(' ', ''))
        d[str(key2)] = d.pop(key)

    for key, value in list(d.items()):
        d[key] = str(d[key]).split(' ')

        d[key][0] = d[key][0].strip('level=')
        d[key][1] = d[key][1].strip('fsel=')
        if d[key][1] != '0':
            d[key][2] = d[key][2].strip('alt=')
            d[key][3] = d[key][3].strip('func=')
            d[key][4] = d[key][4].strip('pull=')
        else:
            d[key][2] = d[key][2].strip('func=')
            d[key][3] = d[key][3].strip('pull=')

    #print('{0}'.format(pi_info().headers['J8']))
    #print('{0:full}'.format(pi_info().headers['J8']))
    #print(pi_info().headers['J8'])
    #print(pi_info().headers['J8'].pins[3])
    print(gz.pi_info().revision)
    #print(pi_info().soc)
    #print(pi_info().board)
    #print('{0}'.format(pi_info()))
    #                                       print('{0:board}'.format(gz.pi_info()))
    # GPIO.setmode(GPIO.BOARD)  # 10
    if (GPIO.getmode() != 11):
        GPIO.setmode(GPIO.BCM)
    mode = GPIO.getmode()

    print(mode)




    # for key in list(d.keys()):
    #     len1 = len(d[key])      # count values
    #     for i in range(len1):
    #         d[i] = d[key][i].split('=')
    #         d[i] = {d[i][0]:d[i][1]}
    #         print (key, i, d[i])

    #print (d['GPIO2'][0], d['GPIO2'][1])
    return d

print(test())