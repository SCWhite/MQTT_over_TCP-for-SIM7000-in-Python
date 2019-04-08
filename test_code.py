from time import sleep
import serial

def formatStrToInt(target):
    kit = ""
    for i in range(len(target)):
        temp=ord(target[i])
        temp=hex(temp)[2:]
        kit=kit+str(temp)+" "
        #print(temp,)
    return kit

#this is every field for IAQ project
gps_lat = 25.1933
gps_num = 100
CFPM10 = 0
s_t0 = 25.91
app = "IAQ_TW"
s_lr = 4065
s_l0 = 5696.45
date = "2019-03-21"
s_d2 = 26
s_d0 = 41
s_d1 = 48
fmt_opt = 0
s_lg = 7911
s_h0 = 55
tick = 389.4
s_lb = 7474
s_lc = 19552
device_id ="9C65F9XXXXXX"
s_g8 = 885
ver_format = 3
gps_lon = 121.787
CFPM25 = 0
gps_fix = 1
CFPM10 = 0
ver_app = "5.2b.1"
device = "LinkIt_Smart_7688"
FAKE_GPS = 1
time = "06:53:55"

##A full MQTT publish contain "connect_pack" & "message_package"

#CONN/RL/PLEN/MQIsdp/LVL/FL/KA/CIDLEN/ABCDEF/ULEN/xxxx/PWLEN/xxxxxx
#see more from "mqtt.xlsx"
connect_pack = "10 22 00 06 4D 51 49 73 64 70 03 C2 00 3C 00 06 41 42 43 44 45 46 00 04 78 78 78 78 00 06 78 78 78 78 78 78 " #fix value for now / remember to change


#message_package = add_on + HEX(prifix+publish_pack) + end_line
prifix = "MAPS/IAQ_TW/NBIOT/"+device_id
publish_pack = "|gps_lat="+str(gps_lat)+"|gps_num="+str(gps_num)+"|CFPM10="+str(CFPM10)+"|s_t0="+str(s_t0)+"|app="+app+"|s_lr="+str(s_lr)+"|s_l0="+str(s_l0)+"|date="+date+"|s_d2="+str(s_d2)+"|s_d0="+str(s_d0)+"|s_d1="+str(s_d1)+"|fmt_opt="+str(fmt_opt)+"|s_lg="+str(s_lg)+"|s_h0="+str(s_h0)+"|tick="+str(tick)+"|s_lb="+str(s_lb)+"|s_lc="+str(s_lc)+"|device_id="+device_id+"|s_g8="+str(s_g8)+"|ver_format="+str(ver_format)+"|gps_lon="+str(gps_lon)+"|CFPM2.5="+str(CFPM25)+"|gps_fix="+str(gps_fix)+"|CFPM1.0="+str(CFPM10)+"|ver_app="+ver_app+"|device="+device+"|FAKE_GPS="+str(FAKE_GPS)+"|time="+time
#publish_pack = "|gps_lat=25.1933|gps_num=100|CFPM10=0|s_t0=25.91|app=IAQ_TW|s_lr=4065|s_l0=5696.45|date=2019-03-21|s_d2=26|s_d0=41|s_d1=48|fmt_opt=0|s_lg=7911|s_h0=55|tick=389.4|s_lb=7474|s_lc=19552|device_id=9C65F920C020|s_g8=885|ver_format=3|gps_lon=121.787|CFPM2.5=0|gps_fix=1|CFPM1.0=0|ver_app=5.2b.1|device=LinkIt_Smart_7688|FAKE_GPS=1|time=06:53:55"
#publish_pack = "1234567890"

payload_len = len(prifix+publish_pack) #remember to add tpoic length (2 byte in this case)
payload_len = payload_len + 2

#print("prifix+publish_pack:",prifix+publish_pack)
#print("payload_len:" ,payload_len)


#MQTT Remaining Length calculate
#currently support range 0~16383(1~2 byte)
if(payload_len<128):
    payload_len_hex = hex(payload_len).split('x')[-1]
else:
    a = payload_len % 128
    b = payload_len // 128
    a = hex(a+128).split('x')[-1]
    b = hex(b).split('x')[-1]
    b = b.zfill(2)
    payload_len_hex = str(a) + " " +  str(b)
    #print(payload_len_hex)

a = formatStrToInt(prifix+publish_pack)

#add_on = "30 F0 02 00 1E "
add_on = "30 " + str(payload_len_hex.upper()) +" 00 1E "
                        #please check packege length-> http://indigoo.com/petersblog/?p=263
                        #0x23 will be 2+30+msg_len -> in HEX
#print("add_on:",add_on)
end_line = "1A"

#all_package = connect_pack + add_on + a + end_line
message_package = add_on + a + end_line
print(connect_pack)
print("==========================")
print(message_package.upper())

##About sending AT command
#
ser=serial.Serial("COM16",57600,timeout=0.5)

ser.write("AT+CIPCLOSE\r".encode())
sleep(1)
data = ser.readline()
print(data)

ser.write("AT+CIPSENDHEX=1\r\n".encode())
sleep(1)
data = ser.readline()
print(data)


ser.write("AT+CSTT=\"nbiot\"\r\n".encode())
sleep(1)
data = ser.readline()
print(data)

ser.write("AT+CIICR\r\n".encode())
sleep(1)
data = ser.readline()
print(data)

ser.write("AT+CIFSR\r\n".encode())
sleep(1)
data = ser.readline()
print(data)

ser.write("AT+CIPSTART=\"TCP\",\"IP.ADD.RE.SS\",\"port\"\r\n".encode())
sleep(1)
data = ser.readline()
print(data)
data = ser.readline()
print(data)
data = ser.readline()
print(data)
data = ser.readline()
print(data)

ser.write("AT+CIPSEND\r\n".encode())
sleep(1)
data = ser.readline()
print(data)

ser.write(connect_pack.encode())
#ser.write("\r\n".encode())
sleep(1)
#data = ser.readline()
#print(data)

ser.write(message_package.upper().encode())
#ser.write("\r\n".encode())
sleep(1)
data = ser.readline()
print(data)

ser.write("AT+CIPCLOSE\r\n".encode())
sleep(1)
data = ser.readline()
print(data)

ser.close()

print("OK!!!")
