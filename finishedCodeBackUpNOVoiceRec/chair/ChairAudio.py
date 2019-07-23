from AudioData import AudioData
import serial
import pygame
import time
import datetime

def switchContent():
	audioMode += 1
	if audioMode > 2: audioMode = 0
	contentSwitchTimer = 0
	contentHasUpdatedRecently = True
	global contentHasUpdatedRecently
	global contentSwitchTimer
	global audioMode

def createLogFile():
	f = open('logFile', 'a')
	f.write('Date' + '\t' + 'Time' + '\t' + 'Heading' + '\t' + 'Orientation \n')
	f.flush()
	f.close()


def logWrite(Heading, Orientation):
	n = datetime.datetime.now()
	f = open('logFile', 'a')
	f.write("%s" % n + '\t' + str(Heading) + '\t' + Orientation + '\n')
	f.flush()
	f.close()


def playIdleAudio():
	if nextIdleSpeak == 0:
		pygame.mixer.music.load("/home/pi/Desktop/chair/data/Idle_1.mp3")
	if nextIdleSpeak == 1:
		pygame.mixer.music.load("/home/pi/Desktop/chair/data/Idle_2.mp3")
	if nextIdleSpeak == 2:
		pygame.mixer.music.load("/home/pi/Desktop/chair/data/Idle_3.mp3")
	pygame.mixer.music.set_volume(1)
	pygame.mixer.music.play()


def determineAudio(dir, lDir, contentArray):
	for i in range (0, len(contentArray)):
		if contentArray[i].dirLeft > contentArray[i].dirRight:
			if (dir > contentArray[i].dirLeft or dir < contentArray[i].dirRight) and lDir != contentArray[i].dirString:
				lastDir = contentArray[i].dirString
				pygame.mixer.music.load(contentArray[i].audioPath)
				pygame.mixer.music.set_volume(1)
				pygame.mixer.music.play()
				logWrite(i, lastDir)
				global lastDir
		else:
			if (dir > contentArray[i].dirLeft and dir < contentArray[i].dirRight) and lDir != contentArray[i].dirString:
				lastDir = contentArray[i].dirString
				pygame.mixer.music.load(contentArray[i].audioPath)
				pygame.mixer.music.set_volume(1)
				pygame.mixer.music.play()
				logWrite(i, lastDir)
				global lastDir
	
# Call functions for initiation of the audio player, and to create the log file
pygame.mixer.init()
createLogFile()

# Port variable
port = serial.Serial("/dev/ttyACM0", 9600)

# Asorted variables
lastDir = "none"
lastTime = time.time()
timeSinceData = 0
timeSinceUserDetected = 0
nextIdleSpeak = 0
userHere = False
directionData = 0
contentHasUpdatedRecently = False

audioMode = 0 			# tracks which layer of audio should be played

contentSwitchTimer = 0

# Variables handling rotation patterns
originDirection = 0
rotationDelta = 0
rotationTimeout = 0
rotationStart = 0
currentlyRotating = False
rotationTracker = 0
tempDirection = 0
rotationDeltaIsLargeEnough = False

# Content arrays
pastContent = [AudioData(350, 10, "kommune past", "/home/pi/Desktop/chair/data/Past_Kommune.mp3"),
               AudioData(20, 35, "stigsborg past", "/home/pi/Desktop/chair/data/Past_Stigsborg.mp3"),
               AudioData(40, 55, "industri past", "/home/pi/Desktop/chair/data/Past_Industri.mp3"),
               AudioData(70, 90, "oestrehavn past", "/home/pi/Desktop/chair/data/Past_OstreHavn.mp3"),
               AudioData(115, 140, "MusikkensHus past", "/home/pi/Desktop/chair/data/Past_MH.mp3.mp3"),
               AudioData(160, 175, "NordKraft past", "/home/pi/Desktop/chair/data/Past_NK.mp3"),
               AudioData(260, 280, "havnefronten past", "/home/pi/Desktop/chair/data/Past_Havnefronten.mp3"),
               AudioData(290, 310, "broen past", "/home/pi/Desktop/chair/data/Past_Limfjordsbroen.mp3"),
               AudioData(320, 340, "PPH past", "/home/pi/Desktop/chair/data/Past_PPH.mp3")]

presentContent = [AudioData(350, 10, "kommune present", "/home/pi/Desktop/chair/data/Present_Kommune.mp3"),
                  AudioData(20, 35, "stigsborg present", "/home/pi/Desktop/chair/data/Present_Stigsborg.mp3"),
                  AudioData(40, 55, "industri present", "/home/pi/Desktop/chair/data/Present_Industri.mp3"),
                  AudioData(70, 90, "oestrehavn present", "/home/pi/Desktop/chair/data/Present_OstreHavn.mp3"),
                  AudioData(160, 175, "NordKraft present", "/home/pi/Desktop/chair/data/Present_NK.mp3"),
                  AudioData(225, 245, "create present", "/home/pi/Desktop/chair/data/Present_Create.mp3"),
                  AudioData(260, 280, "havnefronten present", "/home/pi/Desktop/chair/data/Present_Havnefronten.mp3")]

