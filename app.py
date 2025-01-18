import sys
import time
import tkinter as tk

from pymodbus.client.serial import *
from tkinter import ttk
from tkinter.constants import *


class ModbusTester(object):
    def protocol_select(self, event):
        if self.protocol.current() == 2:
            self.com.configure(state='disable')
        else:
            self.com.configure(state='readonly')
        return

    def go_func(self):
        print(self.stopbits.get())
        return

    def modbus_read(self):
        try:
            if self.stopbits.get() == '' or self.bytesize.get() == '' or self.parity.get() == '':
                print('There are fields that have not been filled in')
                return
            DEVICE_ID = 1
            client = ModbusSerialClient(
                framer=FramerType(self.protocol.get()), port=self.com.get(), baudrate=int(self.baudrate.get()),
                stopbits=int(self.stopbits.get()), bytesize=int(self.bytesize.get()), parity=self.parity.get(), timeout=1)

            if not client.connect():
                print('Fail to connect to modbus slave')
                return

            while True:
                result = client.read_holding_registers(1, 8, DEVICE_ID)
                try:
                    print(result.registers)
                    self.text.configure(text=result.registers)
                except:
                    print(result.function_code)
                time.sleep(1)
        except Exception as e:
            print(e)
            sys.exit()

    def main(self):
        # create interface
        window = tk.Tk()
        window.title('Modbus Tester')
        window.geometry('500x600')
        window.resizable(False, False)

        protocol_text = tk.Label(text='protocol')
        protocol_text.pack()

        self.protocol = ttk.Combobox(state='readonly', values=[
                                     'rtu', 'ASCII', 'TCP/IP'])
        self.protocol.set('rtu')
        self.protocol.bind('<<ComboboxSelected>>', self.protocol_select)
        self.protocol.pack(fill='x')

        com_text = tk.Label(text='PORT')
        com_text.pack()

        self.com = ttk.Combobox(state='readonly', values=[
                                'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9'])
        self.com.set('COM1')
        self.com.pack(fill='x')

        functionCode_text = tk.Label(text='Function Code')
        functionCode_text.pack()

        self.functionCode = ttk.Combobox(state='readonly', values=[
                                         'Read Holding Registers (03)', 'Read Input Registers (04)'])
        self.functionCode.set('Read Holding Registers (03)')
        self.functionCode.pack(fill='x')

        baudrate_text = tk.Label(text='baudrate')
        baudrate_text.pack()

        self.baudrate = ttk.Combobox(state='readonly', values=[
                                     '1200', '2400', '4800', '9600', '115200', '19200', '38400'])
        self.baudrate.set('9600')
        self.baudrate.pack(fill='x')

        stopbits_text = tk.Label(text='Stopbits')
        stopbits_text.pack()

        self.stopbits = tk.Entry()
        self.stopbits.pack(fill='x')
        # --------------------------------------------#
        bytesize_text = tk.Label(text='Bytesize')
        bytesize_text.pack()

        self.bytesize = tk.Entry()
        self.bytesize.pack(fill='x')

        parity_text = tk.Label(text='Parity')
        parity_text.pack()

        self.parity = tk.Entry()
        self.parity.pack(fill='x')

        go = tk.Button(text='Read', command=self.modbus_read)
        go.pack()

        self.text = tk.Label(text='')
        self.text.pack()

        window.mainloop()


if __name__ == '__main__':
    run = ModbusTester()
    run.main()
