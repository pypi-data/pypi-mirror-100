

# from rpa.core import *
# from rpa.utils import *
# import rpa3 as rpa # 使用V3引擎

import pywinio
import time
import atexit
# KeyBoard Commands
# Command port
KBC_KEY_CMD = 0x64
# Data port
KBC_KEY_DATA = 0x60
g_winio = None
WordDict = {'a': 0x1e, 'b': 0x30, 'c': 0x2e, 'd': 0x20, 'e': 0x12, 'f': 0x21,
            'g': 0x22, 'h': 0x23, 'i': 0x17, 'j': 0x24, 'k': 0x25, 'l': 0x26,
            'm': 0x32, 'n': 0x31, 'o': 0x18, 'p': 0x19, 'q': 0x10, 'r': 0x13,
            's': 0x1f, 't': 0x14, 'u': 0x16, 'v': 0x2f, 'w': 0x11, 'x': 0x2d,
            'y': 0x15, 'z': 0x2c, '0': 0x0b, '1': 0x02, '2': 0x03, '3': 0x04,
            '4': 0x05, '5': 0x06, '6': 0x07, '7': 0x08, '8': 0x09, '9': 0x0a,
            '!': 0x02, '"': 0x28, '#': 0x04, '$': 0x05, '%': 0x06, '&': 0x08,
            '\'':0x28, '(': 0x0a, ')': 0x0b, '*': 0x09, '+': 0x0d, ',': 0x33,
            '-': 0x0c, '.': 0x34, '/': 0x35, ':': 0x27, ';': 0x27, '<': 0x33,
            '=': 0x0d, '>': 0x34, '?': 0x35, '@': 0x03, '[': 0x1a,']': 0x1b,
            '^': 0x07, '_': 0x0c, '`': 0x29, '{': 0x1a, '|': 0x2b,'}': 0x1b,
            '~': 0x29, 'caps_lock': 0x3A,'shift':0x36}

def get_winio():
    global g_winio
    if g_winio is None:
            g_winio = pywinio.WinIO()
            def __clear_winio():
                    global g_winio
                    g_winio = None
            atexit.register(__clear_winio)
    return g_winio

def wait_for_buffer_empty():
    '''
    Wait wio-keyboard buffer empty
    '''
    winio = get_winio()
    dwRegVal = 0x02
    while (dwRegVal & 0x02):
            dwRegVal = winio.get_port_byte(KBC_KEY_CMD)

def key_down(scancode):
    winio = get_winio()
    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_DATA, scancode)

def key_up(scancode):
    winio = get_winio()
    wait_for_buffer_empty()
    winio.set_port_byte( KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte( KBC_KEY_DATA, scancode | 0x80)

def key_press(scancode, press_time = 0.2):
    key_down(scancode)
    time.sleep(press_time)
    key_up(scancode)

def key_input(str_keys):
    for str_key in str(str_keys):
        try:
            if str_key in list(WordDict.keys()):
                key_press(WordDict[str_key])
            else:
                print('您的输入有误')
        except Exception as e:
            print('你的输入有误',e)

