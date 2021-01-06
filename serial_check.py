import sys   
import glob   
import serial   
import serial.tools.list_ports

def serial_ports():   
    """ Lists serial port names   

        :raises EnvironmentError:   
            On unsupported or unknown platforms   
        :returns:   
            A list of the serial ports available on the system   
    """   
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

if __name__ == '__main__':   
    print(serial_ports())   
    comlist = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(comlist):
        print("{}: {} [{}]".format(port, desc, hwid))
    #connected = []
    # for element in comlist :
    #     connected.append(element.device)
    # print("COM port : "+str(connected))





