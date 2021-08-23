#!/usr/bin/env python3

import os

class start_editor():
    def __init__(self, argslist: list):
        self.argslist = argslist

    def args(self, pos=None):
        if pos:
            return self.argslist[pos]
        else:
            return self.argslist

    def start_led(self):
        self.led()

    def __returnval(self, val, pos):
        try:
            return val[pos]
        except IndexError:
            return None

    def write(self, file_name, final_buffer):
        final_buffer_string = '\n'.join(final_buffer)
        write_file = open(file_name, 'w')
        write_file.write(final_buffer_string+'\n')
        write_file.close()

    def read_file(self):
        try:
            file_path: str = self.args(1)
            if file_path:
                if os.path.exists(file_path):
                    fr = open(file_path, 'r')
                    file_content_string = fr.read()
                    fr.close()
                    file_content = file_content_string.split('\n')
                    file_content.pop(len(file_content)-1)
                    return file_content
                else:
                    return []
        except IndexError:
            return []

    def change(self, pos, original_buffer):
        temp_buffer = []
        while(True):
            c = input()
            if c != '~|':
                temp_buffer.append(c)
            else:
                break;

        temp_buffer_string = '\n'.join(temp_buffer)
        original_buffer[pos] = temp_buffer_string
        original_buffer_string = '\n'.join(original_buffer)
        return original_buffer_string.split('\n')


    def led(self):
        try:
            mode: str = 'normal'
            led_buffer: list = self.read_file()
            pos: int = 0

            while(True):
                if mode == 'normal':
                    c = input(f'{mode}> ')
                else:
                    c = input()
            
                cmd = c.split()
                arg = self.__returnval
                if mode == 'normal':
                    if c in [None, '']:
                        pass

                    elif arg(cmd, 0) in ['insert', 'i']:
                        mode = 'insert'

                    elif arg(cmd, 0) in ['change', 'c']:
                        if arg(cmd, 1) and led_buffer[int(arg(cmd, 1))-1]:
                            led_buffer = self.change(int(arg(cmd, 1))-1, led_buffer)
                        else:
                            print('Error')

                    elif arg(cmd, 0) in ['print', 'p']:
                        for x in led_buffer:
                            print(x)

                    elif arg(cmd, 0) in ['lineprint', 'n']:
                        for x in range(len(led_buffer)):
                            print(f'{x+1}\t| {led_buffer[x]}')

                    elif arg(cmd, 0) in ['write', 'w']:
                        if arg(cmd, 1):
                            self.write(arg(cmd, 1), led_buffer)
                        elif self.args(1):
                            self.write(self.args(1), led_buffer)
                        else:
                            print('Err: Invalid Filename')

                    elif arg(cmd, 0) in ['quit', 'q']:
                        break;

                    else:
                        print(f'Err: Invalid instruction: {arg(cmd, 0)}')

                elif mode == 'insert':
                    if c != '~|':
                        led_buffer.append(c)
                        pos+=1

                    else:
                        mode = 'normal'
        except EOFError:
            pass