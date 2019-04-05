from Tkinter import *
from random import *
import random
import string
import os
import csv
from PIL import Image,ImageDraw

class PaintBox(Frame):
    def __init__(self,data_type):
        Frame.__init__( self )
        self.pack( expand = YES, fill = BOTH )
        self.master.title( "Simple Draw App v1.0" )
        self.master.geometry( "100x140" )

        #self.message = Label( self, text = "Drag the mouse to draw" )
        #self.message.pack( side = BOTTOM )
        
        self.tagName = Text(self, height=1, width=10)
        self.tagName.pack(side = TOP)
        self.btnSave = Button(self, text = "Save", command = self.save,height=1, width=10)
        self.btnSave.pack(side = TOP)

        # create Canvas component
        self.myCanvas = Canvas( self )
        self.myCanvas.pack( expand = NO, fill = BOTH , side = TOP)

        # bind mouse dragging event to Canvas
        self.myCanvas.bind("<B1-Motion>", self.paint )
        self.myCanvas.bind("<ButtonPress-1>", self.b1down)
        self.myCanvas.bind("<ButtonRelease-1>", self.b1up)

        

        self.image = self.newImage()
        self.draw = self.newDraw()
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.coords= []

        self.data_type = data_type

    def save(self):
        if(self.data_type == "Train"):
            path = "./Train/" + self.tagName.get("1.0",'end-1c')
        elif(self.data_type == "Test"):
            path = "./Test/"

        
        if not os.path.exists(path):
            os.makedirs(path)
        name = ""
        for i in range(0,5):
            name += random.choice(string.ascii_letters)
        path += "/" + name +str(randint(1, 10000)) + ".png"

        if(self.data_type == "Train"):
            with open('train.csv','a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([path, self.tagName.get("1.0",'end-1c')])
            self.image.save(path)
        elif(self.data_type == "Test"):
            with open('test.csv','a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([path, self.tagName.get("1.0",'end-1c')])
            self.image.save(path)
        self.clear()

    def clear(self):
        print("clear")
        self.myCanvas.delete("all")
        self.image = self.newImage()
        self.draw = self.newDraw()

    def paint( self, event ):
        x1, y1 = ( event.x - 0.1 ), ( event.y - 0.1 )
        x2, y2 = ( event.x + 0.1 ), ( event.y + 0.1 )
        self.myCanvas.create_oval( x1, y1, x2, y2, fill = "black" )
        self.coords.append((x1,y1))

    def b1down(self,event):
        print("down")

    def b1up(self,event):
        self.draw.line(self.coords,"black",width=3)
        self.coords = []

    def newImage(self):
        return Image.new("RGB",(100,100),(255,255,255))

    def newDraw(self):
        return ImageDraw.Draw(self.image)
