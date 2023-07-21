from __future__ import print_function

import os
import sys
import librosa

import soundfile as sf

EIGHT_KHZ = 8096 #sample rate of AMR codec
SPEECH_LOW_BAND = 200 #bandwidth of AMR phone codec
SPEECH_UPPER_BAND = 3400

def convert_to_phone(file, directory, outputt):
	filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), directory + file) #search for file
	newfilename = "call_1_" + file
	print(filename)
	timeSeries, sampleRate = librosa.load(filename, sr=None)
	print(timeSeries, sampleRate)
	resampledTimeSeries = librosa.core.resample(y=timeSeries, orig_sr=sampleRate, target_sr=EIGHT_KHZ) #resample
	print(resampledTimeSeries)
	sf.write(outputt+"eightkhz_resampled.wav", resampledTimeSeries, EIGHT_KHZ) #output

	stft = librosa.core.stft(y=resampledTimeSeries)
	
	stft[:SPEECH_LOW_BAND] = 0
	stft[SPEECH_UPPER_BAND: len(stft)] = 0 #bandstop filter 

	reconstructedTimeSeries = librosa.core.istft(stft)
	
	sf.write(outputt+newfilename, reconstructedTimeSeries, EIGHT_KHZ)
	os.remove(outputt+"eightkhz_resampled.wav")

inputdir = "samples/input/"
#sample = "test1.wav"
#newfilename = "call_1_" + sample
#convert_to_phone(sample, inputdir)
outputdir = "samples/output1/"

fileno = 0

()

for filename in os.listdir(inputdir):
	sample = filename
	f = os.path.join(inputdir, filename)
	print(f)
	fileno+=1
	print(fileno)
	newfilename = "call_" + str(fileno) + "_" + sample
	convert_to_phone(sample, inputdir, outputdir)




