import PySimpleGUI as sg
from src.collector import *

#####################
# ------ CPU ------ #
#####################

def window_cpu_details():
    # A list of the keys of dictionary
    # list_keys = [k for k in dict]

    # or a list of the values
    # list_values = [v for v in dict.values()]

    # or just a list of the list of key value pairs
    # list_key_value = [[k, v] for k, v in dict.items()]

    # dict = {'a': 1, 'b': 2, 'c': 3}
    # dict_list = []
    # for i, j in dict.iteritems():
    #    dict_list.append((i, j))
    # print(dict_list)

    # Converting into list of tuple
    # list = [(k, v) for k, v in dict.items()]

    # Converting into list of tuple
    # list = list(dict.items())

    data1 = [(k, v) for k, v in dict.items(cpu_details1())]     # unsorted list of tuples from dict
    data2 = [(k, v) for k, v in dict.items(cpu_details2())]     # unsorted list of tuples from dict
    data3 = [(k, v) for k, v in dict.items(cpu_stats())]     # unsorted list of tuples from dict
    data_info = sorted(data1 + data2 + data3)    # sorted list of tuples from dicts
    data_times = sorted([(k, v) for k, v in dict.items(cpu_times())])  # sorted list of tuples from dict

    frame_cpu_info = [[sg.Table(
                key='table_cpu_info',
                pad=(10,10),
                # col_widths=40,
                # def_col_width=40,
                values=data_info,
                headings= ['Feature','Value'],
                auto_size_columns=True,
                justification='left',
                num_rows=min(len(data_info), 25),
                enable_events=False)],
                ]

    frame_cpu_times = [[sg.Table(
                key='table_cpu_times',
                pad=(10, 10),
                # col_widths=40,
                # def_col_width=40,
                values=data_times,
                headings=['Feature', 'Time'],
                auto_size_columns=True,
                justification='left',
                num_rows=min(len(data_times), 20),
                enable_events=False)],
                ]

    layout = [[sg.Frame('CPU Info', frame_cpu_info), sg.Frame('CPU Times', frame_cpu_times)],
              # [sg.T('1')],
              [sg.OK()]]

    window = sg.Window('CPU Details', layout, element_padding=(10, 10), keep_on_top=True, auto_size_buttons=True,
                       force_toplevel=True)
    event, values = window.read()
    window.close()

#####################
# ------ SoC ------ #
#####################

def window_soc_details():

    data_clocks = sorted([(k, v) for k, v in dict.items(soc_clocks())])     # sorted list of tuples from dict
    data_codecs = sorted([(k, v) for k, v in dict.items(soc_codecs())])     # sorted list of tuples from dict
    data_config = sorted([(k, v) for k, v in dict.items(soc_config())])     # sorted list of tuples from dict
    data_volts = sorted([(k, v) for k, v in dict.items(soc_volts())])       # sorted list of tuples from dict

    frame_soc_clocks = [
                        #[sg.T('SoC clock frequencies')],
                        [sg.Table(
                            key='table_soc_clocks',
                            pad=(10, 10),
                            # col_widths=40,
                            # def_col_width=40,
                            values=data_clocks,
                            headings=['Clock', 'Value'],
                            auto_size_columns=True,
                            justification='left',
                            num_rows=min(len(data_clocks), 20),
                            enable_events=False)],
                        ]
    frame_soc_codecs = [
                        [sg.Table(
                            key='table_soc_codecs',
                            pad=(10, 10),
                            # col_widths=40,
                            # def_col_width=40,
                            values=data_codecs,
                            headings=['Codec', 'Value'],
                            auto_size_columns=True,
                            justification='left',
                            num_rows=min(len(data_codecs), 20),
                            enable_events=False)],
                        ]
    frame_soc_config = [
                        [sg.Table(
                            key='table_soc_config',
                            pad=(10, 10),
                            # col_widths=40,
                            # def_col_width=40,
                            values=data_config,
                            headings=['Feature', 'int Value'],
                            auto_size_columns=True,
                            justification='left',
                            num_rows=min(len(data_config), 17),
                            enable_events=False)],
                        ]

    frame_soc_volts = [
                        [sg.Table(
                            key='table_soc_volts',
                            pad=(10, 10),
                            # col_widths=40,
                            # def_col_width=40,
                            values=data_volts,
                            headings=['Feature', 'Volt'],
                            auto_size_columns=True,
                            justification='left',
                            num_rows=min(len(data_volts), 20),
                            enable_events=False)],
                        ]

    layout = [ [sg.Frame('SoC Config', frame_soc_config), sg.Frame('SoC Codecs', frame_soc_codecs), sg.Frame('SoC Clock Frequencies', frame_soc_clocks), sg.Frame('SoC Volts', frame_soc_volts)],
               #[sg.T('1')],
                [sg.OK()]]

    window = sg.Window('SoC Details', layout, element_padding=(10,10), keep_on_top=True, auto_size_buttons=True, force_toplevel=True)
    event, values = window.read()
    window.close()

