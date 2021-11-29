#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author:Chanapai Chuadchum
#Project:Auracore color controller GUI 
#release date:25/2/2020
from pyzbar import pyzbar 
import getpass 
import cv2  # Opencv for the camera qr code tracking and the covid 19 detection data 
import qrcode 
from printrun.printcore import printcore
from printrun import gcoder
from PyQt5.QtCore import Qt, QSize, QTimer, QThread

from PyQt5 import QtCore, QtWidgets, uic,Qt,QtGui 
from PyQt5.QtWidgets import QApplication,QTreeView,QDirModel,QFileSystemModel,QVBoxLayout, QTreeWidget,QStyledItemDelegate, QTreeWidgetItem,QLabel,QGridLayout,QLineEdit,QDial,QComboBox,QPushButton 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QIcon,QImage,QPalette,QBrush
from pyqtgraph.Qt import QtCore, QtGui   #PyQt graph to control the model grphic loaded  
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph.opengl as gl
import pandas as pd # Reading the pandas data from the csv data of the patient 
import csv #reading the csv file data 
import re
import os 
import sys
import serial # Serial protocol for connecting to the pheripheral devices like microcontroller 
import time
import subprocess # subprocess for running the command inside the linux system 
config_Data = {"Top_catesian":{'x':200,'y':200},"Bottom_catesian":{'x':200,'y':200}} #Configuretion data in json for the stepper motor control step co-ordination
#Setting the current position in array 
#Top cam catsian robot 
xt_array = [] 
yt_array =[]
#Bottom cam catesian robot 
xb_array = [] 
yb_array = []

#Calibration interval from the auto calibration 
Qr_interval = [] 
Covid_interval = []
#referent covid status
Covid_status = [] #current covid19 status on the testtube detected on each position and colllect into the json data created on the list 
seriallist = os.listdir("/sys/class/tty") 
serialmem1 = []

Patientpersonaldata = ['index no.','patient name','age'] #Getting the patients personal data as the key for the system 
Patientdata = {} #Getting the json file generated for the qrcode generator 
index_number = [] #Getting the index number of the patient 
name_patient =[]  #Getting the name of the patient 
age_patient = []  #Getting the age of the patient 
username = getpass.getuser() #Getting the host of the user 
PATHDIR = "/media/" + username #Getting the path from the list of this data 
listPATH_drive = os.listdir(PATHDIR) #Getting the data inside the list of the path

dirmem_ext = [] #Getting the external drive list data  
external_file = [] #Getting the external file in the directory
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
 # Camera devices get index 
cameradevmem = [] #getting the camera mem data inside the list of the function 
cam_index = [] #Getting the camera device index data 
Getcam = []
Index_cam =[] #Getting the index camera mem inside the list
cam_num = [] # Getting the camera number 
Qr_listdata = [] #Getting the qr code list data function
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Camera , SerialUSB , pheripheral device detect must running in the multitasking programming to automaticly detect the devices 
# List the camera webcam available connected with the computer 
try:
  listcamera = subprocess.check_output("v4l2-ctl --list-devices",shell=True)
  print("Camera devices listing")
  print(listcamera.decode()) #decode the list the camera device
  camlist = listcamera.decode().split("/dev/")
  for re in range(0,len(camlist)):
          print(camlist[re])
          cameradevmem.append(camlist[re])
  print(cameradevmem,len(cameradevmem))
  for indexcam in range(0,len(cameradevmem)-1):
              cam_index.append(cameradevmem[indexcam]) #Getting the index unsorted value 
  print(cam_index)
  #Getting the video camera with modulo technique 
  for qs in range(0,len(cam_index)):
            modulo = qs%2  #Getting the modulo calculate inside the data 
            if modulo == 1:
                Getcam.append(cam_index[qs]) #Getting the camera devices 
  print(Getcam[0])
  for w in range(0,len(Getcam)):
         print(str(Getcam[w])) #Getting the camera video list devices 
         Index_cam.append(str(Getcam[w]))
  print("Index camera: ",Index_cam)
  for wr in range(0,len(Index_cam)):
          print(list(Index_cam[wr]))
          listcamdat = list(Index_cam[wr])
          print(listcamdat[len(listcamdat)-3]) 
          indexcamdat = listcamdat[len(listcamdat)-3]
          cam_num.append(indexcamdat) 
  print("Camera list available ID: ",cam_num)
