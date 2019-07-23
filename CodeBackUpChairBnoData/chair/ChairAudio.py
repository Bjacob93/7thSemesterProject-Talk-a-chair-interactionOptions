from AudioData import AudioData
import serial
import pygame
import time
import datetime


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
	

pygame.mixer.init()
createLogFile()

lastDir = "none"
port = serial.Serial("/dev/ttyACM0", 9600)
lastTime = time.time()
timeSinceData = 0
timeSinceUserDetected = 0
nextIdleSpeak = 0
userHere = False
audioMode = 0

directionData = 0

# Content arrays
pastContent = [AudioData(350, 10, "kommune past", "/home/pi/Desktop/chair/data/Kommune_bygning.mp3"),
               AudioData(20, 35, "stigsborg past", "/home/pi/Desktop/chair/data/Stigsborg_Parken.mp3"),
               AudioData(40, 55, "industri past", "/home/pi/Desktop/chair/data/Industri.mp3"),
               AudioData(70, 90, "oestrehavn past", "/home/pi/Desktop/chair/data/Ostre_Havn.mp3"),
               AudioData(115, 140, "MH past", "/home/pi/Desktop/chair/data/Musikkens_Hus.mp3"),
               AudioData(160, 175, "NK past", "/home/pi/Desktop/chair/data/Nordkraft.mp3"),
               AudioData(260, 280, "havnefront past", "/home/pi/Desktop/chair/data/Aalborg_Harbourfront.mp3"),
               AudioData(290, 310, "broen past", "/home/pi/Desktop/chair/data/Limfjordsbroen.mp3"),
               AudioData(320, 340, "PPH past", "/home/pi/Desktop/chair/data/PPH.mp3")]

presentContent = [AudioData(350, 10, "kommune present", "/home/pi/Desktop/chair/data/.mp3"),
                  AudioData(20, 35, "stigsborg present", "/home/pi/Desktop/chair/data/.mp3"),
                  AudioData(40, 55, "industri present", "/home/pi/Desktop/chair/data/.mp3"),
                  AudioData(70, 90, "oestrehavn present", "/home/pi/Desktop/chair/data/.mp3"),
                  AudioData(115, 140, "MH present", "/home/pi/Desktop/chair/data/.mp3"),
                  AudioData(160, 175, "NK present", "/home/pi/Desktop/chair/data/.mp3"),
                  AudioData(225, 245, "create present", "/home/pi/Desktop/chair/data/.mp3"),
                  AudioData(260, 280, "havnefront present", "/home/pi/Desktop/chair/data/.mp3"),
                  AudioData(290, 310, "broen present", "/home/pi/Desktop/chair/data/.mp3"),
                  AudioData(320, 340, "PPH present", "/home/pi/Desktop/chair/data/.mp3")]

eventContent = [AudioData(20, 35, "stigsborg event", "/home/pi/Desktop/chair/data/.mp3"),
                AudioData(70, 90, "oestrehavn event", "/home/pi/Desktop/chair/data/.mp3"),
                AudioData(115, 140, "MH event", "/home/pi/Desktop/chair/data/.mp3"),
                AudioData(160, 175, "NK event", "/home/pi/Desktop/chair/data/.mp3"),
                AudioData(260, 280, "havnefront event", "/home/pi/Desktop/chair/data/.mp3")]

while True:
	data = ""
	
	try:
		data = port.readline()
		timeSinceData = 0
	except serial.SerialException as e:
		print(e)
		timeSinceData += time.time() - lastTime
	except TypeError as e:
		print(e)
		timeSinceData += time.time() - lastTime
	except Exception as e:
		print(e)
		timeSinceData += time.time() - lastTime
	
	data.replace(" ", "")
	data.strip()
	data = data.strip("\n")
	data = data.strip("\r")
	if data != "":
		if data == "contentUp":
			if audioMode == 2: 
				audioMode = 0
			else: audioMode += 1
		elif data == "userDetected":
			userHere = True
			timeSinceUserDetected = 0
		else:
			try:
				directionData = float(data)
			except Exception as e:
				print(e)
				print(repr(data))
	
	
	
	timeSinceUserDetected += time.time() - lastTime
	if pygame.mixer.music.get_busy():
		timeSinceSpeak = 0
	
	if audioMode == 0:
		determineAudio(directionData, lastDir, pastContent)
		
	elif audioMode == 1:
		determineAudio(directionData, lastDir, presentContent)
		
	elif audioMode == 2:
		determineAudio(directionData, lastDir, eventContent)
	
	lastTime = time.time()
	if userHere == False:
		playIdleAudio()
		nextIdleSpeak += 1
			
		if nextIdleSpeak > 2:
			nextIdleSpeak = 0
				
	if userHere == True and timeSinceUserDetected > 90:
		userHere = False
			
	
	# print(timeSinceData)
	if timeSinceData > 5:
		try:
			port.close()
			port.open()
		# port = serial.Serial("/dev/ttyACM0", 9600)
		except Exception as e:
			print(e)
