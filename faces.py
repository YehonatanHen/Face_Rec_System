import numpy as np
import cv2
import pickle
from playsound import playsound
import camera
import datetime
from gtts import gTTS
import os

def make_4k():
    cap.set(3, 3840)
    cap.set(4, 2160)

if os.path.isfile("match.mp3"):
    os.remove("match.mp3")
    print("removed")
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)
make_4k()
i=0
counter1 = 0
counter2 = 0
lrcounter = 8
name = "None"
tempname = "None"
color = (0,0,255)
beepflag = 1
tempmatch = 'None'
#beepuls = 0

while(True):
    '''
    if cv2.waitKey(20) & 0xFF == ord('v'):
        if beepflag == 0:
            beepflag = 1
        if beepflag == 1:
            beepflag = 0
    if beepflag == 1:
        beepuls += 1
        if beepuls % 25 == 0:
            playsound('beep.mp3',False)
            '''
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=12, minNeighbors=5)

    for (x, y, w, h) in faces:
        #print(x,y,w,h)
        roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
        roi_color = frame[y:y+h, x:x+w]

        # recognize? deep learned model predict keras tensorflow pytorch scikit learn
        id_, conf = recognizer.predict(roi_gray)
        if conf>=54.5 and conf <= 60:
            #print(conf)
            #print(5: #id_)
            print(labels[id_], name, counter1,counter2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            if labels[id_] == name or name == "None":
                counter1+=1
                counter2 = 0
                if counter1 == 10:
                    tempname = name
            if tempname != name:
                counter2 += 1
            if counter2 >= 8:
                counter1 = 0
                
            name = labels[id_]
            
            stroke = 2 #font thickness
            ''' #match sound
            if counter1 > 20 and counter2 == 0:
                match = "Match found: " + tempname
                if counter1%2 == 0:
                    color = (0, 255, 0)
                else:
                    color = (255, 255, 255)
                cv2.putText(frame, match, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                
                tts = gTTS(text=match, lang = 'en')
                tts.save("match.mp3")
                if(tempmatch != match):
                    if os.path.isfile("match.mp3"):
                        playsound("match.mp3",False)
                    if os.path.isfile("match.mp3") and tempmatch!='None' and tempmatch!=match:
                        print("start")
                        os.remove("match.mp3")
                        print("end")
                    tempmatch = match
                    

            el'''
            if counter1 > 10:
                color = (0, 255, 0) #green
                cv2.putText(frame, tempname, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                
            else:
                color = (0, 0, 255) #red
                cv2.putText(frame, "analyzing...", (x,y), font, 1, color, stroke, cv2.LINE_AA)
                
        else:
            counter2+=1
        
        cv2.imshow('frame',frame)

        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        # sound
        print(x)
        if x < 350:
            if lrcounter % 10 == 0:
                playsound('moveright.mp3',False)
            lrcounter+=1
        
        elif x > 680:
            if lrcounter % 10 == 0:
                playsound('moveleft.mp3',False)
            lrcounter+=1

        if cv2.waitKey(20) & 0xFF == ord('p'):
            i+=1
            if counter1>10 and counter2 == 0:
                img_item =  "images\\" + tempname + "\\" + tempname + str(i) +".png"
            else:
                img_item =  "unknown\\unknown" + str(i) +".png" 
            cv2.imwrite(img_item, roi_color)
            #now = (datetime.datetime.now()).strftime("%Y-%m-%d %H_%M_%S")
        #subitems = smile_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in subitems:
        #	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    # Display the resulting frame
    cv2.imshow('frame',frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()