except: 
    print("No such camera device found!")

print(Index_cam) #Show the index cam list to using inside the 
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        #Load the UI Page
        uic.loadUi('coviddetector.ui', self)
        self.setWindowTitle('Covid detector')
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(p)
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Covid detector page 
        #label pixmap  camera 
        self.camera = self.findChild(QLabel,"label_16")
        self.camera.setFixedSize(451,441)
        #Button function front 
        self.pushButton_3.clicked.connect(self.Addlist) #Getting the addlist function into the Qr reader function 
        self.pushButton_4.clicked.connect(self.Clearlist) #Clear list from the function of the Qr code 
        self.pushButton_6.clicked.connect(self.Rundetect) #Running the detector mode 
        self.pushButton_5.clicked.connect(self.Reportresult) #Report the result into the csv and pdf file 
        self.pushButton_9.clicked.connect(self.Qrgenerator_fromlist) #Getting the list of the customer to add in the list and concatinate the function of the qr code 
        self.pushButton_10.clicked.connect(self.Visual1)
        #Textedit input 
        self.text = self.findChild(QTextEdit,"textEdit") #Qrcodename detected for text edit 
        self.text2 = self.findChild(QTextEdit,"textEdit_2") #Getting the match value 
        self.text3 = self.findChild(QTextEdit,"textEdit_4") #Getting the first name of the patient 
        self.text4 = self.findChild(QTextEdit,"textEdit_5") #Getting the last name of the patient 
        self.text5 = self.findChild(QTextEdit,"textEdit_6") #Getting the age of the patient 
        self.text6 = self.findChild(QTextEdit,"textEdit_7") #Getting the patient number 
        self.text7 = self.findChild(QTextEdit,"textEdit_3") #Show the mathed latest list of the text edit mathed value 
        #Combobox external drive data 
        self.combo_external = self.findChild(QComboBox,"comboBox_2") #Getting the combobox for the external for write and read file storage 
        self.combo_external.addItem("No drive") #List of status no drive detected 
        #List path data drive 
        for r in range(0,len(listPATH_drive)):
                 print(listPATH_drive)
                 for q in range(0,len(listPATH_drive)):
                             dirmem_ext.append(PATHDIR+"/"+listPATH_drive[q]) #Getting the drive file
        self.combo_external.addItems(dirmem_ext) #Getting the list of the external drive
        if listPATH_drive !=[]:
            try:
                #for w in range(0,len(dirmem_ext)):
                #       fileinside = os.listdir(dirmem_ext[w])
                #       print(fileinside) 
                #       for qw in range(0,len(fileinside)): #Getting the file inside the listdir 
                fileinside = os.listdir(PATHDIR+"/"+listPATH_drive[0]) #Get the file inside the directory 
                for qw in range(0,len(fileinside)):        
                        external_file.append(fileinside[qw]) #Getting the file append inside the external list 
                        
            except: 
                print("No drive found")
        #Setting the file from the drive inside directory 
        self.combo_external.activated[str].connect(self.Externaldata)      
        #List file inside the selected drive 
        self.combo_internal = self.findChild(QComboBox,"comboBox_3") #Getting the file inside the external drive selected 
        self.combo_internal.addItem("No-file") #No file in the case not selected 
        self.combo_internal.addItems(external_file) #Getting the list file extrackted from the list 
        self.combo_internal.activated[str].connect(self.Internalfile) #Getting the internal file 
        #Combobox serial communication with the hardware catesian robot 
        self.comboserial = self.findChild(QComboBox,"comboBox") #Get the serial communication from the combobox 
        self.comboserial.addItem("Non-serial") # Getting the item list on the serial search function 
        for i in range(0,len(seriallist)):
               
              if len(str(seriallist[i]).split("USB")) >= 2:

                        serialmem1.append(str(seriallist[i])) 
                        
              if len(str(seriallist[i]).split("ACM")) >= 2: 

                        serialmem1.append(str(seriallist[i])) 

        self.comboserial.addItems(serialmem1) #Get the serial data       
        self.comboserial.activated[str].connect(self.Serialfunc)      
        
        #Label for the function of the the video frame display on the opencv covid 19 detection function 
        
        #Top camera #QR code detection 
        self.camera2 = self.findChild(QLabel,"label_8")
        self.camera2.setFixedSize(541,431)

        self.camera3 = self.findChild(QLabel,"label") 
        self.camera3.setFixedSize(541,431) 

        #Button control 
        self.pushButton_7.clicked.connect(self.Homeposition_top) #Getting the home position for the top catesian robot 
        self.pushButton.clicked.connect(self.Auto_calibration_top) #Getting the auto positioning calibration  and setting the interval of testtube pitch by itself
        self.camon2 = self.findChild(QPushButton,"pushButton_11")
        self.camon2.clicked.connect(self.Visual2) #Getting the camera top view on detecting the QRcode and calibrate position 
        #Dial control 
        self.dial1 = self.findChild(QDial,"dial") # Getting the dial 1 for the function of the light intensity control 
        self.dial1.setMinimum(0)
        self.dial1.setMaximum(255) # PWM output control function
        self.dial1.setValue(0)
        self.dial1.valueChanged.connect(self.Light_intense_top) #Top light intensity control 
        self.dial2 = self.findChild(QDial,"dial_2") #Getting the dial 2 for the function of the wavelength control function 
        #X-axis control herizontal slider  
        self.slider_xt = self.findChild(QSlider,"horizontalSlider") #Getting the X axis function of the slider 
        self.slider_xt.setMinimum(0)
        self.slider_xt.setMaximum(config_Data.get('Top_catesian').get('x')) #Getting the maximum value of the X config data on the catesian robot        
        self.slider_xt.valueChanged.connect(self.Top_xt)
        #Y-axis control vertical slider 
        self.slider_yt = self.findChild(QSlider,"verticalSlider") #Getting the Y axis function of the slider to working 
        self.slider_yt.setMinimum(0) 
        self.slider_yt.setMaximum(config_Data.get('Top_catesian').get('y')) #Getting the maximum value of the Y config data on the catesian robot 
        self.slider_yt.valueChanged.connect(self.Top_yt)
        
        # Setting the slider function controller
        #Bottom camera 
        #Button control 
        self.pushButton_8.clicked.connect(self.Homeposition_bottom) 
        self.pushButton_2.clicked.connect(self.Auto_calibration_bottom)
        self.dial3 = self.findChild(QDial,"dial_3") #Getting the dial 3 for the function of light intensity control 
        self.dial3.setMinimum(0)
        self.dial3.setMaximum(255) # PWM output control function
        self.dial3.setValue(0)
        self.dial3.valueChanged.connect(self.Light_intense_bottom) #Top light intensity control
        self.dial4 = self.findChild(QDial,"dial_4") #Getting the dial 4 for the function of the wavelength control function 
        self.slider_xb = self.findChild(QSlider,"horizontalSlider_2") 
        self.slider_xb.setMinimum(0) 
        self.slider_xb.setMaximum(config_Data.get('Bottom_catesian').get('x')) #Getting the config of the x axis at catesian robot 
        self.slider_xb.valueChanged.connect(self.Bottom_xb)

        self.slider_yb = self.findChild(QSlider,"verticalSlider_2")  #Getting the config of the y axis at catsian robot 
        self.slider_yb.setMinimum(0)
        self.slider_yb.setMaximum(config_Data.get('Bottom_catesian').get('y'))
        self.slider_yb.valueChanged.connect(self.Bottom_yb)
        

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #Camera 
    def Visual1(self):
            #Camerafunc(self.camera,0,451,441)
             self.Worker1 = Worker1()
             self.Worker1.start()
             self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
    def Visual2(self):
            #Camerafunc(self.camera,0,451,441)
             self.Worker2 = Worker2()
             self.Worker2.start()
             self.Worker2.ImageUpdate.connect(self.ImageUpdateSlot2)
    
    # Button Function of the covid detect page 
    def Addlist(self): #Add list function to the dataset of the user 
          print("Add list")
          #Getting the patient name 
          firstname = self.text3.toPlainText()
          lastname  = self.text4.toPlainText()
          age = self.text5.toPlainText() 
          Number = self.text6.toPlainText() 
          print(firstname,lastname,age,Number) 
          Patientdata[Patientpersonaldata[0]] = index_number.append(str(Number))  
          Patientdata[Patientpersonaldata[1]] = name_patient.append(str(firstname)+"\t"+str(lastname))
          Patientdata[Patientpersonaldata[2]] = age_patient.append(str(age))
          print("Patient json data: ",Patientdata)
    def Clearlist(self):
          print("Clear list")
    def Rundetect(self):
          print("Run detection")
    def Reportresult(self):
          print("Report result")
    def Qrgenerator_fromlist(self):
          print("Qrcode generator")
          #Running the function of the patient data in the loop 
          img = qrcode.make('{'+'name'+":"+"kornbot"+'}')  #Adding the data list from the add list function here
          type(img)  # qrcode.image.pil.PilImage
          img.save("patientname.png") #Getting the path from the text input in the combobox 
          
   
    #Button Function of the Top camera 
    def Homeposition_bottom(self):
           print("Home position bottom")

    def Auto_calibration_bottom(self): 
           print("Auto calibration bottom")

    #Dial data 
    def Light_intense_top(self): 
          print("Light intensity top: ",self.dial1.value())
          self.lcd1 = self.findChild(QLCDNumber,"lcdNumber")
          self.lcd1.display(self.dial1.value())
          self.lcd1.setStyleSheet("""QLCDNumber { background-color: black; }""")
 
    def Light_intense_bottom(self):
          print("Light intensity bottom: ",self.dial3.value())
          self.lcd2 = self.findChild(QLCDNumber,"lcdNumber_5") 
          self.lcd2.display(self.dial3.value())
          self.lcd2.setStyleSheet("""QLCDNumber { background-color: black; }""")

    #Button Function of the Bottom camera 
    def Homeposition_top(self):
          print("Home position top")
    def Auto_calibration_top(self):
          print("Auto calibration top")

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
               #Running the function of the value 
    def Top_xt(self):
        print("top_xt: ",self.slider_xt.value())  #Getting the value on each axis to save the value into the an array of each axis 
        if len(xt_array) >1:
             xt_array.clear() # Clear out the array if the array is more than one 
        xt_array.append(self.slider_xt.value())
        print(xt_array,len(xt_array))
        self.lcd3 = self.findChild(QLCDNumber,"lcdNumber_3")
        self.lcd3.display(self.slider_xt.value()) #Getting the top slider of X axis
        self.lcd3.setStyleSheet("""QLCDNumber { background-color: black; }""")
 
    def Top_yt(self):
        print("top_yt: ",self.slider_yt.value())   
        if len(yt_array) >1:
            yt_array.clear() #Clear out the array 
        yt_array.append(self.slider_yt.value())
        print(yt_array,len(yt_array))
        self.lcd4 = self.findChild(QLCDNumber,"lcdNumber_4")
        self.lcd4.display(self.slider_yt.value()) #Getting the top slider of Y axis
        self.lcd4.setStyleSheet("""QLCDNumber { background-color: black; }""")
 
    def Bottom_xb(self):
        print("bottom_xb: ",self.slider_xb.value())   
        if len(xb_array) >1:
             xb_array.clear() #clear out the array 
        xb_array.append(self.slider_xb.value())
        print(xb_array,len(xb_array))
        self.lcd7 = self.findChild(QLCDNumber,"lcdNumber_7")
        self.lcd7.display(self.slider_xb.value()) #Getting bottom slider of X axis
        self.lcd7.setStyleSheet("""QLCDNumber { background-color: black; }""")
 
    def Bottom_yb(self):
        print("bottom_yb: ",self.slider_yb.value())   
        if len(yb_array) >1:
            yb_array.clear() #clear out the array 
        yb_array.append(self.slider_yb.value()) 
        print(yb_array,len(yb_array))
        self.lcd8 = self.findChild(QLCDNumber,"lcdNumber_8") 
        self.lcd8.display(self.slider_yb.value()) #Getting bottom slider of Y axis 
        self.lcd8.setStyleSheet("""QLCDNumber { background-color: black; }""")

    def Serialfunc(self,text): #Getting the text from the list file of the serial 
              print("serial_selected",text)
              try:
                if text != "Non-serial":
                     pnp_serial = printcore('/dev/'+str(text),115200) #fixed baudrate  using the serial communication to control the gcode core motion 
                     while not pnp_serial.online:
                               time.sleep(0.1)  

                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                #Do process processing here for the G-code command running the fully autonomouse code on the robot 
                
              except:
                  print("Serial connection fail please recheck the serial communication at the pnp machine") 
    def Externaldata(self,text):
              try:
                 print("External data: ",text) #the text is the actual directory of the drive 
              except:
                 print("No drive found") 
    def Internalfile(self,text):

              try:
                  print("Internal data: ",text)                  
              except:
                  print("No file found!") 
    def ImageUpdateSlot(self, Image):
            self.pixmap = QPixmap.fromImage(Image)
            self.camera.setPixmap(self.pixmap) 
            self.camera2.setPixmap(self.pixmap)        
    def ImageUpdateSlot2(self, Image):
            self.pixmap = QPixmap.fromImage(Image)
            self.camera3.setPixmap(self.pixmap)        
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    

