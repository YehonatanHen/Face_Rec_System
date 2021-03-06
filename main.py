import cv2
from tkinter import *
from tkinter import ttk
import tkinter as tk
import keyboard
import sys
import datetime
from playsound import playsound
from MainPageWindow import WelcomeWindow
from User_login import *
from StartPage import * #some functions and varibales in start page are necessery here
from User_login import User_login as ul
from StartPage import StartPage as sp


class ManageAppFrames(tk.Tk):
    ''' ManageAppFrames class - makes a main window for all the other GUI classes and opens it in the same window '''
    def __init__(self,*args,**kwargs):q
        tk.Tk.__init__(self,*args,**kwargs)
        self.title('Hours registration system')
        self.geometry("1000x850")
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        #Background sound helps with accessability for visually impaired users.
        pygame.mixer.init()
        pygame.mixer.music.load('general audio\\background_audio.mp3')
        pygame.mixer.music.play(999)
        #set volume of background music
        global music_vol
        pygame.mixer.music.set_volume(music_vol)
        self.frames={}
        for F in (sp,ul):
            frame=F(container,self)
            self.frames[F] = frame
            frame.grid(row = 0,column = 0,sticky = "nsew")
        self.show_frame(sp)


    def show_frame(self,controller):
        ''' Showing user login window '''
        if(str(controller)=="<class 'User_login.User_login'>"):
            changecolor(self.frames[controller])
            Change_font_size(self.frames[controller])
        if(color_changer!=0):
            self.frames[controller]["bg"]=color1[color_changer-1]
        else:
            self.frames[controller]["bg"]=color1[9]
        frame = self.frames[controller]
        #Advance the window to the front
        frame.tkraise() 

def OpenMenu():
    ''' makes a ManageAppFrames object and play it '''
    app=ManageAppFrames()
    app.mainloop()

# play the whole system (main)
WelcomeWindow()
faces()
OpenMenu()
