#import gpsd
import threading
import time
import sys
import serial

from datetime import datetime,tzinfo,timedelta
from datetime import datetime
from dateutil import tz
import pdb



class GPS:
    def __init__(self, dialog, host="127.0.0.1", port=2947, interval = 0.1):
        
        self.interval = interval
        self.position = None
        
        self.dialog = dialog
        self.rtkFlag = False
        self.ser = None
        self.gGPSCurrentUTCDate = None
    
    def run(self):
        thread = threading.Thread(target=self.thread_function)
        thread.start()
        
        
        
    def funcDecodeRTKDatestr(self, rtkstring):
       
    
        temp1 = rtkstring.split("$GNRMC")
        strDate = ''
        temp = temp1[1].split(',')
        

        
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Australia/Adelaide')
        
        tempDate = temp[9]

        strDate = tempDate[4] + tempDate[5] + tempDate[2]+tempDate[3] +tempDate[0]+tempDate[1] +'_'+temp[1]


        getTime = '20'+tempDate[4:6:]+'-'+tempDate[2:4:]+'-'+tempDate[0:2:]+' '+temp[1][0:2:] +':'+temp[1][2:4:]+':'+temp[1][4:6:]
        
        t = datetime.strptime(getTime,'%Y-%m-%d %H:%M:%S')
        

        
        t = t.replace(tzinfo=from_zone)
        self.gGPSCurrentUTCDate = t.astimezone(from_zone).strftime('%Y:%m:%d ')

        
        gpsDateTime = t.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S')
        self.dialog.setDateTime(t)
        
        return gpsDateTime
        
    def funcDecodeRTKstr(self, rtkstring):
        
        tempLon = ''
        tempLat = ''
        
        strRTK = ''
        temp = rtkstring.split(',')

        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Australia/Adelaide')

        if (len(temp) ==15 and len(temp[1]) != 0):
            
           
            gGPSAltitude = temp[9] # update altitude 

            
            getTime = self.gGPSCurrentUTCDate.replace(':','-') + temp[1][0:2:] +':'+temp[1][2:4:]+':'+temp[1][4:6:]
            t = datetime.strptime(getTime,'%Y-%m-%d %H:%M:%S')


            t = t.replace(tzinfo=from_zone)
            gGPSCurrentUTCTime = t.astimezone(to_zone).strftime('%Y:%m:%d %H:%M:%S')
            strSentingUTCDate = t.astimezone(to_zone).strftime('%Y%m%d%H%M%S')


            if (len(temp[2].split('.')[0]) == 5):

                tempLat = tempLat+ temp[2][0:3:]+'.0'
                tempLat = str(float(tempLat) + (float(temp[2][3:len(temp[2])])/60.0))

            else:
                tempLat = tempLat+temp[2][0:2:]+'.0'
                tempLat = str(float(tempLat) + (float(temp[2][2:len(temp[2])])/60.0))
            
            if (temp[3] == 'S'):
                tempLat = '-' + tempLat
            

            
            if (len(temp[4].split('.')[0]) == 5):

                tempLon = tempLon+ temp[4][0:3:]+'.0'
                tempLon = str(float(tempLon) + (float(temp[4][3:len(temp[4])])/60.0))

            else:
                tempLon = tempLon+temp[2][0:2:]+'.0'
                tempLon = str(float(tempLon) + (float(temp[4][2:len(temp[4])])/60.0))
            
            if (temp[5] =='W'):
                tempLon = '-' + tempLon


            gGPSLat = tempLat
            gGPSLon = tempLon
            print(gGPSLat)
            print(gGPSLon)
            self.dialog.setGps(gGPSLat, gGPSLon)

        else:
            strRTK = "GPS_FAILURE"

        return strRTK

        
    def funcInitRTKSerialPort(self):

        self.ser = serial.Serial()
        self.ser.port = "/dev/ttyACM0"
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.ser.parity = serial.PARITY_NONE #set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
            #ser.timeout = None          #block read
        self.ser.timeout = 5               #non-block read
            #ser.timeout = 2              #timeout block read
        self.ser.xonxoff = True     #disable software flow control
        self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control

        try: 
            self.ser.open()
            print ("RTK PORT SUCCEES: ")
        except (Exception):
            print ("error open serial port: ")
            gCurrentDebugMsg = "RTK DEVICE FAILURE, CHECK DEVICE AND REBOOT SYSTEM."
            print(gCurrentDebugMsg)
        
        
        
    def thread_function(self):
            
        while(True):
            try:
                currentline = self.ser.readline()
            except:
                
                self.funcInitRTKSerialPort()
                continue  
            
            currentline.decode('latin-1')
            currentline = str(currentline)
            
            if str("$GNGGA") in currentline:
                

                self.funcDecodeRTKstr(currentline)
            if str("$GNRMC") in currentline:

                temp1 = currentline.split("$GNRMC")
                temp = temp1[1].split(',')
                tempDate = temp[9]
                if (len(tempDate) == 0):
                    continue
                gCurrentDate = self.funcDecodeRTKDatestr(currentline)
                print(gCurrentDate)
                
                
            time.sleep(self.interval)
                
            
            


                

#gps = GPS(None)
#gps.run()
