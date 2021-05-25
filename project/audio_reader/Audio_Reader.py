import librosa
import numpy as np
import cv2 as cv
import subprocess
import os
#from project.utils import storage

class VideoGenerator():
    def covertToVideo(file_path_name, file_name):
        f_name, f_ext = os.path.splitext(file_name)
        #Loading file
        time_series, sample_rate = librosa.load(file_path_name)  

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

        size = 480, 854, 3

        def draw_circle(frame, center):
            thickness = 1
            line_type = 8
            cv.circle(frame, center, 80, (0, 0, 255), thickness, line_type)

        def draw_line(frame, start, end):
            thickness = 7
            line_type = 8
            cv.line(frame, start, end, (200, 45, 0), thickness, line_type)

        j=280
        frame_count=1

        for iter in range(0,len(times)-1, 2):
            i=36
            frame = np.zeros(size, dtype=np.uint8)                #640x360
            for frequency in range(100, 8000, 100):
                draw_line(frame, (i,j), (i, 370-((get_decibel(times[iter], frequency)*2)).astype(np.uint8)))
                i=i+10
            cv.imwrite(f'./project/audio_reader/images/img_i001.{frame_count:05d}.jpg', frame)
            frame_count+=1

        img_input = r"./project/audio_reader/images/img_i001.%05d.jpg"
        video_output = "out.mp4"
        framerate = 21.55
        cmd = f'ffmpeg -framerate {framerate} -i {img_input} {video_output}'
        subprocess.check_output(cmd, shell=True)

        dir_name = "./project/audio_reader/images/"
        test = os.listdir(dir_name)

        for item in test:
            if item.endswith(".jpg"):
                os.remove(os.path.join(dir_name, item))

        cmd2 = f'ffmpeg -i out.mp4 -i {file_path_name} -map 0:v -map 1:a -c:v copy -shortest {f_name}.mp4'
        subprocess.check_output(cmd2, shell=True)

        os.remove('out.mp4')
        os.remove(file_path_name)
        return f'{f_name}.mp4'
        

