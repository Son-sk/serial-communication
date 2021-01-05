# -*- coding: cp949 -*-
import serial
from multiprocessing import Process


def read_rx() :
    ser_rx = serial.Serial(port='COM5', baudrate = 19200)
    datachar_rx = ''
    while True :
        data_rx = ser_rx.read()
        data_decode_rx = data_rx.decode('utf-8')

        if data_decode_rx == '\r' :
            datachar_rx += '\r'
            print (datachar_rx)
            datachar_rx = ''
        else :
            datachar_rx += data_decode_rx

def read_tx() :
    ser_tx = serial.Serial(port='COM3', baudrate = 19200)
    datachar_tx = ''
    while True :
        data_tx = ser_tx.read()
        data_decode_tx = data_tx.decode('utf-8')
        if data_decode_tx == '\r' :
            datachar_tx += '\r'
            print (datachar_tx)
            datachar_tx = ''
        else :
            datachar_tx += data_decode_tx

if __name__ == "__main__":
    p1 = Process(target=read_rx) 
    p2 = Process(target=read_tx) 

    p1.start()
    p2.start()

    p1.join()
    p2.join()