def Gcodecontrollermotion(Xt,Yt,Xb,Yb): #Getting the motion control function for the catesian robot 
        print(Xt,Yt,Xb,Yb) #Getting the value from each axis input from each catesian robot 
    
class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(int(cam_num[0]))
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(451, 441, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()
class Worker2(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(int(cam_num[1])) 
        #detector = cv2.QRCodeDetector()
        while self.ThreadActive:
            try:
                if Qr_listdata == []:
                     Qr_listdata.append("No Qr_code_data")
                if len(Qr_listdata) > 1:
                     Qr_listdata.remove(Qr_listdata[0]) # remove the list if inside the list data has more than 1
                     print("Qr_code_Data: ",Qr_listdata[len(Qr_listdata)-1])
                     
            except:
                print("Out of range")     
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #print(Image)
                try:
                   
                   barcodes = pyzbar.decode(Image)
                   for barcode in barcodes:
	                              # extract the bounding box location of the barcode and draw the
	                              # bounding box surrounding the barcode on the image
	                              (x, y, w, h) = barcode.rect
                                  
	                              cv2.rectangle(Image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                                  # the barcode data is a bytes object so if we want to draw it on
	                              # our output image we need to convert it to a string first
	                              barcodeData = barcode.data.decode("utf-8")
	                              barcodeType = barcode.type
	                              # draw the barcode data and barcode type on the image
	                              text = "{} ({})".format(barcodeData, barcodeType)
	                              cv2.putText(Image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
                                  # Add the function to output the data from hear 

	                              Qr_listdata.append("[{},{},{},{}]".format(barcodeType, barcodeData,str(len(barcodes)),(x,y,w,h))) #Grab output data 
                                  
                except:

                    print("No QRcode detected!")
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(541, 431, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()
     
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


    
if __name__ == '__main__':         
      main()
