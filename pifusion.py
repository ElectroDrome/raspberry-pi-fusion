#!/usr/bin python3
import PySimpleGUI as sg

def menus():

    sg.theme('Topanga')
    sg.set_options(element_padding=(0, 0))

    # ------ Menu Definition ------ #
    menu_def = [['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
                ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Monitor'],
                ['&Control'],
                ['&Info'],
                ['&Docs'],
                ['&Toolbar', ['---', 'Command &1', 'Command &2',
                              '---', 'Command &3', 'Command &4']],
                ['&Help', '&About Pi Fusion...'], ]

    right_click_menu = ['Unused', ['Right', '!&Click', '&Menu', 'E&xit', 'Properties']]

    # ------ GUI Defintion ------ #
    layout = [
        [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
        [sg.Text('Right click me for a right click menu example')],
        [sg.Output(size=(80, 20))],
        [sg.ButtonMenu('ButtonMenu',  right_click_menu, key='-BMENU-'), sg.Button('Plain Button')],
        [sg.Text('Status Bar', relief=sg.RELIEF_SUNKEN,
                 size=(80, 1), pad=(0, 3), key='-status-')]
    ]

    window = sg.Window("Pi Fusion Dashboard",
                       layout,
                       default_element_size=(12, 1),
                       default_button_element_size=(12, 1),
                       right_click_menu=right_click_menu)

    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        print(event, values)
        # ------ Process menu choices ------ #
        if event == 'About Pi Fusion...':
            window.disappear()
            sg.popup('About this program', 'Version 0.10',
                     'PySimpleGUI Version', sg.version,  grab_anywhere=True)
            window.reappear()
        elif event == 'Open':
            filename = sg.popup_get_file('file to open', no_window=True)
            print(filename)
        elif event == 'Properties':
            window_gpio()

    window.close()

def window_gpio():

    layout = [[sg.Text('The second form is small \nHere to show that opening a window using a window works')],
              [sg.OK()]]

    window = sg.Window('Second Form', layout)
    event, values = window.read()
    window.close()

menus()