########################
# ------ Memory ------ #
########################

def window_memory_details():

    data_meminfo = [(k, v) for k, v in dict.items(mem_meminfo())]  # unsorted list of tuples from dict
    data_usage = mem_usage()  # unsorted list of tuples from list

    frame_mem_meminfo = [[sg.Table(
                key='table_mem_meminfo',
                pad=(10,10),
                # col_widths=40,
                # def_col_width=40,
                values=data_meminfo,
                headings= ['Feature','Size'],
                auto_size_columns=True,
                justification='left',
                num_rows=min(len(data_meminfo), 25),
                enable_events=False)],
                ]

    frame_mem_usage = [[sg.Table(
                key='table_mem_usage',
                pad=(10,10),
                # col_widths=40,
                # def_col_width=40,
                values=data_usage,
                headings= ['Mem %','PID','User','Command'],
                auto_size_columns=True,
                justification='left',
                num_rows=min(len(data_usage), 25),
                enable_events=False)],
                ]

    layout = [[sg.Frame('Memory Info', frame_mem_meminfo), sg.Frame('Memory Usage', frame_mem_usage)],
              # [sg.T('1')],
              [sg.OK()]]

    window = sg.Window('Memory Details', layout, element_padding=(10, 10), keep_on_top=True, auto_size_buttons=True,
                       force_toplevel=True)
    event, values = window.read()
    window.close()

######################
# ------ Disk ------ #
######################

def window_disk_partitions():

    data_partitions = sorted(disk_partitions())     # sorted list

    layout = [[sg.Table(
        key='table_disk_partitions',
        pad=(10, 10),
        # col_widths=40,
        # def_col_width=40,
        values=data_partitions,
        alternating_row_color='blue',
        headings=['Partition', 'Name', 'Free %', 'Type', 'Mountpoint', 'Options', 'Size' ],
        auto_size_columns=True,
        justification='left',
        num_rows=min(len(data_partitions), 30),
        enable_events=False)],
        [sg.OK()]]

    window = sg.Window('Disk Partitions Details', layout, element_padding=(10, 10), keep_on_top=True,
                       auto_size_buttons=True, force_toplevel=True)
    event, values = window.read()
    window.close()


######################
# ------ GPIO ------ #
######################

