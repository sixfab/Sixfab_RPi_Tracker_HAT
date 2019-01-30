'''
  Sixfab_RPi_GPRSIoT_HAT 
  -
  Library for Sixfab RPi GPRSIoT HAT.
  -
  Created by Yasin Kaya (selengalp), January 2, 2019.
'''

import time
import serial
import RPi.GPIO as GPIO
import pigpio
import os

# Peripheral Pin Definations
USER_BUTTON = 6
USER_LED = 5
ENABLE = 17
POWERKEY = 24 
STATUS = 23
L96_RESET = 18
L96_STANDBY = 20
PPS_PIN = 26
L96_SOFT_RX = 27
L96_SOFT_TX = 22

os.system("sudo pgpiod") 

pigpio.pi()
L96_SERIAL = pigpio.pi()
L96_SERIAL.set_mode(L96_SOFT_RX,pigpio.INPUT)
L96_SERIAL.set_mode(L96_SOFT_TX,pigpio.OUTPUT)

L96_SERIAL.bb_serial_read_open(L96_SOFT_RX,9600,8)

# global variables
TIMEOUT = 3 # seconds
ser = serial.Serial()


###########################################
### Private Methods #######################
###########################################

# Function for printing debug message 
def debug_print(message):
	print(message)

# Function for getting time as miliseconds
def millis():
	return int(time.time())

# Function for delay as miliseconds
def delay(ms):
	time.sleep(float(ms/1000.0))


###########################################
### Cellular IoT App HAT Class #############
###########################################

