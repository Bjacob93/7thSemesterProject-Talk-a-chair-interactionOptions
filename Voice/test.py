
import speech_recognition as sr
global x
rec = sr.Recognizer() 
keywords = ["next"]
with sr.Microphone() as source: 
    print("I'm listening!")
    audio = rec.listen(source=source) 

    try: 
        transcription = str(rec.recognize_google(audio))
    except sr.UnknownValueError: 
        transcription = "Google Speech API is confused" 
    except sr.RequestError as e: 
        transcription = "Request to Google Speech API failed, request error: ", e 
    print(transcription)
    x = transcription

if any(keyword in x for keyword in keywords):
	print("fisk")