def window_gpio_mini():

    ###################################
    # ------ Column Definition ------ #
    ###################################

    # col1 = [[sg.Text('CPU temp',size=(9,1)), sg.Text(win_cpu_temp_text, size=(5, 1), key='cpu_temp_text'), sg.Text('°C of max.', size=(9, 1)), sg.Text(win_cpu_temp_max, size=(5, 1))],
    #         [sg.ProgressBar(100, orientation='h', size=(33, 10), key='cpu_temp'), sg.Text(win_cpu_temp_pct, size=(5, 1), key='cpu_temp_pct' )],
    #         [sg.Text('CPU load avg', size=(12, 1)), sg.Text(win_cpu_load_avg_1m_text, size=(10, 1), key='cpu_load_avg_1m_text'), sg.Text(win_cpu_load_avg_5m_text , size=(10, 1), key='cpu_load_avg_5m_text'), sg.Text(win_cpu_load_avg_15m_text , size=(10, 1), key='cpu_load_avg_15m_text')],
    #         [sg.ProgressBar(100, orientation='h', size=(33, 10), key='cpu_load_avg'), sg.Text(win_cpu_load_avg_pct, size=(5, 0), key='cpu_load_avg_pct')],
    #         [sg.Text('CPU MHz', size=(9, 1)), sg.Text(win_cpu_freq_text, size=(6, 1), key='cpu_freq_text'), sg.Text('of max.', size=(6, 1)), sg.Text(win_cpu_freq_max)],
    #         [sg.ProgressBar(100, orientation='h', size=(33, 10), key='cpu_freq'), sg.Text(win_cpu_freq_pct, size=(5, 0), key='cpu_freq_pct')],
    #         [sg.Text('RAM', size=(6, 1)), sg.Text('used', size=(4, 1)), sg.Text(win_mem_info_used_text, size=(10, 1), key='mem_info_used_text'), sg.Text('free', size=(4, 1)), sg.Text(win_mem_info_free_text, size=(10, 1), key='mem_info_free_text'), sg.Text('total', size=(4, 1)), sg.Text(win_mem_info_total_text, size=(10, 1), key='mem_info_total_text')],
    #         [sg.ProgressBar(100, orientation='h', size=(33, 10), key='mem_info'), sg.Text(win_mem_swap_pct, size=(5, 0), key='mem_info_pct')],
    #         [sg.Text('SWAP', size=(6, 1)), sg.Text('used', size=(4, 1)), sg.Text(win_mem_info_used_text, size=(10, 1), key='mem_swap_used_text'), sg.Text('free', size=(4, 1)), sg.Text(win_mem_swap_free_text, size=(10, 1), key='mem_swap_free_text'), sg.Text('total', size=(4, 1)), sg.Text(win_mem_swap_total_text, size=(10, 1), key='mem_swap_total_text')],
    #         [sg.ProgressBar(100, orientation='h', size=(33, 10), key='mem_swap'), sg.Text(win_mem_swap_pct, size=(5, 0), key='mem_swap_pct')],
    #         [sg.Text('DISK /', size=(6, 1)), sg.Text('used', size=(4, 1)), sg.Text(win_disk_info_used_text, size=(10, 1), key='disk_info_used_text'), sg.Text('free', size=(4, 1)), sg.Text(win_disk_info_free_text, size=(10, 1), key='disk_info_free_text'), sg.Text('total', size=(4, 1)), sg.Text(win_disk_info_total_text, size=(10, 1), key='disk_info_total_text')],
    #         [sg.ProgressBar(100, orientation='h', size=(33, 10), key='disk_info'), sg.Text(win_disk_info_pct_text, size=(5, 0), key='disk_info_pct')],
    # ]

    col1 = [
            [sg.Text('BCM', size=(4, 1)), sg.Text('PIN', size=(4, 1)), sg.Text('PIN', size=(4, 1)), sg.Text('BCM', size=(4, 1)), sg.Text('State', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('1', size=(4, 1)), sg.Text('2', size=(4, 1)), sg.Text('BCM', size=(4, 1)), sg.Text('', size=(1, 1)), sg.Text(' ', background_color='red',size=(2, 1)), sg.Text('', size=(1, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('3', size=(4, 1)), sg.Text('4', size=(4, 1)), sg.Text('BCM', size=(4, 1)), sg.Text('', size=(1, 1)), sg.Text(' ', background_color='green',size=(2, 1)), sg.Text('', size=(1, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('5', size=(4, 1)), sg.Text('6', size=(4, 1)), sg.Text('BCM', size=(4, 1)), sg.Text('', size=(1, 1)), sg.Text(' ', background_color='yellow',size=(2, 1)), sg.Text('', size=(1, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('7', size=(4, 1)), sg.Text('8', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('9', size=(4, 1)), sg.Text('10', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('11', size=(4, 1)), sg.Text('12', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('13', size=(4, 1)), sg.Text('14', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('15', size=(4, 1)), sg.Text('16', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('17', size=(4, 1)), sg.Text('18', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('19', size=(4, 1)), sg.Text('20', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('21', size=(4, 1)), sg.Text('22', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('23', size=(4, 1)), sg.Text('24', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('25', size=(4, 1)), sg.Text('26', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('27', size=(4, 1)), sg.Text('28', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('29', size=(4, 1)), sg.Text('30', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('31', size=(4, 1)), sg.Text('32', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('33', size=(4, 1)), sg.Text('34', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('35', size=(4, 1)), sg.Text('36', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('37', size=(4, 1)), sg.Text('38', size=(4, 1)), sg.Text('BCM', size=(4, 1))],
        [sg.Text('BCM', size=(4, 1)), sg.Text('39', size=(4, 1)), sg.Text('40', size=(4, 1)), sg.Text('BCM', size=(4, 1))],



            ]

    col2 = [[sg.Text('PIN'),sg.Text('BCM')],
            [sg.Button('10', disabled=True, enable_events=False, button_color=('white', 'red'), size=(1, 1), key='led1', pad=(0, 0)), sg.Button('1', disabled=True, enable_events=False, button_color=('white', 'green'), size=(1, 1), key='led1', pad=(0, 0))],

            ]

    # col2 = [[sg.Text('Board:', size=(10, 1)), sg.Text(board_model(), size=(40,1))],
    #         [sg.Text('Start:', size=(10, 1)), sg.Text(sys_runstart(), size=(40,1))],
    #         [sg.Text('Runtime:', size=(10, 1)), sg.Text(sys_runtime(), size=(40, 1), key='sys_runtime')],
    #         [sg.Text('Distribution:', size=(10, 1)), sg.Text(sys_dist(), size=(40, 1))],
    #         [sg.Text('Kernel:', size=(10, 1)), sg.Text(sys_kernel(), size=(40, 1))],
    #         [sg.Text('Firmware:', size=(10, 1)), sg.Text(sys_firmware(), size=(40, 1))],
    #         [sg.Text('Disk:', size=(10, 1)), sg.Text('read', size=(4, 1)), sg.Text(win_disk_read_text, size=(10, 1), key='disk_read_text'), sg.Text('write', size=(4, 1)), sg.Text(win_disk_write_text, size=(10, 1), key='disk_write_text'), sg.Text('total', size=(4, 1)), sg.Text(win_disk_total_text, size=(10, 1), key='disk_total_text')],
    #         [sg.Text('Network:', size=(10, 1)), sg.Text('recv', size=(4, 1)), sg.Text(win_net_io_recv_text, size=(10, 1), key='net_io_recv_text'), sg.Text('sent', size=(4, 1)), sg.Text(win_net_io_sent_text, size=(10, 1), key='net_io_sent_text'), sg.Text('total', size=(4, 1)), sg.Text(win_net_io_total_text, size=(10, 1), key='net_io_total_text')],
    #         [sg.Text('Hostname:', size=(10, 1)), sg.Text(sys_hostname(), size=(15, 1)), sg.Text('Connections:', size=(12, 1)), sg.Text(win_net_conn, size=(5, 1), key='net_conn'), sg.Text('Users:', size=(6, 1)), sg.Text(win_sys_users, size=(4, 1), key='sys_users')],
    #         [sg.Text('IP LAN:', size=(7, 1)), sg.Text('xxx.xxx.xxx.xxx', size=(10, 1)), sg.Text('IP WLAN:', size=(9, 1)), sg.Text('xxx.xxx.xxx.xxx', size=(10, 1)), sg.Text('IP extern:', size=(8, 1)), sg.Text('xxx.xxx.xxx.xxx', size=(10, 1))],
    #         [sg.Text('LINE')],
    #         [sg.Spin(['100', '200', '300', '400', '500', '600', '700', '800', '900'], initial_value='900', key='-spin-'), sg.Text('milliseconds update interval')]
    # ]

    # layout horizontal
    layout = [
        # [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
        [sg.Column(col1), sg.VerticalSeparator(pad=(1,1)), sg.Column(col2)],      # horizontal
    ]

    window = sg.Window('GPIO Control Mini', layout, default_element_size=(12, 1), default_button_element_size = (12, 1), keep_on_top=True, force_toplevel=True)
    event, values = window.read()
    window.close()

    default_element_size = (12, 1),
    default_button_element_size = (12, 1),
    keep_on_top = True,