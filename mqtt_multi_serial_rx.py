
# -*- coding: cp949 -*-
import serial
import chardet
def read_rx(port_num) : #port No. #Print Port name
    ser = serial.Serial(port=port_num, baudrate = 19200)
    #datalist = []
    datachar = ''
    port_name = ''

    max_val=0
    max_len=0

    mqtt_data_r = 0
    mqtt_data_re = 0
    mqtt_rpc_inf_new = []
    mqtt_rpc_inf_old = []
    change_data = []
    mqtt_data_2byte_adr = [10,  13,  15,  17,  29,  41,  56,  59,  61] #2byte Mqtt data
    mqtt_data_3byte_adr = [21] #3byte Mqtt data
    mqtt_data_12byte_adr = [44] #12byte Mqtt data
    mqtt_data_print_no = {0:"Power", 1:"Trial run", 2:"Heating", 3:"Hot water", 4:"Quick heating", 5:"Pre heating", 6:"Lock", 
                        7:"Indoor-flow mode", 8:"Heating-combustion", 9:"Hotwater-combustion", 10: "Hotwater temperature", 11:"Hotwater temperature flaot", 
                        12:"Heating flow temperature", 13:"Heating Indoor temperature", 14: "Current temperature", 15:"Outing mode", 16:"Error state", 17:"Error code",
                        18:"Eco state", 19:"Water flow state", 20:"Mode state", 21:"Freeze warning", 22:"Freezing buzzer", 23:"setting temperature limit",
                        24:"SW-Power", 25:"SW-Heat", 26:"SW-Hotwater", 27:"SW-Outing", 28:"SW-Mode", 29:"SW-Reservation", 30:"SW-Heat temperature", 31:"SW-Hotwater temperature",
                        32:"Reservation state", 33:"Reservation type", 34:"Reservation info-General", 35:"Reservation info-24H No.", 36:"Reservation info-24H 4-5P",
                        37:"Reset User Information", 38:"Heating Control Information", 39:"Flow heating energy saving", 40:"Indoor Temperatur heating energy saving",
                        41:"Gas usage unit information"
    # mqtt data No.
    }
    mqtt_data_print_exception = [7, 20, 24, 25, 26, 27, 28, 29, 30, 31, 33, 41] #mqtt data value No. (Not On/Off) 
    mqtt_data_sw_on_off_info = [24, 25, 26, 27, 29, 30, 31] #SW Opertaion data No. (value: 0,1,2) (Exclude Data No. 28)
    mqtt_data_print_state = {"off":"OFF", "on":"ON", "flow":"Flow Heat", "indoor":"Indoor Heat", "auto":"Auto Mode", "save":"Save Mode", "m3":"M3", "kg":"Kg" }

    i=0
    try : 
        while True :
            data = ser.read()
            encode = chardet.detect(data)
            
            if encode['encoding'] == 'ascii' :
                data_decode = data.decode('utf-8')
                if data_decode == '\r' :
                    # for j in range(int(len(datalist))) :
                    #     datachar += datalist[j]
                    if datachar == 'AT+NETWORK5E' :
                        port_name = 'MCU: '
                    elif datachar == 'AT+NETOK5B' :
                        port_name = 'Module: '
                    datachar += '\r'
                    print (port_name+datachar)

                    datachar_split = datachar.split('"')
                    #print (datachar_split)
                    if int(len(datachar)) > 100 : 
                        for i in range(int(len(datachar_split))) :
                            if int(len(datachar_split[i])) > max_val:
                                max_val = int(len(datachar_split[i]))
                                max_len = i

                        if int(len(datachar_split[max_len])) > 50 :
                            

                            mqtt_data_r = datachar_split[max_len]

                            if mqtt_data_re != mqtt_data_r :
                                print("-------------------------------")
                                if mqtt_data_re != 0 : 
                                    i=0
                                    while i < int(len(mqtt_data_r)) :
                                        
                                        if i in mqtt_data_2byte_adr :
                                            j = 2               
                                        elif i in mqtt_data_3byte_adr :
                                            j = 3                       
                                        elif i in mqtt_data_12byte_adr  :
                                            j = 12
                                        else:
                                            j = 1
                                        mqtt_rpc_inf_new.append(mqtt_data_r[i:(i+j)])
                                        mqtt_rpc_inf_old.append(mqtt_data_re[i:(i+j)])
                                    
                                        i = i+j
                                else :
                                    print (mqtt_data_r)

                                mqtt_data_re = mqtt_data_r
                                #print(mqtt_data_re)
                                for i in range(int(len(mqtt_rpc_inf_new))) :
                                    if mqtt_rpc_inf_old[i] != mqtt_rpc_inf_new[i] :
                                        change_data.append(i)

                                i=0
                    
                                while i < int(len(change_data)) :

                                    j=0            
                                    while j < int(len(mqtt_rpc_inf_new)) :
                                        int_mqtt_data = int(mqtt_rpc_inf_new[int(change_data[i])],16)
                                        int_change_data = int(change_data[i])
                                        
                                        if int_change_data == j:
                                            if int_change_data in mqtt_data_print_exception :
                                                if int_mqtt_data  == 0 and int_change_data == 7 : # flow mode or indoor mode
                                                    print(mqtt_data_print_state["flow"])
                                                    #file_output_csv(mqtt_data_print_no[j], mqtt_data_print_state["flow"])
                                                elif int_mqtt_data  == 1 and int_change_data == 7 :
                                                    print(mqtt_data_print_state["indoor"])
                                                    #file_output_csv(mqtt_data_print_no[j], mqtt_data_print_state["indoor"])

                                                if int_mqtt_data  == 0 and int_change_data == 20 : # heating mode : auto/save
                                                    print("Mode: "+mqtt_data_print_state["off"])
                                                    #file_output_csv(mqtt_data_print_no[j], mqtt_data_print_state["off"])
                                                elif int_mqtt_data  == 1 and int_change_data == 20 :
                                                    print(mqtt_data_print_state["save"])
                                                    #file_output_csv(mqtt_data_print_no[j], mqtt_data_print_state["save"])
                                                elif int_mqtt_data  == 2 and int_change_data == 20 :
                                                    print(mqtt_data_print_state["auto"])
                                                    #file_output_csv(mqtt_data_print_no[j], mqtt_data_print_state["auto"])

                                                if int_mqtt_data  == 0 and int_change_data in mqtt_data_sw_on_off_info : #SW operation info
                                                    pass
                                                elif int_mqtt_data  == 1 and int_change_data in mqtt_data_sw_on_off_info  :
                                                    print(mqtt_data_print_no[j]+": "+mqtt_data_print_state["on"])
                                                    #file_output_csv(mqtt_data_print_no[j], mqtt_data_print_state["on"])
                                                elif int_mqtt_data  == 2 and int_change_data in mqtt_data_sw_on_off_info  :
                                                    print(mqtt_data_print_no[j]+": "+mqtt_data_print_state["off"])
                                                    #file_output_csv(mqtt_data_print_no[j], mqtt_data_print_state["off"])

                                                if int_mqtt_data  == 0 and int_change_data == 28 : #SW operation info_ heat mode auto/save
                                                    pass
                                                elif int_mqtt_data  == 1 and int_change_data == 28 : 
                                                    print(mqtt_data_print_no[j]+"SAVE: "+mqtt_data_print_state["on"])
                                                    #file_output_csv(mqtt_data_print_no[j]+" SAVE", mqtt_data_print_state["on"])
                                                elif int_mqtt_data  == 2 and int_change_data == 28 :
                                                    print(mqtt_data_print_no[j]+"SAVE: "+mqtt_data_print_state["off"])
                                                    #file_output_csv(mqtt_data_print_no[j]+" SAVE", mqtt_data_print_state["off"])
                                                elif int_mqtt_data  == 3 and int_change_data == 28 :
                                                    print(mqtt_data_print_no[j]+"AUTO: "+mqtt_data_print_state["on"])
                                                    #file_output_csv(mqtt_data_print_no[j]+" AUTO", mqtt_data_print_state["on"])
                                                elif int_mqtt_data  == 4 and int_change_data == 28 :
                                                    print(mqtt_data_print_no[j]+"AUTO: "+mqtt_data_print_state["off"])
                                                    #file_output_csv(mqtt_data_print_no[j]+" AUTO", mqtt_data_print_state["off"])

                                                if int_mqtt_data  == 0 and int_change_data == 41 :
                                                    print(mqtt_data_print_no[j]+": "+mqtt_data_print_state["m3"]) #gas info
                                                    #file_output_csv(mqtt_data_print_no[j], mqtt_data_print_state["m3"])
                                                elif int_mqtt_data  == 1 and int_change_data == 41 :
                                                    print(mqtt_data_print_no[j]+": "+mqtt_data_print_state["kg"])
                                                    #file_output_csv(mqtt_data_print_no[j], mqtt_data_print_state["kg"])

                                            elif int_mqtt_data == 0 :
                                                print(mqtt_data_print_no[j] +": "+mqtt_data_print_state["off"]) 
                                                #file_output_csv(mqtt_data_print_no[j], mqtt_data_print_state["off"])

                                            elif int_mqtt_data  == 1 and int_change_data != 35 : 
                                                print(mqtt_data_print_no[j] +": "+mqtt_data_print_state["on"])
                                                #file_output_csv(mqtt_data_print_no[j], mqtt_data_print_state["on"])

                                            else : #예약DATA를 시간으로 표시
                                                if int_change_data == 36 : # Hex data No. (Reservation info-24H 4-5P)
                                                    
                                                    hex_mqtt_data = hex(int_mqtt_data)
                                                    
                                                    pat4 = mqtt_rpc_inf_new[int(change_data[i])][0:6]
                                                    pat5 = mqtt_rpc_inf_new[int(change_data[i])][6:12]
                                                    print(mqtt_data_print_no[j] +": P4->"+pat4+", "+"P5->"+pat5)

                                                    bin_pat4 = bin(int(pat4,16))
                                                    bin_pat5 = bin(int(pat5,16))
                                                    #print(len(bin_pat4))
                                                    str_zero4 = ''
                                                    str_zero5 = ''

                                                    if len(str(bin_pat4)) != 26 :
                                                        zero4 = 26 - len(str(bin_pat4))
                                                        s=0
                                                        for s in range(zero4) :
                                                            str_zero4 += '0'

                                                    if len(str(bin_pat5)) != 26 :
                                                        zero5 = 26 - len(str(bin_pat5))
                                                        s=0
                                                        for s in range(zero5) :
                                                            str_zero5 += '0'
                                                    
                                                    str_pat4 = str_zero4 + str(bin_pat4)[2:]
                                                    str_pat5 = str_zero5 + str(bin_pat5)[2:]
                                                    #print(str_pat4)
                                                    #print(str_pat5)

                                                    s=0
                                                    hour = 23
                                                    pat4_hour = []
                                                    while len(str_pat4) > s :
                                                        if str_pat4[s] == '1' :
                                                            pat4_hour.append(hour)
                                                        s+=1
                                                        hour-=1

                                                    s=0
                                                    hour = 23
                                                    pat5_hour = []
                                                    while len(str_pat5) > s :
                                                        if str_pat5[s] == '1' :
                                                            pat5_hour.append(hour)
                                                        s+=1
                                                        hour-=1
                                                    
                                                    pat4_hour.sort()
                                                    pat5_hour.sort()
                                                    print("P4:")
                                                    print(pat4_hour)
                                                    print("P5: ")
                                                    print(pat5_hour)

                                                    #file_output_csv(mqtt_data_print_no[j], hex_mqtt_data)

                                                elif int_change_data == 17 : # Hex data No. (Error)
                                                    hex_mqtt_data = hex(int_mqtt_data)
                                                    print(mqtt_data_print_no[j] +": "+str(hex_mqtt_data))
                                                    #file_output_csv(mqtt_data_print_no[j], hex_mqtt_data)

                                                else : #Dec data No.
                                                    print(mqtt_data_print_no[j] +": "+str(int_mqtt_data))
                                                    #file_output_csv(mqtt_data_print_no[j], int_mqtt_data)
                                        j+=1

                                    i+=1

                                print(change_data)
                                
                                #file_output_csv(mqtt_data_re, '')
                                print("-------------------------------")
                            
                            del change_data[0:int(len(change_data))]
                            del mqtt_rpc_inf_old[0:int(len(mqtt_rpc_inf_old))]
                            del mqtt_rpc_inf_new[0:int(len(mqtt_rpc_inf_new))]

                    #del datalist[0:int(len(datalist))]
                    datachar = ''


                else :
                    #datalist.append(data_decode)
                    datachar += data_decode

            

    except KeyboardInterrupt :
        ser.close()
        pass


