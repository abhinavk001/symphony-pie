import librosa
import numpy as np
import cv2 as cv
import subprocess
import os

#Loading file
filename = "./audio/back_to_you.mp3"
time_series, sample_rate = librosa.load(filename)  

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))


# converting the matrix to decibel matrix
spectrogram = librosa.amplitude_to_db(stft, ref=np.max)

# getting an array of frequencies, shape: 4097 range:freq 0- 1.10250000e+04, difference: 2.69165039e+00
frequencies = librosa.core.fft_frequencies(n_fft=2048*4)

# getting an array of time periodic
times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4) #shape:4471, range: 1.85759637e-01 - 2.07795374e+02, differnce; 0.023219955
time_index_ratio = len(times)/times[len(times) - 1]

frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]


def get_decibel(target_time, freq):
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]

size = 720, 1280, 3

def draw_circle(frame, center):
    thickness = 1
    line_type = 8
    cv.circle(frame, center, 80, (0, 0, 255), thickness, line_type)

def draw_line(frame, start, end):
    thickness = 7
    line_type = 8
    cv.line(frame, start, end, (200, 45, 0), thickness, line_type)

i=53
j=420
frame_count=1

""" frame = np.zeros(size, dtype=np.uint8)
draw_line(frame, (i,j), (i, 720-(np.abs(get_decibel(times[0], frequencies[0]))).astype(np.uint8)))
draw_line(frame, (i+10,j), (i+10, 720-(np.abs(get_decibel(times[0], frequencies[1]))).astype(np.uint8)))
draw_line(frame, (i+20,j), (i+20, 720-(np.abs(get_decibel(times[0], frequencies[2]))).astype(np.uint8)))
draw_line(frame, (40, 40), (40, 60))
cv.imwrite("1.jpg", frame) """
for iter in range(len(times)-1):
    i=53
    frame = np.zeros(size, dtype=np.uint8)                #640x360
    for frequency in range(100, 8000, 100):
        draw_line(frame, (i,j), (i, 500-((get_decibel(times[iter], frequency)*2)).astype(np.uint8)))
        i=i+15
    cv.imwrite(f'images/img_i001.{frame_count:05d}.jpg', frame)
    frame_count+=1

""" frame = np.zeros(size, dtype=np.uint8)                #640x360
for frequency in range(100, 8000, 100):
    draw_line(frame, (i,j), (i, 500-((get_decibel(times[0], frequency)*2)).astype(np.uint8)))
    i=i+15
cv.imwrite(f'images/img_p001.{frame_count:05d}.jpg', frame)
frame_count+=1 """

img_input = r"./images/img_i001.%05d.jpg"
video_output = "out.mp4"
framerate = 43
cmd = f'ffmpeg -framerate {framerate} -i {img_input} {video_output}'
subprocess.check_output(cmd, shell=True)

dir_name = "./images/"
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".jpg"):
        os.remove(os.path.join(dir_name, item))

cmd2 = 'ffmpeg -i out.mp4 -i audio/back_to_you.mp3 -map 0:v -map 1:a -c:v copy -shortest output.mp4'
subprocess.check_output(cmd2, shell=True)

