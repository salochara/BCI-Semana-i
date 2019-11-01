from serial.tools import list_ports
from pydobot import Dobot
from turtle import Turtle, Screen
import os 
import random
from alphabet import alphabet
import socket
import sys

# Global variable definitions
TURTLE_SIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
flag = False
tmp = ''
message = ''
count = 0
column = 0
c = 0
# Binding for the socket. IP, Port
s.bind(('127.0.0.1', 2000))
# Physical port where DoBot is.
port = list_ports.comports()[1].device
device = Dobot(port=port, verbose=False)

def init():
	device.speed(75,75) # Defines dobot velocity and acceleration in 75%
	device.move_to(250, 0, 50, 0, wait=True) #DOBOT HOME
	#print("Move DoBOT to desired position for writing")
	#input("Press Enter to continue...")
	device.move_to(193.02188110351562, -45.02191162109375, -48.760108947753906, 0, wait = True)

def receive():
	recibido = s.recvfrom(1024) # Receives message using socket
	data = recibido[0]
	message_received = ''
	for key in data:
		message_received += chr(key)
	message_received=message_received.upper()
	return message_received

# Main loop	
while True:
	init()
	(x, y, z, r, j1, j2, j3, j4) = device.pose() # Gets the Dobot position
	print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}') #Prints dobot position

	device.move_to(250, 0, 50 , 0, wait=True) #DOBOT HOME

	yertle = Turtle(shape="turtle", visible=False)
	yertle.penup()
	yertle.goto(y,x) # Turtle goes to the dobot selected position for writing
	yertle.pendown()
	yertle.goto(y,x) # Turtle goes to the dobot selected position for writing
	
	device.move_to(x, y, z,0, wait = True)
	zw = z
	aw = y
	bw = x
	width = 100 # Width of an A4 sheet
	n_character = 0
	(a,b) = (y,x)
	# Defining writing details
	fontSize = 10
	characterSpacing = (.5 * fontSize)

	# Loop for writing
	while True:
		if flag == False:
			tmp = receive()
			while tmp[0] != "S":
				tmp = receive()
		else:
			flag = False
		print(tmp)
		
		# Cases for selection
		if tmp == "Q":
			break
		elif tmp == "SELECTION: UP\n":
			message = "HOLA"
		elif tmp == "SELECTION: DOWN\n":
			message = "ADIOS" 
		elif tmp == "SELECTION: RIGHT\n":
			message = "SI"
		elif tmp == "SELECTION: LEFT\n":
			message = "NO"
		else:
			continue
		
		# Receives confirmation message, wich is "SELECTION: STOP"
		tmp = receive()
		while tmp[0] != "S":
			tmp = receive()
		# If the user confirms the selection, then the writing with DoBot will begin.
		if tmp == "SELECTION: STOP\n":
			# Writing part
			for character in message:
				if character == " ":
					a += characterSpacing
				
				elif character == "_":
					a = aw
					b +=fontSize + characterSpacing

				elif character in alphabet:
					letter=alphabet[character]
					yertle.penup()
					device.move_to(x, y, -10, 0, wait=True)
					for dot in letter:
						yertle.goto(a + dot[0]*fontSize, b + dot[1]*fontSize)
						yertle.pendown()
						(y,x) = yertle.position()
						device.move_to(x, y, zw, 0, wait=True)
					a += fontSize + .05*fontSize
			b += fontSize + characterSpacing
			count = count + 1
			if count == 4:
				count = 0
				column += 1
				c = 0
				b = bw
				for i in range (0,6):
					c += fontSize + .05*fontSize
			a = aw + column*c

			device.move_to(250, 0, 50, 0, wait=True) #DOBOT HOME
			print("Complete...\n")
		else:
			flag = True
			print("didnt receive stop")
	