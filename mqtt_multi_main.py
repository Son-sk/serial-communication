
from mqtt_multi_serial_rx import read_rx
from mqtt_multi_serial_tx import read_tx
from multiprocessing import Process

if __name__ == "__main__":
    p1 = Process(target=read_rx) 
    p2 = Process(target=read_tx) 

    p1.start()
    p2.start()

    p1.join()
    p2.join()