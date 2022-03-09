#!/usr/bin/env python

import PySimpleGUI as sg
import subprocess
import email_scraper as es


def start_nmap(arguments):
    command_to_run = 'nmap' + arguments
    es.update_output_text(window=my_ui.window, field_to_update='-OUTPUT-',
                          new_text='Running command: ' + command_to_run)
    # sg.popup(command_to_run, keep_on_top=False)
    sp = subprocess.run(command_to_run, shell=True, text=True, capture_output=False)

    # sp = subprocess.Popen(['nmap'] + [arg_string], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    scan_output = sp.stdout

    print(sp)


class UILayout:
    go_button = sg.Button('GO!', bind_return_key=True, key='-GO_BUTTON-')
    cross_tab_layout = [[[sg.Text('Enter target', font='15')], sg.Input(key='-INPUT-', pad=(8, 0), expand_x=False),
                         go_button, sg.Button('Never-mind')]]
    # key must be the same as metadata
    column = [[sg.Checkbox('OS Detection', default=False, auto_size_text=True, key='-O', metadata='-O'),
               sg.Checkbox('OS and version detection', key='-A', metadata='-A'),
               sg.Checkbox('T4', key='-T4', metadata='-T4'),
               sg.Checkbox('Treat all hosts as online', key='-Pn', metadata='-Pn')],
              [sg.Checkbox('Fast mode', key='-F', metadata='-F')]]

    output_column = [[sg.Column([[sg.Text(size=(90, 90), key='-OUTPUT-',
                                          auto_size_text=True, expand_y=True,
                                          expand_x=True)]],
                                scrollable=True, vertical_scroll_only=True, expand_x=True)]]

    scan_tab = [[sg.Column(column)],
                [sg.Button('Scan!', bind_return_key=True, key='-SCAN_BUTTON-')]]  # , [output_column]]
    scrape_tab = [[sg.Button('Scrape emails')]]
    layout = cross_tab_layout
    layout += [[sg.TabGroup([
        [sg.Tab('Scanning (nmap)', scan_tab, key='-SCAN_TAB-')],
        [sg.Tab('Web scraping', scrape_tab, key='-SCRAPE_TAB-')]],
        key='-TAB_GROUP-', enable_events=True)]]
    layout += output_column
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Script Kiddie Toolbox', layout, location=(1050, 300), resizable=True, size=(1000, 550))

    # process-factory.dk


def get_scan_args():
    arg_string = ''
    for i in range(0, len(my_ui.column)):
        for checkbox in my_ui.column[i]:
            if values[checkbox.metadata]:
                arg_string += ' ' + checkbox.metadata
    return arg_string


def change_go_button_text():
    my_text = str(values[event])
    update_text = my_text[1:my_text.find('_')]
    update_text = update_text[0:1] + update_text[1:].lower() + '!'
    print(update_text)
    my_ui.go_button.update(text=update_text)


if __name__ == '__main__':
    my_ui = UILayout()
    while True:
        event, values = my_ui.window.read()
        # print(values[event])
        if event == sg.WINDOW_CLOSED or event == 'Never-mind':
            break
        elif values[event] != '':
            change_go_button_text()
        elif event == 'Scan!' or event == 'Return':
            args = get_scan_args() + ' ' + values['-INPUT-']
            start_nmap(args)
        elif event == 'Scrape emails':
            scrape_me = es.EmailScraper()
            es.EmailScraper.scrape_emails(self=scrape_me, target=values['-INPUT-'], window=my_ui.window)
    my_ui.window.close()
