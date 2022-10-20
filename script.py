from moviepy.editor import *
import sounddevice as sd
from scipy.io.wavfile import write
import uuid
import subprocess
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cv2
from multiprocessing import Process

if not os.path.exists("build"):
    os.mkdir("build")
    
fileName = str(uuid.uuid4())
jobs =[]
images = []
def player():
    path = os.getcwd()
    cap = cv2.VideoCapture(path+'/build/'+fileName+'.mp4')
    cv2.namedWindow('Video',cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Video",640,480)
    while True:
        ret_val, frame = cap.read()
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()

def imageMerge():
    imageData = []
    for temp in images:
        tempData = ImageClip(temp)
        tempData = tempData.set_duration(30.0)
        imageData.append(tempData)
    video = concatenate(imageData,method="compose")
    video.write_videofile('build/'+fileName+".mp4",fps=30)

    messagebox.showinfo("Info", "Video Created successfully.")
    

def audioRecorder():
    tempDuration = VideoFileClip('build/'+fileName+".mp4").duration
    fs = 44100
    audio = sd.rec(int(tempDuration * fs), samplerate=fs, channels=2)
    sd.wait()
    write('build/'+fileName+'.wav',fs,audio)

def merger():
    name = str(uuid.uuid1())
    tempVideo = 'build/'+fileName+'.mp4'
    tempAudio = 'build/'+fileName+'.wav'

    cmd = 'ffmpeg -y -i '+tempAudio+'  -r 30 -i '+tempVideo+'  -filter:a aresample=async=1 -c:a flac -c:v copy '+'build/'+fileName+'.avi'
    subprocess.call(cmd, shell=True)
    
    os.remove(tempVideo)
    os.remove(tempAudio)

def Recorder():
    p1 =Process(target=audioRecorder)
    p2 = Process(target = player)
    jobs.append(p1)
    jobs.append(p2)
    p1.start()
    p2.start()

    for j in jobs:
        j.join()
    merger()
    messagebox.showinfo("Info", "Audio recorded successfully and your file is saved in build directory")
    
def browseFile():
    f = filedialog.askopenfilenames(multiple=True)
    for i in f:
        images.append(i)
    


root = Tk()
browse = Button(root,text="Browse",command=browseFile)
browse.grid(row=0,column=0)
ir = Button(root,text="Merge Images",command=imageMerge)
ir.grid(row=0,column=1)
r = Button(root,text="Record Audio and merge",command=Recorder)
r.grid(row=0,column=2)
label1 = Label(text="A message will popup when a process is completed")
label1.grid(row=1,column=0,columnspan=3)
label2 = Label(text="It may take time depending on size, quality and quantity of image / images")
label2.grid(row=2,column=0,columnspan=3)
root.mainloop()