class GPRSIoT:
	board = "" # HAT name (Cellular IoT or Cellular IoT App.)
	ip_address = "" # ip address       
	domain_name = "" # domain name   
	port_number = "" # port number 
	timeout = TIMEOUT # default timeout for function and methods on this library.
	
	response = "" # variable for modem self.responses
	compose = "" # variable for command self.composes

	# Special Characters
	CTRL_Z = '\x1A'
	
	# Initializer function
	def __init__(self, serial_port="/dev/ttyS0", serial_baudrate=115200, board="Sixfab Raspberry Pi Cellular IoT HAT"):
		
		self.board = board
    	
		ser.port = serial_port
		ser.baudrate = serial_baudrate
		ser.parity=serial.PARITY_NONE
		ser.stopbits=serial.STOPBITS_ONE
		ser.bytesize=serial.EIGHTBITS
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(ENABLE, GPIO.OUT)
		GPIO.setup(POWERKEY, GPIO.OUT)
		GPIO.setup(L96_RESET, GPIO.OUT)
		GPIO.setup(L96_STANDBY, GPIO.OUT)
		GPIO.setup(STATUS, GPIO.IN)
		GPIO.setup(PPS_PIN, GPIO.IN)
			
		debug_print(self.board + " Class initialized!")
 	
 	# Function for clearing global compose variable 
	def clear_compose(self):
		self.compose = ""

	# Function for enable M95 module
	def enable(self):
		GPIO.output(ENABLE,0)
		debug_print("M95 module enabled!")

	# Function for powering down M95 module and all peripherals from voltage regulator 
	def disable(self):
		GPIO.output(ENABLE,1)
		debug_print("M95 module disabled!")

	# Function for powering up or down M95 module
	def powerUp(self):
		if(self.getModemStatus()):
			GPIO.output(POWERKEY,1)
			delay(1000)
			GPIO.output(POWERKEY,0)
			delay(1000)
		
		while self.getModemStatus():
			pass
		debug_print("M95 module powered up!")
		
	# Function for getting modem power status
	def getModemStatus(self):
		return GPIO.input(STATUS)
	
	# Function for getting modem response
	def getResponse(self, desired_response):
		if (ser.isOpen() == False):
			ser.open()
			
		while 1:	
			self.response =""
			while(ser.inWaiting()):
				self.response += ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
			if(self.response.find(desired_response) != -1):
				debug_print(self.response)
				break
	
	# Function for sending data to module
	def sendDataCommOnce(self, command):
		if (ser.isOpen() == False):
			ser.open()		
		self.compose = ""
		self.compose = str(command)
		ser.reset_input_buffer()
		ser.write(self.compose.encode())
		debug_print(self.compose)

	# Function for sending at comamand to module
	def sendATCommOnce(self, command):
		if (ser.isOpen() == False):
			ser.open()		
		self.compose = ""
		self.compose = str(command) + "\r"
		ser.reset_input_buffer()
		ser.write(self.compose.encode())
		debug_print(self.compose)
		
	# Function for sending data to M95_AT.
	def sendDataComm(self, command, desired_response, timeout = None):
		
		if timeout is None:
			timeout = self.timeout
        
		self.sendDataCommOnce(command)
		
		timer = millis()
		while 1:
			if( millis() - timer > timeout): 
				self.sendDataCommOnce(command)
				timer = millis()
			
			self.response =""
			while(ser.inWaiting()):
				self.response += ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
			if(self.response.find(desired_response) != -1):
				debug_print(self.response)
				break

	# Function for sending at command to M95_AT.
	def sendATComm(self, command, desired_response, timeout = None):
		
		if timeout is None:
			timeout = self.timeout
			
		self.sendATCommOnce(command)
		
		f_debug = False
		
		timer = millis()
		while 1:
			if( millis() - timer > timeout): 
				self.sendATCommOnce(command)
				timer = millis()
				f_debug = False
			
			self.response =""
			while(ser.inWaiting()):
				try: 
					self.response += ser.read(ser.inWaiting()).decode('utf-8', errors='ignore')
					delay(100)
				except Exception as e:
					debug_print(e.Message)
				# debug_print(self.response)
					
			if(self.response.find(desired_response) != -1):
				debug_print(self.response)
				break

	# Function for saving conf. and reset M95_AT module
	def resetModule(self):
		self.saveConfigurations()
		delay(200)
		self.disable()
		delay(200)
		self.enable()
		self.powerUp()

	# Function for save configurations that be done in current session. 
	def saveConfigurations(self):
		self.sendATComm("AT&W","OK\r\n")

	# Function for getting IMEI number
	def getIMEI(self):
		return self.sendATComm("AT+CGSN","OK\r\n")

	# Function for getting firmware info
	def getFirmwareInfo(self):
		return self.sendATComm("AT+CGMR","OK\r\n")

	# Function for getting hardware info
	def getHardwareInfo(self):
		return self.sendATComm("AT+CGMM","OK\r\n")

	# Function for getting self.ip_address
	def getIPAddress(self):
		return self.ip_address

	# Function for setting self.ip_address
	def setIPAddress(self, ip):
		self.ip_address = ip


	# Function for getting self.domain_name
	def getDomainName(self):
		return self.domain_name

	# Function for setting domain name
	def setDomainName(self, domain):
		self.domain_name = domain

	# Function for getting port
	def getPort(self):
		return self.port_number

	# Function for setting port
	def setPort(self, port):
		self.port_number = port

	# Function for getting timout in ms
	def getTimeout(self):
		return self.timeout

	# Function for setting timeout in ms    
	def setTimeout(self, new_timeout):
		self.timeout = new_timeout


	#******************************************************************************************
	#*** Network Service Functions ************************************************************
	#****************************************************************************************** 

	# Fuction for getting signal quality
	def getSignalQuality(self):
		return self.sendATComm("AT+CSQ","OK\r\n")

	# Function for connecting to base station of operator
	def connectToOperator(self):
		debug_print("Trying to connect base station of operator...")
		self.sendATComm("AT+CGREG?","+CGREG: 0,1\r\n");
		self.getSignalQuality()

	
	#******************************************************************************************
	#*** SMS Functions ************************************************************************
	#******************************************************************************************
	
	# Function for sending SMS
	def sendSMS(self, number, text):
		self.sendATComm("AT+CMGF=1","OK\r\n") # text mode	
		delay(500)
		
		self.compose = "AT+CMGS=\""
		self.compose += str(number)
		self.compose += "\""

		self.sendATComm(self.compose,">")
		delay(1000)
		self.clear_compose()
		delay(1000)
		self.sendATCommOnce(text)
		self.sendATComm(self.CTRL_Z,"OK",8) # with 8 seconds timeout
		

	#******************************************************************************************
	#*** GNSS Functions ***********************************************************************
	#******************************************************************************************
	
	#Function for reading NMEA message
	def readNMEA(self):
		(count, data) = L96_SERIAL.bb_serial_read(L96_SOFT_RX)
		if count:
			print(data)
	
	# Function for turning on GNSS
	def turnOnGNSS(self):
		self.sendATComm("AT+QGPS=1","OK\r\n")

	# Function for turning of GNSS
	def turnOffGNSS(self):
		self.sendATComm("AT+QGPSEND","OK\r\n")
	
	# Function for getting latitude
	def getLatitude(self):

		self.sendATComm("ATE0","OK\r\n")
		self.sendATCommOnce("AT+QGPSLOC=2")
		
		timer = millis()
		while 1:
			self.response = ""

			while(ser.inWaiting()):
				self.response += ser.readline().decode('utf-8')
				
				if( self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1 ):
					self.response = self.response.split(",")
					ser.close()
					return Decimal(self.response[1])
					
				if(self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1 ):
					debug_print(self.response)
					ser.close()
					return 0
	
	# Function for getting longitude		
	def getLongitude(self):

		self.sendATComm("ATE0","OK\r\n")
		self.sendATCommOnce("AT+QGPSLOC=2")
		
		timer = millis()
		while 1:
			self.response = ""

			while(ser.inWaiting()):
				self.response += ser.readline().decode('utf-8')
				
				if( self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1 ):
					self.response = self.response.split(",")
					ser.close()
					return Decimal(self.response[2])
					
				if(self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1 ):
					debug_print(self.response)
					ser.close()
					return 0
	
	# Function for getting speed in MPH			
	def getSpeedMph(self):

		self.sendATComm("ATE0","OK\r\n")
		self.sendATCommOnce("AT+QGPSLOC=2")
		
		timer = millis()
		while 1:
			self.response = ""

			while(ser.inWaiting()):
				self.response += ser.readline().decode('utf-8')
				
				if( self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1 ):
					self.response = self.response.split(",")
					ser.close()
					return round(Decimal(self.response[7])/Decimal('1.609344'), 1)
					
				if(self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1 ):
					debug_print(self.response)
					ser.close()
					return 0
	
	# Function for getting speed in KMPH			
	def getSpeedKph(self):

		self.sendATComm("ATE0","OK\r\n")
		self.sendATCommOnce("AT+QGPSLOC=2")
		
		timer = millis()
		while 1:
			self.response = ""

			while(ser.inWaiting()):
				self.response += ser.readline().decode('utf-8')
				
				if( self.response.find("QGPSLOC") != -1 and self.response.find("OK") != -1 ):
					self.response = self.response.split(",")
					ser.close()
					return Decimal(self.response[7])
					
				if(self.response.find("\r\n") != -1 and self.response.find("ERROR") != -1 ):
					debug_print(self.response)
					ser.close()
					return 0

	#******************************************************************************************
	#*** TCP & UDP Protocols Functions ********************************************************
	#******************************************************************************************
	
	# Function for configurating and activating TCP context 
	def activateContext(self):
		self.sendATComm("AT+CGDCONT=1,\"IP\",\"CMNET\"","OK\r\n"); 
		delay(1000);
		self.sendATComm("AT+CGACT=1,1","OK\r\n");

	# Function for deactivating TCP context 
	def deactivateContext(self):
		self.sendATComm("AT+CGACT=0,1","OK\r\n");

	# Function for connecting to server via TCP
	# just buffer access mode is supported for now.
	def connectToServerTCP(self):
		self.compose = "AT+QIOPEN="
		self.compose += "\"TCP\",\""
		self.compose += str(self.ip_address)
		self.compose += "\","
		self.compose += str(self.port_number)

		self.sendATComm(self.compose,"OK\r\n")
		self.clear_compose()
		self.sendATComm("AT+QISTATE","OK\r\n");

	# Fuction for sending data via tcp.
	# just buffer access mode is supported for now.
	def sendDataTCP(self, data):
		self.compose = "AT+QISEND="
		self.compose += str(len(data))

		self.sendATComm(self.compose,">")
		self.sendATComm(data,"SEND OK")
		self.clear_compose()
	
	# Function for connecting to server via UDP
	def startUDPService(self):
		self.compose = "AT+QIOPEN=\"UDP\",\""
		self.compose += str(self.ip_address)
		self.compose += "\","
		self.compose += str(self.port_number)

		self.sendATComm(self.compose,"OK\r\n")
		self.clear_compose()
		self.sendATComm("AT+QISTATE","OK\r\n");

	# Fuction for sending data via udp.
	def sendDataUDP(self, data):
		self.compose = "AT+QISEND="
		self.compose += str(len(data))

		self.sendATComm(self.compose,">")
		self.clear_compose()
		self.sendATComm(data,"SEND OK")

	# Function for closing server connection
	def closeConnection(self):
		self.sendATComm("AT+QICLOSE","\r\n")

	# Function for sending data to Sixfab connect
	def sendDataSixfabConnect(self, server, token, data):
	
		self.compose = "AT+QHTTPCFG=\"contextid\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		self.compose = "AT+QHTTPCFG=\"requestheader\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		url = str("https://"+ server+ "/sixfabStage/")
		self.compose = "AT+QHTTPURL="
		self.compose += str(len(url))
		self.compose += ",80"
		self.setTimeout(20)
		self.sendATComm(self.compose,"CONNECT")
		self.clear_compose()
		self.sendDataComm(url,"OK")
	
		payload = "POST /sixfabStage/ HTTP/1.1\r\nHost: "+server+"\r\nx-api-key: "+ token +"\r\nContent-Type: application/json\r\nContent-Length: "+str(len(data))+"\r\n\r\n"
		payload += data
		
		print("POSTED DATA")
		print(payload)
		print("----------------")
	
		self.compose = "AT+QHTTPPOST="
		self.compose += str(len(payload))
		self.compose += ",60,60"
		
		self.sendATComm(self.compose,"CONNECT")
		self.clear_compose()
		self.sendDataComm(payload,"OK")
	
	# Function for sending data to IFTTT	
	def sendDataIFTTT(self, eventName, key, data):
		
		self.compose = "AT+QHTTPCFG=\"contextid\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		self.compose = "AT+QHTTPCFG=\"requestheader\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		self.compose = "AT+QHTTPCFG=\"self.responseheader\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		url = str("https://maker.ifttt.com/trigger/" + eventName + "/with/key/"+ key)
		self.compose = "AT+QHTTPURL="
		self.compose += str(len(url))
		self.compose += ",80"
		self.setTimeout(20)
		self.sendATComm(self.compose,"CONNECT")
		self.clear_compose()
		self.sendDataComm(url,"OK")
		
		payload = "POST /trigger/" + eventName + "/with/key/"+ key +" HTTP/1.1\r\nHost: maker.ifttt.com\r\nContent-Type: application/json\r\nContent-Length: "+str(len(data))+"\r\n\r\n"
		payload += data
	
		self.compose = "AT+QHTTPPOST="
		self.compose += str(len(payload))
		self.compose += ",60,60"
		
		self.sendATComm(self.compose,"CONNECT")
		self.clear_compose()
		self.sendDataComm(payload,"OK")
		
		delay(5000)
		
		self.sendATComm("AT+QHTTPREAD=80","+QHTTPREAD: 0")
	
	# Function for sending data to Thingspeak
	def sendDataThingspeak(self, key, data):
	
		self.compose = "AT+QHTTPCFG=\"contextid\",1"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		self.compose = "AT+QHTTPCFG=\"requestheader\",0"
		self.sendATComm(self.compose,"OK")
		self.clear_compose()
		
		url = str("https://api.thingspeak.com/update?api_key=" + key + "&"+ data)
		self.compose = "AT+QHTTPURL="
		self.compose += str(len(url))
		self.compose += ",80"
		self.setTimeout(20)
		self.sendATComm(self.compose,"CONNECT")
		self.clear_compose()
		self.sendDataComm(url,"OK")
	
		delay(3000)
		
		self.sendATComm("AT+QHTTPGET=80","+QHTTPGET")

	#******************************************************************************************
	#*** HAT Peripheral Functions **********************************************************
	#******************************************************************************************

	# Function for reading user button
	def readUserButton(self):
		GPIO.setup(USER_BUTTON, GPIO.IN)
		return GPIO.input(USER_BUTTON)

	# Function for turning on user LED
	def turnOnUserLED(self):
		GPIO.setup(USER_LED, GPIO.OUT)
		GPIO.output(USER_LED, 1)

	# Function for turning off user LED
	def turnOffUserLED(self):
		GPIO.setup(USER_LED, GPIO.OUT)
		GPIO.output(USER_LED, 0)
