import speech_recognition as sr 
import os 
import sys
from pydub import AudioSegment

r = sr.Recognizer()

def transcribe_audio(path):
	with sr.AudioFile(path) as source:
		audio_listened = r.record(source)
		text = r.recognize_google(audio_listened)
	return text

# a function that splits the audio file into fixed interval chunks and applies speech recognition
def audio_transcription_chunks(path, seconds=10):
	sound = AudioSegment.from_file(path)
	chunkLengthms = int(1000 * seconds) 
	chunks = [sound[i:i + chunkLengthms] for i in range(0, len(sound), chunkLengthms)]
	folderName = "audio-fixed-chunks"
	# create a directory to store the audio chunks
	if not os.path.isdir(folderName):
		os.mkdir(folderName)
	wholeText = ""
	# process each chunk 
	for i, audioChunk in enumerate(chunks, start=1):
		# export audio chunk and save it in the `folderName` directory.
		chunkFilename = os.path.join(folderName, f"chunk{i}.wav")
		print(chunkFilename)
		audioChunk.export(chunkFilename, format="wav")
		try:
			text = transcribe_audio(chunkFilename)
		except sr.UnknownValueError as e:
			print("Error:", str(e))
		except LookupError:
			print("Could Not Understand")
		else:
			text = f"{text.capitalize()}. "
			print(chunkFilename, ":", text)
			wholeText += text

	return wholeText

path = "samples/output1/call_1_test1.wav"
#path = sys.argv[1]
print("\nFull text:", audio_transcription_chunks(path, seconds=10))


"""
inputdir = "samples/output1/"
#sample = "test1.wav"
#newfilename = "call_1_" + sample
#convert_to_phone(sample, inputdir)
outputdir = "samples/output1/"

fileno = 0

for filename in os.listdir(inputdir):
	sample = filename
	f = os.path.join(inputdir, filename)
	print(f)
	fileno+=1
	print(fileno)
	newfilename = "call_" + str(fileno) + "_" + sample
	convert_to_phone(sample, inputdir, outputdir)
	
"""