#!/usr/bin python3
from src.windows import *
import RPi.GPIO as GPIO

def menus():

    ##################################
    # ------ Theme Definition ------ #
    ##################################
    sg.theme('Topanga')
    sg.set_options(element_padding=(0, 0))

    #################################
    # ------ Menu Definition ------ #
    #################################
    menu_def = [['&Program', ['&Settings',
                              'E&xit', '---',
                              '&About Pi Fusion',
                              '&Credits',
                              '&Donation']],
                ['&Control'],
                ['&Info', ['&Board',
                           '&SoC (CPU & GPU)', ['&CPU Details', '&GPU', '&SoC Details'],
                           '&Disk', ['&Partitions Details'],
                           '&Interfaces', ['&Audio / Video', '&GPIO Status', '&USB Devices'],
                           '&Memory', ['Memory &Details'],
                           #'&!Network',
                           '&Network',
                           '&Operating system', ['&Cron jobs', '&General info', '&Kernel modules', 'Running &processes', 'Running &services', '&Software packages', '&Users & groups'],
                            ],
                 ],
                ['&Monitor'],
                ['&Tools', ['---', 'Command &1', 'Command &2',
                              '---', 'Command &3', 'Command &4']],
                ['&Add-ons'],
                ['&Docs'],
               ]

    ##########################
    # ------ Init vars------ #
    ##########################
    win_cpu_temp_pct = 0
    win_cpu_temp_text = 0
    win_cpu_temp_max = cpu_temp()[1]

    win_cpu_freq_pct = 0
    win_cpu_freq_text = 0
    win_cpu_freq_max = cpu_freq().get('max')[0]

    win_cpu_load_avg_pct = 0
    win_cpu_load_avg_1m_text = ''
    win_cpu_load_avg_5m_text = ''
    win_cpu_load_avg_15m_text = ''

    win_mem_info_pct = 0.00
    win_mem_info_used_text = ''
    win_mem_info_free_text = ''
    win_mem_info_total_text = ''

    win_mem_swap_pct = 0
    win_mem_swap_used_text = ''
    win_mem_swap_free_text = ''
    win_mem_swap_total_text = ''

    win_disk_info_pct_text = 0
    win_disk_io_counters_pct_text = 0.00
    win_disk_info_used_text = ''
    win_disk_info_free_text = ''
    win_disk_info_total_text = ''

    win_disk_read_text = ''
    win_disk_write_text = ''
    win_disk_total_text = ''

    win_net_io_sent_text = ''
    win_net_io_recv_text = ''
    win_net_io_total_text = ''

    win_net_conn = 0
    win_sys_users = ''

    ###################################
    # ------ Column Definition ------ #
    ###################################

    col1 = [[sg.Text('CPU temp',size=(9,1)), sg.Text(win_cpu_temp_text, size=(5, 1), key='cpu_temp_text'), sg.Text('°C of max.', size=(9, 1)), sg.Text(win_cpu_temp_max, size=(5, 1))],
            [sg.ProgressBar(100, orientation='h', size=(33, 10), key='cpu_temp'), sg.Text(win_cpu_temp_pct, size=(5, 1), key='cpu_temp_pct' )],
            [sg.Text('CPU load avg', size=(12, 1)), sg.Text(win_cpu_load_avg_1m_text, size=(10, 1), key='cpu_load_avg_1m_text'), sg.Text(win_cpu_load_avg_5m_text , size=(10, 1), key='cpu_load_avg_5m_text'), sg.Text(win_cpu_load_avg_15m_text , size=(10, 1), key='cpu_load_avg_15m_text')],
            [sg.ProgressBar(100, orientation='h', size=(33, 10), key='cpu_load_avg'), sg.Text(win_cpu_load_avg_pct, size=(5, 0), key='cpu_load_avg_pct')],
            [sg.Text('CPU MHz', size=(9, 1)), sg.Text(win_cpu_freq_text, size=(6, 1), key='cpu_freq_text'), sg.Text('of max.', size=(6, 1)), sg.Text(win_cpu_freq_max)],
            [sg.ProgressBar(100, orientation='h', size=(33, 10), key='cpu_freq'), sg.Text(win_cpu_freq_pct, size=(5, 0), key='cpu_freq_pct')],
            [sg.Text('RAM', size=(6, 1)), sg.Text('used', size=(4, 1)), sg.Text(win_mem_info_used_text, size=(10, 1), key='mem_info_used_text'), sg.Text('free', size=(4, 1)), sg.Text(win_mem_info_free_text, size=(10, 1), key='mem_info_free_text'), sg.Text('total', size=(4, 1)), sg.Text(win_mem_info_total_text, size=(10, 1), key='mem_info_total_text')],
            [sg.ProgressBar(100, orientation='h', size=(33, 10), key='mem_info'), sg.Text(win_mem_swap_pct, size=(5, 0), key='mem_info_pct')],
            [sg.Text('SWAP', size=(6, 1)), sg.Text('used', size=(4, 1)), sg.Text(win_mem_info_used_text, size=(10, 1), key='mem_swap_used_text'), sg.Text('free', size=(4, 1)), sg.Text(win_mem_swap_free_text, size=(10, 1), key='mem_swap_free_text'), sg.Text('total', size=(4, 1)), sg.Text(win_mem_swap_total_text, size=(10, 1), key='mem_swap_total_text')],
            [sg.ProgressBar(100, orientation='h', size=(33, 10), key='mem_swap'), sg.Text(win_mem_swap_pct, size=(5, 0), key='mem_swap_pct')],
            [sg.Text('DISK /', size=(6, 1)), sg.Text('used', size=(4, 1)), sg.Text(win_disk_info_used_text, size=(10, 1), key='disk_info_used_text'), sg.Text('free', size=(4, 1)), sg.Text(win_disk_info_free_text, size=(10, 1), key='disk_info_free_text'), sg.Text('total', size=(4, 1)), sg.Text(win_disk_info_total_text, size=(10, 1), key='disk_info_total_text')],
            [sg.ProgressBar(100, orientation='h', size=(33, 10), key='disk_info'), sg.Text(win_disk_info_pct_text, size=(5, 0), key='disk_info_pct')],
    ]

    col2 = [[sg.Text('Board:', size=(10, 1)), sg.Text(board_model(), size=(40,1))],
            [sg.Text('Start:', size=(10, 1)), sg.Text(sys_runstart(), size=(40,1))],
            [sg.Text('Runtime:', size=(10, 1)), sg.Text(sys_runtime(), size=(40, 1), key='sys_runtime')],
            [sg.Text('Distribution:', size=(10, 1)), sg.Text(sys_dist(), size=(40, 1))],
            [sg.Text('Kernel:', size=(10, 1)), sg.Text(sys_kernel(), size=(40, 1))],
            [sg.Text('Firmware:', size=(10, 1)), sg.Text(sys_firmware(), size=(40, 1))],
            [sg.Text('Disk:', size=(10, 1)), sg.Text('read', size=(4, 1)), sg.Text(win_disk_read_text, size=(10, 1), key='disk_read_text'), sg.Text('write', size=(4, 1)), sg.Text(win_disk_write_text, size=(10, 1), key='disk_write_text'), sg.Text('total', size=(4, 1)), sg.Text(win_disk_total_text, size=(10, 1), key='disk_total_text')],
            [sg.Text('Network:', size=(10, 1)), sg.Text('recv', size=(4, 1)), sg.Text(win_net_io_recv_text, size=(10, 1), key='net_io_recv_text'), sg.Text('sent', size=(4, 1)), sg.Text(win_net_io_sent_text, size=(10, 1), key='net_io_sent_text'), sg.Text('total', size=(4, 1)), sg.Text(win_net_io_total_text, size=(10, 1), key='net_io_total_text')],
            [sg.Text('Hostname:', size=(10, 1)), sg.Text(sys_hostname(), size=(15, 1)), sg.Text('Connections:', size=(12, 1)), sg.Text(win_net_conn, size=(5, 1), key='net_conn'), sg.Text('Users:', size=(6, 1)), sg.Text(win_sys_users, size=(4, 1), key='sys_users')],
            [sg.Text('IP LAN:', size=(7, 1)), sg.Text('xxx.xxx.xxx.xxx', size=(10, 1)), sg.Text('IP WLAN:', size=(9, 1)), sg.Text('xxx.xxx.xxx.xxx', size=(10, 1)), sg.Text('IP extern:', size=(8, 1)), sg.Text('xxx.xxx.xxx.xxx', size=(10, 1))],
            [sg.Text('LINE')],
            [sg.Spin(['100', '200', '300', '400', '500', '600', '700', '800', '900'], initial_value='900', key='-spin-'), sg.Text('milliseconds update interval')]
    ]


    ################################
    # ------ GUI Definition ------ #
    ################################

    # layout horizontal
    # layout = [
    #     [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
    #     [sg.Column(col1), sg.VerticalSeparator(pad=(1,5)), sg.Column(col2)],      # horizontal
    # ]

    # layout vertical
    # layout = [
    #     [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
    #       [sg.Column(col1)],      # vertical
    #       [sg.Text('_'*55)],       # seperator
    #       [sg.Column(col2)],      # vertical
    # ]

    # layout tab
    layout = [
        [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
        [sg.TabGroup([[sg.Tab('Status', col1), sg.Tab('Info', col2)]])],
         ]

    window_main = sg.Window("Pi Fusion",
                       layout,
                       default_element_size=(12, 1),
                       default_button_element_size=(12, 1),
                       keep_on_top=True,
                       # grab_anywhere = True
                       )

    # ------ window_main -> layout keys ------ #
    # ------ CPU ------ #
    win_cpu_temp = window_main['cpu_temp']
    win_cpu_temp_text = window_main['cpu_temp_text']
    win_cpu_temp_pct = window_main['cpu_temp_pct']

    win_cpu_load_avg = window_main['cpu_load_avg']
    win_cpu_load_avg_pct = window_main['cpu_load_avg_pct']
    win_cpu_load_avg_1m_text = window_main['cpu_load_avg_1m_text']
    win_cpu_load_avg_5m_text = window_main['cpu_load_avg_5m_text']
    win_cpu_load_avg_15m_text = window_main['cpu_load_avg_15m_text']

    win_cpu_freq = window_main['cpu_freq']
    win_cpu_freq_text = window_main['cpu_freq_text']
    win_cpu_freq_pct = window_main['cpu_freq_pct']

    # ------ Memory ------ #
    win_mem_info = window_main['mem_info']
    win_mem_info_pct = window_main['mem_info_pct']
    win_mem_info_used_text = window_main['mem_info_used_text']
    win_mem_info_free_text = window_main['mem_info_free_text']
    win_mem_info_total_text = window_main['mem_info_total_text']

    # ------ Swap ------ #
    win_mem_swap = window_main['mem_swap']
    win_mem_swap_pct = window_main['mem_swap_pct']
    win_mem_swap_used_text = window_main['mem_swap_used_text']
    win_mem_swap_free_text = window_main['mem_swap_free_text']
    win_mem_swap_total_text = window_main['mem_swap_total_text']

    # ------ Disk ------ #
    win_disk_info = window_main['disk_info']
    win_disk_info_pct = window_main['disk_info_pct']
    win_disk_info_used_text = window_main['disk_info_used_text']
    win_disk_info_free_text = window_main['disk_info_free_text']
    win_disk_info_total_text = window_main['disk_info_total_text']
    win_disk_read_text = window_main['disk_read_text']
    win_disk_write_text = window_main['disk_write_text']
    win_disk_total_text = window_main['disk_total_text']

    # ------ Network ------ #
    win_net_io_sent_text = window_main['net_io_sent_text']
    win_net_io_recv_text = window_main['net_io_recv_text']
    win_net_io_total_text = window_main['net_io_total_text']

    # ------ Other ------ #
    win_sys_runtime = window_main['sys_runtime']
    win_net_conn = window_main['net_conn']
    win_sys_users_online = window_main['sys_users']

    interval = 900      # milliseconds

    ################################
    # ------ Loop & Process ------ #
    ################################
    while True:
        event, values = window_main.read(timeout=interval)
        if event in (None, 'Exit'):
            break

        # print(event, values)
        interval = int(values['-spin-']) * 1    # update interval from -spin- in milliseconds

        ########################
        # ------ Update ------ #
        ########################

        # ------ CPU temperature ------ #
        win_cpu_temp_text.update(cpu_temp()[0])
        win_cpu_temp_pct.update(cpu_temp()[2])
        win_cpu_temp.UpdateBar(cpu_temp()[2])

        # ------ CPU Load average ------ #
        win_cpu_load_avg.UpdateBar(cpu_load_avg_pct()[0])
        win_cpu_load_avg_pct.update(round(cpu_load_avg_pct()[0],1))
        win_cpu_load_avg_1m_text.update(str('1m ') + str(round(cpu_load_avg_pct()[0],2)))
        win_cpu_load_avg_5m_text.update(str('5m ') + str(round(cpu_load_avg_pct()[1], 2)))
        win_cpu_load_avg_15m_text.update(str('15m ') + str(round(cpu_load_avg_pct()[2], 2)))

        # ------ CPU freq ------ #
        win_cpu_freq_text.update(cpu_freq().get('current')[0])
        win_cpu_freq_pct.update(cpu_freq().get('pct')[0])
        win_cpu_freq.UpdateBar(cpu_freq().get('pct')[0])

        # ------ Memory ------ #
        win_mem_info_pct.update(mem_info()['percent'])
        win_mem_info.UpdateBar(mem_info().get('percent'))
        win_mem_info_used_text.update(mem_info().get('used'))
        win_mem_info_free_text.update(mem_info()['free'])
        win_mem_info_total_text.update(mem_info()['total'])

        # ------ Memory Swap ------ #
        win_mem_swap_pct.update(mem_swap()['percent'])
        win_mem_swap.UpdateBar(mem_swap().get('percent'))
        win_mem_swap_used_text.update(mem_swap().get('used'))
        win_mem_swap_free_text.update(mem_swap().get('free'))
        win_mem_swap_total_text.update(mem_swap().get('total'))

        # ------ Disk ------ #
        win_disk_info_pct.update(disk_info()['percent'])
        win_disk_info.UpdateBar(disk_info().get('percent'))
        win_disk_info_used_text.update(disk_info().get('used'))
        win_disk_info_free_text.update(disk_info()['free'])
        win_disk_info_total_text.update(disk_info()['total'])

        # ------ Disk i/o ------ #
        win_disk_read_text.update(disk_io_counters()['read_bytes'])
        win_disk_write_text.update(disk_io_counters()['write_bytes'])
        win_disk_total_text.update(disk_io_counters()['total_bytes'])

        # ------ Network i/o ------ #
        win_net_io_sent_text.update(net_io_counters()['bytes_sent'])
        win_net_io_recv_text.update(net_io_counters()['bytes_recv'])
        win_net_io_total_text.update(net_io_counters()['total_bytes'])

        # ------ Runtime ------ #
        win_sys_runtime.update(sys_runtime())

        # ------ Connections ------ #
        win_net_conn.update(net_connections())

        # ------ Users ------ #
        win_sys_users_online.update(sys_users_online())

        ######################################
        # ------ Process menu choices ------ #
        ######################################

        # ------ Menu choices ------ #
        if event == 'About Pi Fusion':
            window_main.disappear()
            sg.popup('About this program', 'Version 0.10',
                     'Pi Fusion Version', '0.10 dirty',  grab_anywhere=True)
            window_main.reappear()
        elif event == 'Open':
            filename = sg.popup_get_file('file to open', no_window=True)
            print(filename)
        elif event == 'CPU Details':
            window_main.Hide()
            window_cpu_details()
            window_main.UnHide()
        elif event == 'CPU Times':
            window_main.Hide()
            window_cpu_times()
            window_main.UnHide()
        elif event == 'Memory Details':
            window_main.Hide()
            window_memory_details()
            window_main.UnHide()
        elif event == 'GPIO Status':
            window_main.Hide()
            window_gpio_mini()
            window_main.UnHide()
        elif event == 'Partitions Details':
            window_main.Hide()
            window_disk_partitions()
            window_main.UnHide()
        elif event == 'SoC Details':
            window_main.Hide()
            window_soc_details()
            window_main.UnHide()

    window_main.close()

menus()