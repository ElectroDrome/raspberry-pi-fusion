import PySimpleGUI as sg
from src.collector import *

# ------ General ------ #
# ------ Board ------ #
# ------ CPU ------ #
# ------ SoC ------ #
# ------ Disk ------ #
# ------ Memory ------ #
# ------ Network ------ #
# ------ System ------ #

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
    data = sorted(data1 + data2 + data3)    # sorted list of tuples from dicts

    layout = [[sg.Table(
                key='table_cpu_info',
                pad=(10,10),
                # col_widths=40,
                # def_col_width=40,
                values=data,
                headings= ['Feature','Value'],
                auto_size_columns=True,
                justification='left',
                num_rows=min(len(data), 30),
                enable_events=False)],
                [sg.OK()]]

    window = sg.Window('CPU details', layout, element_padding=(10,10), keep_on_top=True, auto_size_buttons=True, force_toplevel=True)
    event, values = window.read()
    window.close()

def window_cpu_times():

    data = sorted([(k, v) for k, v in dict.items(cpu_times())])     # sorted list of tuples from dict

    layout = [[sg.Table(
                key='table_cpu_times',
                pad=(10,10),
                # col_widths=40,
                # def_col_width=40,
                values=data,
                headings= ['Feature','Value'],
                auto_size_columns=True,
                justification='left',
                num_rows=min(len(data), 20),
                enable_events=False)],
                [sg.OK()]]

    window = sg.Window('CPU times', layout, element_padding=(10,10), keep_on_top=True, auto_size_buttons=True, force_toplevel=True)
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
               [sg.T('1')],
                [sg.OK()]]

    window = sg.Window('SoC details', layout, element_padding=(10,10), keep_on_top=True, auto_size_buttons=True, force_toplevel=True)
    event, values = window.read()
    window.close()

########################
# ------ Memory ------ #
########################

def window_mem_meminfo():

    data = [(k, v) for k, v in dict.items(mem_meminfo())]     # unsorted list of tuples from dict

    layout = [[sg.Table(
                key='table_mem_meminfo',
                pad=(10,10),
                # col_widths=40,
                # def_col_width=40,
                values=data,
                headings= ['Feature','Value'],
                auto_size_columns=True,
                justification='left',
                num_rows=min(len(data), 30),
                enable_events=False)],
                [sg.OK()]]

    window = sg.Window('Memory Info Details', layout, element_padding=(10,10), keep_on_top=True, auto_size_buttons=True, force_toplevel=True)
    event, values = window.read()
    window.close()
