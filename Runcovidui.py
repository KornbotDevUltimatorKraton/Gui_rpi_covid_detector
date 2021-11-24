#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author:Chanapai Chuadchum
#Project:Auracore color controller GUI 
#release date:25/2/2020
from printrun.printcore import printcore
from printrun import gcoder
from PyQt5 import QtCore, QtWidgets, uic,Qt,QtGui 
from PyQt5.QtWidgets import QApplication,QTreeView,QDirModel,QFileSystemModel,QVBoxLayout, QTreeWidget,QStyledItemDelegate, QTreeWidgetItem,QLabel,QGridLayout,QLineEdit,QDial,QComboBox,QPushButton 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QIcon,QImage,QPalette,QBrush
from pyqtgraph.Qt import QtCore, QtGui   #PyQt graph to control the model grphic loaded  
import pyqtgraph.opengl as gl
import pandas as pd
import csv 
import os 
import sys
import serial 
import time
config_Data = { "Top_catesian":{'x':200,'y':200},"Bottom_catesian":{'x':200,'y':200}} #Configuretion data in json for the stepper motor control step co-ordination
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
#referent covid statu s
Covid_status = [] #current covid19 status on the testtube detected on each position and colllect into the json data created on the list 

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
        #Button function front 
        self.pushButton_3.clicked.connect(self.Addlist) #Getting the addlist function into the Qr reader function 
        self.pushButton_4.clicked.connect(self.Clearlist) #Clear list from the function of the Qr code 
        self.pushButton_6.clicked.connect(self.Rundetect) #Running the detector mode 
        self.pushButton_5.clicked.connect(self.Reportresult) #Report the result into the csv and pdf file 
        self.pushButton_9.clicked.connect(self.Qrgenerator_fromlist) #Getting the list of the customer to add in the list and concatinate the function of the qr code 

        #Textedit input 
        self.text = self.findChild(QTextEdit,"textEdit") #Qrcodename detected for text edit 
        self.text2 = self.findChild(QTextEdit,"textEdit_2") #Getting the match value 
        self.text3 = self.findChild(QTextEdit,"textEdit_4") #Getting the first name of the patient 
        self.text4 = self.findChild(QTextEdit,"textEdit_5") #Getting the last name of the patient 
        self.text5 = self.findChild(QTextEdit,"textEdit_6") #Getting the age of the patient 
        self.text6 = self.findChild(QTextEdit,"textEdit_7") #Getting the patient number 
        self.text7 = self.findChild(QTextEdit,"textEdit_3") #Show the mathed latest list of the text edit mathed value 
        #Label for the function of the the video frame display on the opencv covid 19 detection function 

        #Top camera #QR code detection 
        #Button control 
        self.pushButton_7.clicked.connect(self.Homeposition_top) #Getting the home position for the top catesian robot 
        self.pushButton.clicked.connect(self.Auto_calibration_top) #Getting the auto positioning calibration  and setting the interval of testtube pitch by itself
        
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
        
        #Y-axis control vertical slider 
        self.slider_yt = self.findChild(QSlider,"verticalSlider_2") #Getting the Y axis function of the slider to working 
        self.slider_yt.setMinimum(0) 
        self.slider_yt.setMaximum(config_Data.get('Top_catesian').get('y')) #Getting the maximum value of the Y config data on the catesian robot 
        
        # Setting the slider function controller
        #Bottom camera 
        #Button control 
        self.pushButton_8.clicked.connect(self.Homeposition_bottom) 
        self.pushButton_2.clicked.connect(self.Auto_calibration_bottom)
        self.dial3 = self.findChild(QDial,"dial_3") #Getting the dial 3 for the function of light intensity control 
        self.dial4 = self.findChild(QDial,"dial_4") #Getting the dial 4 for the function of the wavelength control function 
        self.slider_xb = self.findChild(QSlider,"horizontalSlider_2") 
        self.slider_xb.setMinimum(0) 
        self.slider_xb.setMaximum(config_Data.get('Bottom_catesian').get('x')) #Getting the config of the x axis at catesian robot 
        self.slider_yb = self.findChild(QSlider,"verticalSlider_2")  #Getting the config of the y axis at catsian robot 
        self.slider_yb.setMinimum(0)
        self.slider_yb.setMaximum(config_Data.get('Bottom_catesian').get('y'))
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Button Function of the covid detect page 
    def Addlist(self): #Addlist function to  
          print("Add list")
    def Clearlist(self):
          print("Clear list")
    def Rundetect(self):
          print("Run detection")
    def Reportresult(self):
          print("Report result")
    def Qrgenerator_fromlist(self):
          print("Qrcode generator")

   
    #Button Function of the Top camera 
    def Homeposition_bottom(self):
           print("Home position bottom")
    def Auto_calibration_bottom(self): 
           print("Auto calibration bottom")
    #Dial data 
    def Light_intense_top(self): 
          print("Light intensiry top",self.dial1.value())

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
    
    def Top_yt(self):
        print("top_yt: ",self.slider_yt.value())   
        if len(yt_array) >1:
            yt_array.clear() #Clear out the array 
        yt_array.append(self.slider_yt.value())
    def Bottom_xb(self):
        print("bottom_xb: ",self.slider_xb.value())   
        if len(xb_array) >1:
             xb_array.clear() #clear out the array 
        xb_array.append(self.slider_xb.value())
    def Bottom_yb(self):
        print("bottom_xt: ",self.slider_yb.value())   
        if len(yb_array) >1:
            yb_array.clear() #clear out the array 
        yb_array.append(self.slider_yb.value()) 
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    

def Gcodecontrollermotion(Xt,Yt,Xb,Yb): #Getting the motion control function for the catesian robot 
        print(Xt,Yt,Xb,Yb) #Getting the value from each axis input from each catesian robot 

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

    
if __name__ == '__main__':         
    main()
