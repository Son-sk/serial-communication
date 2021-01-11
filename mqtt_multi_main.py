
from mqtt_multi_serial_rx import read_rx
from serial_check import serial_check_enable
#from mqtt_multi_serial_tx import read_tx
from multiprocessing import Process

# port1 = 'COM9'
# port2 = 'COM5'


if __name__ == "__main__":
    port1, port2 = serial_check_enable()
    
    # port1 = 'COM9'
    # port2 = 'COM5'

    p1 = Process(target=read_rx, args=(port1, )) 
    p2 = Process(target=read_rx, args=(port2, )) 

    p1.start()
    p2.start()

    p1.join()
    p2.join()