# -*- coding: cp949 -*-
import serial
import chardet

def read_tx() : #Wi-Fi Module 송신, 온도조절기 수신
    ser_tx = serial.Serial(port='COM3', baudrate = 19200)
    datachar_tx = ''
    try :
        while True :
            data_tx = ser_tx.read()
            encode = chardet.detect(data_tx)
            if encode['encoding'] == 'ascii' :
                data_decode_tx = data_tx.decode('utf-8')
                if data_decode_tx == '\r' :
                    datachar_tx += '\r'
                    print ("Module: "+datachar_tx)
                    datachar_tx = ''
                else :
                    datachar_tx += data_decode_tx
    except KeyboardInterrupt :
        ser_tx.close()
        pass
