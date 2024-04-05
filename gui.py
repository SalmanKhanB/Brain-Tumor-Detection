from dis import Instruction
import tkinter
from tkinter.messagebox import showinfo
from PIL import Image
from tkinter import FLAT, LEFT, Frame, Tk, Variable, filedialog
import cv2 as cv
from frames import *
from displayTumor import *
from predictTumor import *

class Gui:
    MainWindow = 0
    listOfWinFrame = list()
    FirstFrame = object()
    val = 0
    fileName = 0
    DT = object()
    wHeight =600
    wWidth = 1000

    def __init__(self):
        global MainWindow
        MainWindow = tkinter.Tk()
        MainWindow.geometry('1017x610')
        MainWindow.resizable(width=False, height=False)

        self.DT = DisplayTumor()

        self.fileName = tkinter.StringVar()

        self.FirstFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, 0, 0)
        self.FirstFrame.btnView['state'] = 'disable'

        self.listOfWinFrame.append(self.FirstFrame)

        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Brain Tumor Detection\nIqra University", height=2, width=40)
        WindowLabel.place(x=260, y=30)
        WindowLabel.configure(background="yellow", font=("Comic Sans MS", 16, "bold"))

        myColorBlue = '#40E0D0' 
        myColorGreen = '#40E0D0'

        self.val = tkinter.IntVar()
        RB1 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="Detect Tumor", variable=self.val,
                                  value=1, command=self.check, background= myColorBlue)
        RB1.place(x=420, y=200)
        RB2 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="View Tumor Region",
                                  variable=self.val, value=2, command=self.check, background= myColorBlue)
        RB2.place(x=420, y=250)

        # RB22 = tkinter.Button(self.FirstFrame.getFrames(), text="View Tumor Region",
        #                           variable=self.val, value=2, command=self.check, background= myColorBlue)
        # RB22.place(x=420, y=250)

        browseBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Select", width=18,  background= myColorGreen,command=self.browseWindow)
        browseBtn.place(x=100, y=250)
        
        InstructionBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Instruction", width=18,  background= myColorGreen,command=self.openFrame)
        InstructionBtn.place(x=100, y=200)

        MainWindow.mainloop()

    def getListOfWinFrame(self):
        return self.listOfWinFrame

    def browseWindow(self):
        global mriImage
        FILEOPENOPTIONS = dict(defaultextension='*.*', filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileName = filedialog.askopenfilename(**FILEOPENOPTIONS)
        image = Image.open(self.fileName)
        imageName = str(self.fileName)
        mriImage = cv.imread(imageName, 1)
        self.listOfWinFrame[0].readImage(image)
        self.listOfWinFrame[0].displayImage()
        self.DT.readImage(image)

    def openFrame(self):
        showinfo(title="Instruction", message="Instruction:\n1.Click on 'Browse' and select image."+
        "\n2.Click on 'Detect Tumor' and view the result.\n3.Click 'View Tumor Region' then.\n4.Click on 'View' to view region.\n\tThanks")

    def check(self):
        global mriImage
        #print(mriImage)
        if (self.val.get() == 1):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)

            res = predictTumor(mriImage)
            
            if res > 0.5:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Tumor Detected", height=1, width=20)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="red")
            else:
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="No Tumor", height=1, width=20)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="green")

            resLabel.place(x=700, y=450)

        elif (self.val.get() == 2):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)
            secFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, self.DT.displayTumor, self.DT)

            self.listOfWinFrame.append(secFrame)


            for i in range(len(self.listOfWinFrame)):
                if (i != 0):
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()

            if (len(self.listOfWinFrame) > 1):
                self.listOfWinFrame[0].btnView['state'] = 'active'

        else:
            print("Not Working")

mainObj = Gui()