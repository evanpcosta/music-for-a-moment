import threading
import PySimpleGUI as sg
import queue
import db
import listener
import multiprocessing
from listener import listener as L
from db import database, corpus_generator

"""
    Threading Demo - "Call popup from a thread"

    Can be extended to call any PySimpleGUI function by passing the function through the queue


    Safest approach to threading is to use a Queue object to communicate
    between threads and maintrhead.

    The thread calls popup, a LOCAL function that should be called with the same
    parameters that would be used to call opiup when called directly

    The parameters passed to the local popup are passed through a queue to the main thread.
    When a messages is received from the queue, sg.popup is called using the parms passed
    through the queue

    Copyright 2021 PySimpleGUI.org
"""

mainthread_queue: multiprocessing.Queue = None


def popup(*args, **kwargs):
    if mainthread_queue:
        mainthread_queue.put((args, kwargs))


def download_thread(url):
    """
    The thread that communicates with the application through the window's events.

    Once a second wakes and sends a new event and associated value to the window
    """
    print('----- We are making your music bank! This may take a few minutes... ----- \n')
    download_status = corpus_generator.generate_corpus(url)
    print('\n')
    if download_status:
        print('----- Download Successful -----')
    else:
        print('Download Failed')

def start_listening():
    """
    The thread that communicates with the application through the window's events.

    Once a second wakes and sends a new event and associated value to the window
    """
    L.listener()

def process_popup():
    try:
        queued_value = mainthread_queue.get_nowait()
        sg.popup_auto_close(*queued_value[0], **queued_value[1])
    except queue.Empty:  # get_nowait() will get exception when Queue is empty
        pass


def main():
    """
    The demo will display in the multiline info about the event and values dictionary as it is being
    returned from window.read()
    Every time "Start" is clicked a new thread is started
    Try clicking "Dummy" to see that the window is active while the thread stuff is happening in the background
    """
    global mainthread_queue

    mainthread_queue = multiprocessing.Queue()

    layout = [[sg.Text('Log', font='Any 15')],
              [sg.Multiline(size=(65, 20), key='-ML-', autoscroll=True, reroute_stdout=True, write_only=True,
                            reroute_cprint=True)],
              [sg.T('Please enter URL to Youtube Playlist')],
              [sg.Input(key='-URL-', size=(30, 1))],
              [sg.B('Download Music'), sg.B('Start Listening'), sg.B('Stop Listening'), sg.Button('Exit')]]

    window = sg.Window('Music For The Moment', layout, finalize=True, keep_on_top=True)
    threads = []
    while True:  # Event Loop
        event, values = window.read(timeout=500)
        # sg.cprint(event, values) if event != sg.TIMEOUT_EVENT else None
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        process_popup()
        if event.startswith('Download Music'):
            multiprocessing.Process(target=download_thread, args=(values['-URL-'],), daemon=True).start()
        if event.startswith('Start Listening'):
            if not len(threads):
                print('----- Listening -----\n')
                threads.append(multiprocessing.Process(target=start_listening, args=(), daemon=True))
                threads[0].start()
        if event.startswith('Stop Listening'):
            if len(threads):
                print('----- Stopped Listening -----\n')
                threads[0].kill()
                threads.pop(0)

    window.close()


if __name__ == '__main__':
    main()