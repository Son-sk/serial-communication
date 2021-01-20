import sys   
import glob   
import serial   
import serial.tools.list_ports

def serial_ports():   

    if sys.platform.startswith('win'):   
        ports = ['COM%s' % (i + 1) for i in range(256)]   
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):   
        # this excludes your current terminal "/dev/tty"   
        ports = glob.glob('/dev/tty[A-Za-z]*')   
    elif sys.platform.startswith('darwin'):   
        ports = glob.glob('/dev/tty.*')   
    else:   
        raise EnvironmentError('Unsupported platform')   

    result = []   
    for port in ports:   
        try:   
            s = serial.Serial(port)   
            #print(s.portstr)
            s.close()   
            result.append(port)   
        except (OSError, serial.SerialException):   
            pass   
    return result   

def serial_check_enable() :
    usb_string = 'Silicon Labs CP210x'
    check_port = []
    check_desc = []

    port1 = 'none'
    port2 = 'none'

    serial_port_wating = serial_ports()
    comlist = serial.tools.list_ports.comports()

    for port, desc, hwid in sorted(comlist):
        print("{}: {} [{}]".format(port, desc, hwid))
        
        check_port.append(format(port))
        check_desc.append(format(desc))
    i =0
    while i < int(len(check_port)) :
        if check_port[i] in serial_port_wating  :
            if usb_string in check_desc[i] and port1 == 'none'  :
                port1 = check_port[i]
            elif usb_string in check_desc[i] :
                port2 = check_port[i]
        i+=1

    if port1 != 'none' :
        print("Available PORT1 : "+str(port1)+" (Automatic connection)")
    else :
        print("Not available PORT1")

    if port2 != 'none' :
        print("Available PORT2 : "+str(port2)+" (Automatic connection)")
    else :
        print("Not available PORT2")

    return port1, port2

port1, port2 = serial_check_enable()

#print(serial_check_enable())

