# -*- coding: cp949 -*-
import serial


ser = serial.Serial(port='COM5', baudrate = 19200)
datalist = []
datachar = ''
max_val=0
max_len=0
i=0
try : 
    while True :
        data = ser.read()
        data_decode = data.decode('utf-8')
        
        if data_decode == '\r' :
            for j in range(int(len(datalist))) :
                datachar += datalist[j]
            datachar += '\r'
            print (datachar)

            datachar_split = datachar.split('"')
            #print (datachar_split)
            if int(len(datachar)) > 100 : 
                for i in range(int(len(datachar_split))) :
                    if int(len(datachar_split[i])) > max_val:
                        max_val = int(len(datachar_split[i]))
                        max_len = i

                print (datachar_split[max_len])

            del datalist[0:int(len(datalist))]
            datachar = ''


        else :
            datalist.append(data_decode)

except KeyboardInterrupt :
    ser.close()
    pass