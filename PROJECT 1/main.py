import cv2
import pyramids
import heartrate
import preprocessing
import PROJECT

# Frequency range for Fast-Fourier Transform
freq_min = 1
freq_max = 1.8

# Preprocessing phase
print("Reading + preprocessing video...")
video_frames, frame_ct, fps = preprocessing.read_video("videos/parth.mp4")

# Build Laplacian video pyramid
print("Building Laplacian video pyramid...")
lap_video = pyramids.build_video_pyramid(video_frames)

amplified_video_pyramid = []

for i, video in enumerate(lap_video):
    if i == 0 or i == len(lap_video)-1:
        continue

    # PROJECT magnification with temporal FFT filtering
    print("Running FFT and PROJECT magnification...")
    result, fft, frequencies = PROJECT.fft_filter(video, freq_min, freq_max, fps)
    lap_video[i] += result

    # Calculate heart rate
    print("Calculating heart rate...")
    heart_rate = heartrate.find_heart_rate(fft, frequencies, freq_min, freq_max)

# Collapse laplacian pyramid to generate final video
print("Rebuilding final video...")
amplified_frames = pyramids.collapse_laplacian_video_pyramid(lap_video, frame_ct)

# Output heart rate and final video
print("Heart rate: ", heart_rate, "bpm")
print("Displaying final video...")

import tkinter
from tkinter import messagebox

# This code is to hide the main tkinter window
root = tkinter.Tk()
root.withdraw()

# Message Box


if(heart_rate<=59):
    messagebox.showinfo("Alert!!","Your heartbeat is less than required. Please Contact Doctor!")
elif(heart_rate>=90):
    messagebox.showinfo("Alert!!","Your heartbeat is More than required. Clam Down! Your self with some medication :)")



for frame in amplified_frames:
    cv2.imshow("frame", frame)
    cv2.waitKey(20)