eventContent = [AudioData(20, 35, "stigsborg event", "/home/pi/Desktop/chair/data/Event_Stigsborg.mp3"),
                AudioData(70, 90, "oestrehavn event", "/home/pi/Desktop/chair/data/Event_OstreHavn.mp3"),
                AudioData(115, 140, "MusikkensHus event", "/home/pi/Desktop/chair/data/Event_MH.mp3"),
                AudioData(160, 175, "NordKraft event", "/home/pi/Desktop/chair/data/Event_NK.mp3"),
                AudioData(260, 280, "havnefront event", "/home/pi/Desktop/chair/data/Event_Havnefronten.mp3")]

while True:
	# Set the data string empty, ready for new data
	data = ""
	
	# Try to read data from the serial connection
	try:
		data = port.readline()
		timeSinceData = 0
	except serial.SerialException as e:		# if we don't get data, track how long we've gone without
		print(e)
		timeSinceData += time.time() - lastTime
	except TypeError as e:
		print(e)
		timeSinceData += time.time() - lastTime
	except Exception as e:
		print(e)
		timeSinceData += time.time() - lastTime
	
	# Strip the data of whitespace and unprintable characters
	data.replace(" ", "")
	data.strip()
	data = data.strip("\n")
	data = data.strip("\r")
	
	# If the data is not an empty string, figure out what it is
	if data != "":
		if data == "contentUp" and contentHasUpdatedRecently == False:	# Switch to the next layer of content
			print("contentUp")
			switchContent()
		elif data == "userDetected":	# A user has been detected
			print("userDetected")
			userHere = True
			timeSinceUserDetected = 0
		else:							# We have new orientation data, save it as a float
			try:
				directionData = float(data)
			except Exception as e:
				print(e)
				print(repr(data))

	
	# If the char has changed orientation since last cycle, track that it is currently rotating	
	if not rotationTracker == directionData and not currentlyRotating: 
		currentlyRotating = True
		rotationTimeout = 0
		originDirection = rotationTracker
		print("Rotation Starting: " + str(rotationDelta))
	
	# Update the rotationTracker reference to our current orientation
	rotationTracker = directionData
	
	# If we are rotation
	if currentlyRotating:
		
		# Update how long we have been rotating for
		rotationStart += time.time() - lastTime
		
		# If our current direction is different from the last one
		if not directionData == tempDirection:
			
			# Calculate our rotation Delta
			rotationDeltaTemp = originDirection - (directionData + rotationDelta)
			if rotationDeltaTemp > 180: rotationDeltaTemp -= 360
			if rotationDeltaTemp < -180: rotationDeltaTemp += 360
		
			rotationDelta += rotationDeltaTemp
			
			rotationTimeout = 0
		
		# Update orientation reference	
		tempDirection = directionData	
		
		# If we have rotated more than 5 degrees, that is enough to activate the pattern
		if abs(rotationDelta) > 5: 
			rotationDeltaIsLargeEnough = True
			print("rotation large enough: " + str(rotationDelta))
			
		# If the pattern is fulfilled, switch audio layer	
		if abs(rotationDelta) <5 and rotationStart > 2 and rotationDeltaIsLargeEnough and not contentHasUpdatedRecently:
			 switchContent()
			 currentlyRotating = False
			 print("contentUp - Rotation")
			 rotationDeltaIsLargeEnough = False
			 rotationDelta = 0
		
		# Update for how long we have not rotated, more more than 1.5 seconds, timeout.
		rotationTimeout += time.time() - lastTime
		if rotationTimeout > 1.5 or abs(rotationDelta) > 20: 
			print(rotationTimeout)
			print(abs(rotationDelta))
			print("Rotation Timeout")
			currentlyRotating = False
			rotationDeltaIsLargeEnough = False
			rotationDelta = 0
			print("hiya")

	# time since we have detected a user	
	timeSinceUserDetected += time.time() - lastTime
	
	# If audio is playing, set the timer since lasy audio to 0
	if pygame.mixer.music.get_busy():
		timeSinceSpeak = 0
	
	# Play correct audio depending on audio layer
	if audioMode == 0:
		determineAudio(directionData, lastDir, pastContent)
		
	elif audioMode == 1:
		determineAudio(directionData, lastDir, presentContent)
		
	elif audioMode == 2:
		determineAudio(directionData, lastDir, eventContent)
	
	# Update last cycle time
	lastTime = time.time()
	
	#If no user is present, chair should play idle sounds occationally
	if userHere == False:
		playIdleAudio()
		nextIdleSpeak += 1
			
		if nextIdleSpeak > 2:
			nextIdleSpeak = 0
	
	# If no user have been here for 90 seconds, register that			
	if userHere == True and timeSinceUserDetected > 90:
		userHere = False
			
	# If we have not recieved data for 5 seconds, try to reconnect through the port
	if timeSinceData > 5:
		try:
			port.close()
			port.open()
		# port = serial.Serial("/dev/ttyACM0", 9600)
		except Exception as e:
			print(e)
	
	contentSwitchTimer += time.time() - lastTime
	if contentSwitchTimer > 2 and contentHasUpdatedRecently:
		contentHasUpdatedRecently = False
