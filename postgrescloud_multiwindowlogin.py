#using the input data from the pyqt5 to login into the system with the client login app to checking with the database 
import os 
import sys 
import csv
import json 
import requests
import socket
import pywifi
import getpass 
import psycopg2 # Login for the client side on the app machine 
import pandas as pd 
import subprocess # Getting the subprocess 
import multiprocessing
import cv2, imutils, socket # Getting the opencv to connect with the web socket base to report the camera output to display on the gui firmware uploader 
import numpy as np
import time
import base64
from PyQt5.QtCore import Qt, QSize, QTimer, QThread
from PyQt5 import QtCore, QtWidgets, uic,Qt,QtGui 
from PyQt5.QtWidgets import QApplication,QTreeView,QDirModel,QFileSystemModel,QVBoxLayout, QTreeWidget,QStyledItemDelegate, QTreeWidgetItem,QLabel,QGridLayout,QLineEdit,QDial,QComboBox,QTextEdit,QTabWidget,QLineEdit,QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap,QIcon,QImage,QPalette,QBrush
from pyqtgraph.Qt import QtCore, QtGui   #PyQt graph to control the model grphic loaded  
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Pyqt5 opengl 
import pyqtgraph as pg 
from pyqtgraph.flowchart import Flowchart
import pyqtgraph.metaarray as metaarray

from paramiko import SSHClient, AutoAddPolicy # SSH remote command to activate the host machine control

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Query database from the remote postgresql 
#using this postgresql-opaque-57490 #heroku cloud postgresql roboreactoruser https://roboreactoruser.herokuapp.com/ | https://git.heroku.com/roboreactoruser.git
#*postgresql-rigid-15553  #heroku cloud postgresql robouserdb https://robouserdb.herokuapp.com/ | https://git.heroku.com/robouserdb.git
#postgresql-amorphous-76096 as DATABASE_URL https://robotuserinterface.herokuapp.com/
#Database url can be get from this command heroku config:get DATABASE_URL -a app name
DATABASE_URL = "postgres://wwpxpsshftlinh:b85574f77cd76ccbaef7a0f661086c6b28724d236c730c74c2d8021934e8bbe1@ec2-18-215-96-54.compute-1.amazonaws.com:5432/d8rl9i6joj63v8"
Host = "ec2-18-215-96-54.compute-1.amazonaws.com"
Database = "d8rl9i6joj63v8"
Password = "b85574f77cd76ccbaef7a0f661086c6b28724d236c730c74c2d8021934e8bbe1"
Port = "5432"
username = getpass.getuser()
print(username)
memwrite = [] #Getting the status of the writing process 
OS_name = [] #Getting the operating system choosing for uploadinto the robot
network_name = []
dict_cc = {} #Getting the dictionary 
username = getpass.getuser()
print(username)
PATH_SD_CARD = "/media/"+str(username)   #Path of the SD card 
name = "name"
code = "code"
ssidmem = [] #Getting the array ssid mem for the data of the wifi host name 
country = [{name: 'Afghanistan', code: 'AF'}, 
  {name: 'Åland Islands', code: 'AX'}, 
  {name: 'Albania', code: 'AL'}, 
  {name: 'Algeria', code: 'DZ'}, 
  {name: 'American Samoa', code: 'AS'}, 
  {name: 'AndorrA', code: 'AD'}, 
  {name: 'Angola', code: 'AO'}, 
  {name: 'Anguilla', code: 'AI'}, 
  {name: 'Antarctica', code: 'AQ'}, 
  {name: 'Antigua and Barbuda', code: 'AG'}, 
  {name: 'Argentina', code: 'AR'}, 
  {name: 'Armenia', code: 'AM'}, 
  {name: 'Aruba', code: 'AW'}, 
  {name: 'Australia', code: 'AU'}, 
  {name: 'Austria', code: 'AT'}, 
  {name: 'Azerbaijan', code: 'AZ'}, 
  {name: 'Bahamas', code: 'BS'}, 
  {name: 'Bahrain', code: 'BH'}, 
  {name: 'Bangladesh', code: 'BD'}, 
  {name: 'Barbados', code: 'BB'}, 
  {name: 'Belarus', code: 'BY'}, 
  {name: 'Belgium', code: 'BE'}, 
  {name: 'Belize', code: 'BZ'}, 
  {name: 'Benin', code: 'BJ'}, 
  {name: 'Bermuda', code: 'BM'}, 
  {name: 'Bhutan', code: 'BT'}, 
  {name: 'Bolivia', code: 'BO'}, 
  {name: 'Bosnia and Herzegovina', code: 'BA'}, 
  {name: 'Botswana', code: 'BW'}, 
  {name: 'Bouvet Island', code: 'BV'}, 
  {name: 'Brazil', code: 'BR'}, 
  {name: 'British Indian Ocean Territory', code: 'IO'}, 
  {name: 'Brunei Darussalam', code: 'BN'}, 
  {name: 'Bulgaria', code: 'BG'}, 
  {name: 'Burkina Faso', code: 'BF'}, 
  {name: 'Burundi', code: 'BI'}, 
  {name: 'Cambodia', code: 'KH'}, 
  {name: 'Cameroon', code: 'CM'}, 
  {name: 'Canada', code: 'CA'}, 
  {name: 'Cape Verde', code: 'CV'}, 
  {name: 'Cayman Islands', code: 'KY'}, 
  {name: 'Central African Republic', code: 'CF'}, 
  {name: 'Chad', code: 'TD'}, 
  {name: 'Chile', code: 'CL'}, 
  {name: 'China', code: 'CN'}, 
  {name: 'Christmas Island', code: 'CX'}, 
  {name: 'Cocos (Keeling) Islands', code: 'CC'}, 
  {name: 'Colombia', code: 'CO'}, 
  {name: 'Comoros', code: 'KM'}, 
  {name: 'Congo', code: 'CG'}, 
  {name: 'Congo, The Democratic Republic of the', code: 'CD'}, 
  {name: 'Cook Islands', code: 'CK'}, 
  {name: 'Costa Rica', code: 'CR'}, 
  {name: 'Cote D\'Ivoire', code: 'CI'}, 
  {name: 'Croatia', code: 'HR'}, 
  {name: 'Cuba', code: 'CU'}, 
  {name: 'Cyprus', code: 'CY'}, 
  {name: 'Czech Republic', code: 'CZ'}, 
  {name: 'Denmark', code: 'DK'}, 
  {name: 'Djibouti', code: 'DJ'}, 
  {name: 'Dominica', code: 'DM'}, 
  {name: 'Dominican Republic', code: 'DO'}, 
  {name: 'Ecuador', code: 'EC'}, 
  {name: 'Egypt', code: 'EG'}, 
  {name: 'El Salvador', code: 'SV'}, 
  {name: 'Equatorial Guinea', code: 'GQ'}, 
  {name: 'Eritrea', code: 'ER'}, 
  {name: 'Estonia', code: 'EE'}, 
  {name: 'Ethiopia', code: 'ET'}, 
  {name: 'Falkland Islands (Malvinas)', code: 'FK'}, 
  {name: 'Faroe Islands', code: 'FO'}, 
  {name: 'Fiji', code: 'FJ'}, 
  {name: 'Finland', code: 'FI'}, 
  {name: 'France', code: 'FR'}, 
  {name: 'French Guiana', code: 'GF'}, 
  {name: 'French Polynesia', code: 'PF'}, 
  {name: 'French Southern Territories', code: 'TF'}, 
  {name: 'Gabon', code: 'GA'}, 
  {name: 'Gambia', code: 'GM'}, 
  {name: 'Georgia', code: 'GE'}, 
  {name: 'Germany', code: 'DE'}, 
  {name: 'Ghana', code: 'GH'}, 
  {name: 'Gibraltar', code: 'GI'}, 
  {name: 'Greece', code: 'GR'}, 
  {name: 'Greenland', code: 'GL'}, 
  {name: 'Grenada', code: 'GD'}, 
  {name: 'Guadeloupe', code: 'GP'}, 
  {name: 'Guam', code: 'GU'}, 
  {name: 'Guatemala', code: 'GT'}, 
  {name: 'Guernsey', code: 'GG'}, 
  {name: 'Guinea', code: 'GN'}, 
  {name: 'Guinea-Bissau', code: 'GW'}, 
  {name: 'Guyana', code: 'GY'}, 
  {name: 'Haiti', code: 'HT'}, 
  {name: 'Heard Island and Mcdonald Islands', code: 'HM'}, 
  {name: 'Holy See (Vatican City State)', code: 'VA'}, 
  {name: 'Honduras', code: 'HN'}, 
  {name: 'Hong Kong', code: 'HK'}, 
  {name: 'Hungary', code: 'HU'}, 
  {name: 'Iceland', code: 'IS'}, 
  {name: 'India', code: 'IN'}, 
  {name: 'Indonesia', code: 'ID'}, 
  {name: 'Iran, Islamic Republic Of', code: 'IR'}, 
  {name: 'Iraq', code: 'IQ'}, 
  {name: 'Ireland', code: 'IE'}, 
  {name: 'Isle of Man', code: 'IM'}, 
  {name: 'Israel', code: 'IL'}, 
  {name: 'Italy', code: 'IT'}, 
  {name: 'Jamaica', code: 'JM'}, 
  {name: 'Japan', code: 'JP'}, 
  {name: 'Jersey', code: 'JE'}, 
  {name: 'Jordan', code: 'JO'}, 
  {name: 'Kazakhstan', code: 'KZ'}, 
  {name: 'Kenya', code: 'KE'}, 
  {name: 'Kiribati', code: 'KI'}, 
  {name: 'Korea, Democratic People\'S Republic of', code: 'KP'}, 
  {name: 'Korea, Republic of', code: 'KR'}, 
  {name: 'Kuwait', code: 'KW'}, 
  {name: 'Kyrgyzstan', code: 'KG'}, 
  {name: 'Lao People\'S Democratic Republic', code: 'LA'}, 
  {name: 'Latvia', code: 'LV'}, 
  {name: 'Lebanon', code: 'LB'}, 
  {name: 'Lesotho', code: 'LS'}, 
  {name: 'Liberia', code: 'LR'}, 
  {name: 'Libyan Arab Jamahiriya', code: 'LY'}, 
  {name: 'Liechtenstein', code: 'LI'}, 
  {name: 'Lithuania', code: 'LT'}, 
  {name: 'Luxembourg', code: 'LU'}, 
  {name: 'Macao', code: 'MO'}, 
  {name: 'Macedonia, The Former Yugoslav Republic of', code: 'MK'}, 
  {name: 'Madagascar', code: 'MG'}, 
  {name: 'Malawi', code: 'MW'}, 
  {name: 'Malaysia', code: 'MY'}, 
  {name: 'Maldives', code: 'MV'}, 
  {name: 'Mali', code: 'ML'}, 
  {name: 'Malta', code: 'MT'}, 
  {name: 'Marshall Islands', code: 'MH'}, 
  {name: 'Martinique', code: 'MQ'}, 
  {name: 'Mauritania', code: 'MR'}, 
  {name: 'Mauritius', code: 'MU'}, 
  {name: 'Mayotte', code: 'YT'}, 
  {name: 'Mexico', code: 'MX'}, 
  {name: 'Micronesia, Federated States of', code: 'FM'}, 
  {name: 'Moldova, Republic of', code: 'MD'}, 
  {name: 'Monaco', code: 'MC'}, 
  {name: 'Mongolia', code: 'MN'}, 
  {name: 'Montserrat', code: 'MS'}, 
  {name: 'Morocco', code: 'MA'}, 
  {name: 'Mozambique', code: 'MZ'}, 
  {name: 'Myanmar', code: 'MM'}, 
  {name: 'Namibia', code: 'NA'}, 
  {name: 'Nauru', code: 'NR'}, 
  {name: 'Nepal', code: 'NP'}, 
  {name: 'Netherlands', code: 'NL'}, 
  {name: 'Netherlands Antilles', code: 'AN'}, 
  {name: 'New Caledonia', code: 'NC'}, 
  {name: 'New Zealand', code: 'NZ'}, 
  {name: 'Nicaragua', code: 'NI'}, 
  {name: 'Niger', code: 'NE'}, 
  {name: 'Nigeria', code: 'NG'}, 
  {name: 'Niue', code: 'NU'}, 
  {name: 'Norfolk Island', code: 'NF'}, 
  {name: 'Northern Mariana Islands', code: 'MP'}, 
  {name: 'Norway', code: 'NO'}, 
  {name: 'Oman', code: 'OM'}, 
  {name: 'Pakistan', code: 'PK'}, 
  {name: 'Palau', code: 'PW'}, 
  {name: 'Palestinian Territory, Occupied', code: 'PS'}, 
  {name: 'Panama', code: 'PA'}, 
  {name: 'Papua New Guinea', code: 'PG'}, 
  {name: 'Paraguay', code: 'PY'}, 
  {name: 'Peru', code: 'PE'}, 
  {name: 'Philippines', code: 'PH'}, 
  {name: 'Pitcairn', code: 'PN'}, 
  {name: 'Poland', code: 'PL'}, 
  {name: 'Portugal', code: 'PT'}, 
  {name: 'Puerto Rico', code: 'PR'}, 
  {name: 'Qatar', code: 'QA'}, 
  {name: 'Reunion', code: 'RE'}, 
  {name: 'Romania', code: 'RO'}, 
  {name: 'Russian Federation', code: 'RU'}, 
  {name: 'RWANDA', code: 'RW'}, 
  {name: 'Saint Helena', code: 'SH'}, 
  {name: 'Saint Kitts and Nevis', code: 'KN'}, 
  {name: 'Saint Lucia', code: 'LC'}, 
  {name: 'Saint Pierre and Miquelon', code: 'PM'}, 
  {name: 'Saint Vincent and the Grenadines', code: 'VC'}, 
  {name: 'Samoa', code: 'WS'}, 
  {name: 'San Marino', code: 'SM'}, 
  {name: 'Sao Tome and Principe', code: 'ST'}, 
  {name: 'Saudi Arabia', code: 'SA'}, 
  {name: 'Senegal', code: 'SN'}, 
  {name: 'Serbia and Montenegro', code: 'CS'}, 
  {name: 'Seychelles', code: 'SC'}, 
  {name: 'Sierra Leone', code: 'SL'}, 
  {name: 'Singapore', code: 'SG'}, 
  {name: 'Slovakia', code: 'SK'}, 
  {name: 'Slovenia', code: 'SI'}, 
  {name: 'Solomon Islands', code: 'SB'}, 
  {name: 'Somalia', code: 'SO'}, 
  {name: 'South Africa', code: 'ZA'}, 
  {name: 'South Georgia and the South Sandwich Islands', code: 'GS'}, 
  {name: 'Spain', code: 'ES'}, 
  {name: 'Sri Lanka', code: 'LK'}, 
  {name: 'Sudan', code: 'SD'}, 
  {name: 'Suriname', code: 'SR'}, 
  {name: 'Svalbard and Jan Mayen', code: 'SJ'}, 
  {name: 'Swaziland', code: 'SZ'}, 
  {name: 'Sweden', code: 'SE'}, 
  {name: 'Switzerland', code: 'CH'}, 
  {name: 'Syrian Arab Republic', code: 'SY'}, 
  {name: 'Taiwan, Province of China', code: 'TW'}, 
  {name: 'Tajikistan', code: 'TJ'}, 
  {name: 'Tanzania, United Republic of', code: 'TZ'}, 
  {name: 'Thailand', code: 'TH'}, 
  {name: 'Timor-Leste', code: 'TL'}, 
  {name: 'Togo', code: 'TG'}, 
  {name: 'Tokelau', code: 'TK'}, 
  {name: 'Tonga', code: 'TO'}, 
  {name: 'Trinidad and Tobago', code: 'TT'}, 
  {name: 'Tunisia', code: 'TN'}, 
  {name: 'Turkey', code: 'TR'}, 
  {name: 'Turkmenistan', code: 'TM'}, 
  {name: 'Turks and Caicos Islands', code: 'TC'}, 
  {name: 'Tuvalu', code: 'TV'}, 
  {name: 'Uganda', code: 'UG'}, 
  {name: 'Ukraine', code: 'UA'}, 
  {name: 'United Arab Emirates', code: 'AE'}, 
  {name: 'United Kingdom', code: 'GB'}, 
  {name: 'United States', code: 'US'}, 
  {name: 'United States Minor Outlying Islands', code: 'UM'}, 
  {name: 'Uruguay', code: 'UY'}, 
  {name: 'Uzbekistan', code: 'UZ'}, 
  {name: 'Vanuatu', code: 'VU'}, 
  {name: 'Venezuela', code: 'VE'}, 
  {name: 'Viet Nam', code: 'VN'}, 
  {name: 'Virgin Islands, British', code: 'VG'}, 
  {name: 'Virgin Islands, U.S.', code: 'VI'}, 
  {name: 'Wallis and Futuna', code: 'WF'}, 
  {name: 'Western Sahara', code: 'EH'}, 
  {name: 'Yemen', code: 'YE'}, 
  {name: 'Zambia', code: 'ZM'}, 
  {name: 'Zimbabwe', code: 'ZW'} 
]
selectedcountry = [] #Getting the selected country 
os_list = [' ','Linux Ubuntu x64 x86','Linux Debian x64 x86','Linux Ubuntu arm 32','Linux Debian arm 32','Linux Ubuntu arm 64','Linux Debian arm 64'] #The list of the operaring system on the system 
osmem = []
#Password = "Rkj3548123" #Find the way to popup and get the password using this part as login into the system 
os.system("echo Hello"+"\t"+str(username)) #Getting the host name 
parent_dir = "/home/"+username+"/"
directory = ["Wifi_devices_connects","Robotics_nodes_json"]
mode = 0o777
# running the loop of make directory 
for dric in range(0,len(directory)):
   try:
      print("Now creating.....",str(directory[dric])) #Getting the directory created for the wifi config and robotics nodes json  
      path = os.path.join(parent_dir, directory[dric]) 
      os.mkdir(path,mode) #Make the path file for the wifi device connection data for choosing on the firmware devices generator
   except:
       print(directory[dric]+" directory  was created")
nodelist = os.listdir(os.path.join(parent_dir,directory[1]))  #getting the list of the robotics node json 
nodelist.append(" ")
storage_path = "/media/"+username   
generic_storage = os.listdir(storage_path) #Getting the list of the storate path 
generic_mem = []
generic_mem.append(" ")
generic_mem.append("Generic storage"+str(generic_storage))
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Getting the device name of the host 
devices = subprocess.check_output("arp -a",shell=True)
extract_devices = devices.decode('utf-8')
#print(extract_devices.split("wlo1"))
devices_list = extract_devices.split("wlo1")
hostname_mem = [] #Getting the list of the devices host name 
hostip_mem = [] #Getting the list of the devices host ip 
automateip_add = {}
hoste_selected =[]
host_password =[]
host_remote = [] #getting the remote host 
robothostname = []
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #Getting the wifi of the host 
wifi_mem = []
wifi_password = []
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#UDP socket client 

#fps,st,frames_to_count,cnt = (0,0,20,0) 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #Targetting command including firmware installation start and stop services and generate the config of the start at boot function 
command_exec = ["roboreactorfirmware.sh","./roboreactorfirmware.sh","sudo service supervisorctl start","sudo service supervisor stop","sudo supervisorctl reread","sudo service supervisor restart"]   #Command to activate the service automaticly and accessing the data inside the singleboard computer via ssh  
r = requests.get('https://raw.githubusercontent.com/KornbotDevUltimatorKraton/Firmwareoflaptop/main/FirmwareNongpuserver.sh')
firmware = requests.get('https://raw.githubusercontent.com/KornbotDevUltimatorKraton/Firmwareoflaptop/main/FirmwareNongpuserver.sh')
try:
  Create_file_storage = os.mkdir(storage_path+"/"+"Roboreactor",mode) #Current storage data # Creating the file inside the directory  
  Current_wifi_path = os.mkdir(storage_path+"/"+"Roboreactor"+"/"+"Wifi_scan",mode) #
except:
    print("File created inside the directory")
client_username = []
class MainWindow2(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow2, self).__init__()

        #Load the UI Page
        uic.loadUi('Roboticfirmwaregenerator.ui', self)
        self.setWindowTitle('Roboreactor firmware generator  User:'+"\t"+client_username[0]) #Getting the the client username from the new array
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.darkGray)
        self.setPalette(p)
        #Adding the roboreactor firmware generator function right here 
        self.setPalette(p)
        oImage = QImage("bg2_new.jpeg")
        oImage.scaled(300,200)
        #sImage = oImage.scaled(QSize(300,200))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)
        
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #Label pixmap camera 
        self.camera = self.findChild(QLabel,"label_5") # Getting this label to display the pixmap data 
        self.camera.setFixedSize(591,571) # Setting the size of the display image 
        #self.camera.setFixedSize(340,350) 
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        self.pushButton.clicked.connect(self.Writeimage)
        self.pushButton_2.clicked.connect(self.Remoteconfig) #Autore mote config 
        self.pushButton_3.clicked.connect(self.Start_remote_robot) #Start remote robot  
        self.pushButton_4.clicked.connect(self.Stop_remote_robot)  #Stop remote robot 
        self.pushButton_5.clicked.connect(self.Scan_host_machine) #Scan robot host
        self.pushButton_6.clicked.connect(self.Scan_wifi) #Scan wifi 
        self.pushButton_7.clicked.connect(self.Logout) #Logout function to setting the new login 
        self.pushButton_8.clicked.connect(self.Visual1) # Getting the camera 1 connect to open visual data on udp 
        self.pushButton_9.clicked.connect(self.Restart_services)
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Adding layout for the nodes display to configure the robot code 
        #Nodes view will display the data of the nodes from the json file input from the json downloaded from the website roboreactor online with the account data connected via the api 
        self.gridLayout = self.findChild(QGridLayout,"gridLayout")
        self.gridLayout.addWidget(QPushButton('1'),0,0)
        
        
        

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        #self.labelcam = self.findChild(QLabel,'label_5')
              #Set of commbobox selection function 
        self.combo1 = self.findChild(QComboBox, "comboBox")
        self.combo2 = self.findChild(QComboBox,"comboBox_2")
        self.combo3 = self.findChild(QComboBox,"comboBox_3")
        self.combo4 = self.findChild(QComboBox, "comboBox_4")
        self.combo5 = self.findChild(QComboBox,"comboBox_5")
        self.combo7 = self.findChild(QComboBox,"comboBox_7")

              #Text combonent 
        self.text6= self.findChild(QTextEdit,"textEdit_6")  #using the text edit 1 input the ssh text input  
        self.text3 = self.findChild(QLineEdit,"lineEdit_2")  #using the text edit 3 input the password of the host target 
        self.text3.setEchoMode(QLineEdit.Password) # Setting the qline edit for password mode 
        self.text4 = self.findChild(QLineEdit,"lineEdit")  #using the text edit 4 input the wifi password 
        self.text4.setEchoMode(QLineEdit.Password) # Setting the qline edit for password mode 
        self.text5 = self.findChild(QTextEdit,"textEdit_5")  #using the text edit 5 input the robot host hame 
             #Tab widget 
        self.tabwidget = self.findChild(QTabWidget,'tabWidget')  #using the TabWidget for the tab change the function
        self.cameras = self.findChild(QWidget,'Camera') #Getting the camera input mode 
        self.nodes_robot = self.findChild(QWidget,'nodes') #Getting the nodes input mode for nodes view data 
        
        #self.labelcam.setText("This is the first tab")
        #self.cameras.layout.addLayout(self.labelcam)
        #self.cameras.setLayout(self.cameras.layout)
        #self.tabWidget.addTab(,"Camera")
              #progressbard function   
        self.progress = self.findChild(QProgressBar,'progressBar') #using progress bar 
        self.progress.setMinimum(0)
        #Getting the maximum value input in dyanmics variant from the process feedback from the socket api communicate with the robotics host 
        self.progress.setMaximum(100) #Getting the number of the maximum value
        self.progress.setValue(0) #Move this progressbar into the function of the rest api feedback 
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #Action combolist function 
        self.combo1.activated.connect(self.Operatingsystem)
        self.combo1.addItems(os_list)
        self.combo2.activated.connect(self.Storage_generic)
        self.combo2.addItems(generic_mem)
        self.combo3.activated.connect(self.robotnodes)
        self.combo3.addItems([" "])
        self.combo3.addItems(nodelist) #Getting the robotics node json file 
        self.combo5.activated.connect(self.countrychoose)  #Getting the data from the list dictionary countr to display on the combobox 
        
       
        print(host_password,wifi_password,robothostname)
        for countries in range(0,len(country)):
                       print(country[countries])
                       dict_cc[country[countries].get('name')] = country[countries].get('code')
        print(dict_cc)
        self.combo5.addItems(list(dict_cc))  #Adding the country into the list item of the combobox
        self.combo4.activated.connect(self.hostname_data)
        print("Start scanning the host machine") #
        lst = map_network()
        print(lst)
        try:
              #automateip_add.clear()
              for r in range(0,len(lst)):
                   host = socket.gethostbyaddr(lst[r])
                   print(host[0],host[2])
                   automateip_add[host[0]] = host[2] #create the new list of the host scanner  
                   #Fixed the unscannable issue now able to scanning at instance scanning mode 
        except:
               print("Unknown host")
        for ri in range(0,len(devices_list)-1):
            print(devices_list[ri].split(" "))
            origin_list = devices_list[ri].split(" ")[0]
            getdatahost = devices_list[ri].split(" ")[1]
            gethostip = getdatahost.split("(")[1].split(")")[0]
            print(origin_list,getdatahost.split("(")[1].split(")")[0])
            hostname_mem.append(origin_list) #Get the hostname of the devices 
            automateip_add[origin_list] = gethostip #Getting the autolist of the ip address  #Create the automate list update 
        self.combo4.addItems(hostname_mem)#Getting the host mem data into the combo box  
        #self.combo6.addItems(hostip_mem) #Getting the ip address of the host target selected
        print(automateip_add)
        self.combo7.activated.connect(self.wifissid)
        
        for wifi_R in range(0,1):
                     getwifi = subprocess.check_output("nmcli dev wifi",shell=True) 
                     dataframe = getwifi.decode('utf-8')
                     #print(type(dataframe))
                     #print(dataframe)
                     file = open("currentwifi.csv",'w')
                     file.write(dataframe)
                     file.close()
                     #df = pandas.DataFrame(dataframe, columns=['SSID', 'SIGNAL'])
                     df = pd.read_csv('currentwifi.csv')
                     #print("Reading the saving current available wifi")
                     print(df)
                     index = df.index
                     print(index)
                     listdata = list(df.columns.values)
                     print(listdata)
                     print(listdata[0].split(" ")) #recreate the columns separate from one big column
                     print(df[listdata[0]].values[0])
                     print(len(index))
                     for wifi in range(0,len(index)-1):
                             getting_str =  df[listdata[0]].values[wifi].split(" ") #split the wifi data to get the wifi name and signal strength to choosing the best connection 
                             print(getting_str[10])
                             if len(wifi_mem) < len(index):
                                           wifi_mem.append(getting_str[10]) #getting the mem wifi name 
                             if len(wifi_mem) > len(index):
                                   terminal = len(wifi_mem)-len(index)
                                   for wifilist in range(len(index),terminal):
                                             wifi_mem.remove(wifi_mem[wifilist]) #remove the len of the index if the length is over 
                     self.combo7.addItems([" "]) #Getting the blank list on the top to be able to choosing the data in the combobox later 
                     self.combo7.addItems(wifi_mem) #getting the list of wifi memory
                     print(wifi_mem)
    
    def Visual1(self): 
           # Camerafunction for the UDP receiver communication       
           #UDP socket client
           print("Connecting the ip camera") 
           self.Worker1 = Worker1() 
           self.Worker1.start()
           self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
    def ImageUpdateSlot(self, Image):
            self.pixmap = QPixmap.fromImage(Image)
            self.camera.setPixmap(self.pixmap) 
    def wifissid(self,wifi_index):
             print(wifi_mem[wifi_index])
             if len(network_name) < len(wifi_mem):
                   network_name.append(wifi_mem[wifi_index-1])  #Getting the wifi mem on the list of the network name to generate the wifi configuretion on sd card 
             if len(network_name) >1:
                   network_name.remove(network_name[0]) #remove the network name from the list if out of range 
             print(network_name)      
    def hostip_data(self,hostip_index):
             print(hostip_mem[hostip_index-1])    
    def hostname_data(self,host_index):
             print(hostname_mem[host_index]) #Getting the host index
             print(automateip_add.get(hostname_mem[host_index]))
             if str(automateip_add.get(hostname_mem[host_index])) not in hostip_mem:
                       hostip_mem.append(automateip_add.get(hostname_mem[host_index]))
             if len(hostip_mem) > 1:
                       hostip_mem.remove(hostip_mem[0])

    def Storage_generic(self,index_storage):
                print(generic_mem[index_storage])
    def robotnodes(self,nodes_list):
                print(nodelist[nodes_list])
    def Operatingsystem(self,osp):
             print(os_list[osp])
             if osmem !=[]:
                   osmem.append(os_list[osp])
             if len(osmem) > 1:
                  osmem.remove(osmem[len(osmem)-1]) 
             print(osmem)    
    def countrychoose(self,countries_cc):
                 #Getting the breviation from key
              try:
                 print(list(dict_cc)[countries_cc])
                 get_extracted = list(dict_cc)[countries_cc]
                 selected_cc = dict_cc.get(get_extracted)
                 print(selected_cc)
                 selectedcountry.append(selected_cc) #Getting the country breviation for the memory function              
                 print("Store country breviation successfully....")
              except: 
                   print("Store country breviation error")
    def Remoteconfig(self):
       print("Operating remote config on the robot......") #Operating the remote config of the robot
       if len(robothostname) <=0:
                    robothostname.append(self.text5.toPlainText()) #Robot hostname for the remote operating robot auto configuretion and setting service 
       if len(robothostname) >1:
                    robothostname.remove(robothostname[0])
       if len(host_password) <=0:
                 host_password.append(self.text3.text()) #Host password for the ssh remote 
       if len(host_password) >1:
                 host_password.remove(host_password[0])
       try:     
           print(robothostname[0],hostip_mem[0],host_password[0])          
           with SSHClient() as client:
                     client.set_missing_host_key_policy(AutoAddPolicy())
                     print(robothostname)
                     print(hostip_mem[0],robothostname[0],host_password[0])
                     client.connect(hostname=str(hostip_mem[0]),username=str(robothostname[0]),password=str(host_password[0]),look_for_keys=False) #Getting all the data from the host ip,host_name and the other hostmachine to connect 
                     command = ["ls","python3 wifiscanner.py","lsusb"]
                     #Access remote command with sodo combine password generated working 
                     #Fix your host password into the remote machine password
                     try:
                         print("Remote chmod permission")
                         stdin, stdout, stderr = client.exec_command("sudo -S <<< " +str(host_password[0])+" chmod +x "+command_exec[0],get_pty=True)
                         lines = stdout.readlines()
                         print(lines)
                         #Messagebox here to display the progress bar 
                        
                         msgbox = QtWidgets.QMessageBox()
                         msgbox.setText('Finish robogenerator firmware generated')
                         msgbox.setTextInteractionFlags(QtCore.Qt.NoTextInteraction) # (QtCore.Qt.TextSelectableByMouse)
                         stdin, stdout, stderr = client.exec_command(command[0],get_pty=True)
                         lines = stdout.readlines()
                         for dataremote in range(0,len(lines)):   
                              msgbox.setDetailedText(lines[dataremote]+"\n")
                         msgbox.exec() 
                         #From the lines output list array seeking the cannot access as the trigger word for git installation on the system to prepare the remote firmware installation process 
                         #Reding the bash script in the list array to modify the firmware percentage report firmware installation progress 
                     except:
                         print("Remote chmod permission fail")
                     
       except: 
            print("You haven't upload firmware and config to the SD card")
    def Scan_wifi(self): #Button input function for the wifi scanning 
           #Input the 1 loop wifi scanner here to operating at search mode 
           print('Mapping wifi") #Start mapping wifi')  
           for wifi_R in range(0,1):
                     getwifi = subprocess.check_output("nmcli dev wifi",shell=True) 
                     dataframe = getwifi.decode('utf-8')
                     #print(type(dataframe))
                     #print(dataframe)
                     file = open("currentwifi.csv",'w')
                     file.write(dataframe)
                     file.close()
                     #df = pandas.DataFrame(dataframe, columns=['SSID', 'SIGNAL'])
                     df = pd.read_csv('currentwifi.csv')
                     #print("Reading the saving current available wifi")
                     print(df)
                     index = df.index
                     print(index)
                     listdata = list(df.columns.values)
                     print(listdata)
                     print(listdata[0].split(" ")) #recreate the columns separate from one big column
                     print(df[listdata[0]].values[0])
                     print(len(index))
                     for wifi in range(0,len(index)-1):
                             getting_str =  df[listdata[0]].values[wifi].split(" ") #split the wifi data to get the wifi name and signal strength to choosing the best connection 
                             print(getting_str[10])
                             if len(wifi_mem) < len(index):
                                           wifi_mem.append(getting_str[10]) #getting the mem wifi name 
                             if len(wifi_mem) > len(index):
                                   terminal = len(wifi_mem)-len(index)
                                   for wifilist in range(len(index),terminal):
                                             wifi_mem.remove(wifi_mem[wifilist]) #remove the len of the index if the length is over 
                             self.progress.setValue((wifi/(len(wifi_mem)-1))*100) # Testing the progressbar using the scanning process of the wifi 
    def Start_remote_robot(self): 
           #Start the service robot to operating at boot 
           print("Start service robot to operating at boot services") # Start running the robot software 
    def Restart_services(self): 
           print("Restart service robot operating at boot services") # Restart the robot software 
    def Stop_remote_robot(self):
           #Stop the service robot to operating at boot 
           print("Stop service robot to operating at boot services") # Stop running the robot software 
    def Scan_host_machine(self):
           #Scan the hostmachine 
           print("Start scanning the host machine") #
           lst = map_network()
           print(lst)
           try:
              #automateip_add.clear()
              for r in range(0,len(lst)):
                   host = socket.gethostbyaddr(lst[r])
                   print(host[0],host[2])
                   automateip_add[host[0]] = host[2] #create the new list of the host scanner  
                   #Fixed the unscannable issue now able to scanning at instance scanning mode 
           except:
               print("Unknown host")
    def Logout(self):
          print("Logging out from the system")
          self.w = MainWindow()
          self.w.show() 
          self.hide() 
    def Writeimage(self):
           
            if len(wifi_password) <=0:
                     wifi_password.append(self.text4.toPlainText()) #Network password for the wifi config session
            if len(wifi_password) >1:
                     wifi_password.remove(wifi_password[0]) #remove the first password from the list

            print(host_password,wifi_password)
            if memwrite ==[]:
                    memwrite.append("Write") #Getting the status write 
            if len(memwrite) >1:
                   memwrite.remove(memwrite[len(memwrite)]) #remove the memwrite with over lenght status writing on the array 
            print("Start writing the firmware on boot........") #Display the status on the logo 
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                 #Start writing the firmware
                 #Selecte case of the operating system to upload the firmware into the 
            #This will be using the list combobox to select the SBC type tp choosing the image writer selection capability 
            #Accessing the boot directory of the raspberrypi_boot directory   
            target_rpi = ["boot","rootfs","/home/pi","system-boot","writable"]   #Getting the into the directory of the inner file 
            #Checking there is boot  
            list_seek_boot = os.listdir(PATH_SD_CARD) #Seeking the target file 
            print("Seek dir",list_seek_boot) #Getting the list seek boot 
            print(network_name[0])
            print(wifi_password[0])
            for re in range(0,len(list_seek_boot)):
                                      #Single Board computer will be choosing from the existing nodes json data to choosing the data from the websize api connecting with the back end 
                        
                                      #Raspberrypi 
                                      # Write on the rpi debian function  condition                       
                                      if list_seek_boot[re] == str(target_rpi[1]):
                                                  print("Found "+str(list_seek_boot[re])+" Now operating firmware injection.......")
                                                  bashwriter = open(PATH_SD_CARD+"/"+list_seek_boot[re]+target_rpi[2]+"/"+"roboreactorfirmware.sh",'w') #Write the firmware directly into the SD card host
                                                  bashwriter.write(r.text) #Getting data inject into the sd card write directly into the user directory and create the file 
                                                  bashwriter.close() 
                                                  #os.system("sudo -S <<< "+str(host_password[0]) +" chmod +x "+PATH_SD_CARD+"/"+list_seek_boot[re]+target_rpi[2]+"/"+"roboreactorfirmware.sh")
                                      if list_seek_boot[re] == str(target_rpi[0]):
                                                  print("Found "+str(list_seek_boot[re])+" Now operating setting SSH and WiFi.......")
                                                  #Writing the file into the path
                                                  filessh = open(PATH_SD_CARD+"/"+list_seek_boot[re]+"/"+"ssh","w")  #Write the ssh file into the boot directory
                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                  filessh.write(" ")
                                                  filessh.close() #Close the file writer after finish writing the file ssh for enable ssh command 

                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                  filewpa_supplicant = open(PATH_SD_CARD+"/"+list_seek_boot[re]+"/"+"wpa_supplicant.conf",'w')
                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 
                                                  print(selectedcountry)
                                                  filewpa_supplicant.write("country="+selectedcountry[0]+"\n") #Getting the country
                                                  filewpa_supplicant.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev"+"\n")
                                                  filewpa_supplicant.write("update_config=1"+"\n")
                                                  filewpa_supplicant.write("network={"+"\n")
                                                  SSIDs = '"' + network_name[0] +'"'
                                                  SIDpass = '"' + wifi_password[0] + '"'
                                                  filewpa_supplicant.write("ssid="+SSIDs+"\n")  #Getting the name of the network from the combobox list SSID password
                                                  filewpa_supplicant.write("psk="+SIDpass+"\n") #Getting the password from the text input 
                                                  filewpa_supplicant.write("key_mgmt=WPA-PSK"+"\n") #Getting key wpa 
                                                  filewpa_supplicant.write("}"+"\n")  
                                                  filewpa_supplicant.close()
                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                  #Fix the cmd code 
                                                  cmdfileconfig = open(PATH_SD_CARD+"/"+list_seek_boot[re]+"/"+"cmdline.txt",'w') 
                                                  cmdfileconfig.write("root=PARTUUID=f4481065-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet init=/usr/lib/raspi-config/init_resize.sh splash plymouth.ignore-serial-consoles") 
                                                  cmdfileconfig.close() #Close file after finished writing the configuretion 
                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                                  #Fix the config boot 
                                                  configfile = open(PATH_SD_CARD+"/"+list_seek_boot[re]+"/"+"config.txt",'w') 
                                                  configfile.write("#Uncomment some or all of these to enable the optional hardware interfaces")
                                                  configfile.write("dtparam=i2c_arm=on"+"\n")
                                                  configfile.write("#dtparam=i2s=on"+"\n")
                                                  configfile.write("dtparam=spi=on"+"\n")
                                                  configfile.write("dtparam=audio=on"+"\n")
                                                  configfile.write("[pi4]"+"\n")
                                                  configfile.write("#Enable DRM VC4 V3D driver on top of the dispmanx display stack"+"\n")
                                                  configfile.write("dtoverlay=vc4-fkms-v3d"+"\n")
                                                  configfile.write("max_framebuffers=2"+"\n")
                                                  configfile.write("[all]"+"\n")
                                                  configfile.write("#dtoverlay=vc4-fkms-v3d"+"\n")
                                                  configfile.write("start_x=1"+"\n")
                                                  configfile.write("gpu_mem=128"+"\n")
                                                  configfile.write("enable_uart=1"+"\n")
                                                  configfile.close() #Close the file writer after finish writing 

                                                  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                    
                                      #Write on the rpi ubuntu function condition 
                                      if list_seek_boot[re] == str(target_rpi[3]):                                
                                                   print("system-boot",list_seek_boot[re]) #getting the system boot 
                                                   

                                      if list_seek_boot[re] == str(target_rpi[4]):
                                                   print("writable",list_seek_boot[re]) #getting the system writable directory to inject the firmware on the system to run 

      
class MainWindow(QtWidgets.QMainWindow):
   
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('Loginpage.ui', self)
        self.setWindowTitle('Welcome to roboreactor User:'+"\t"+username)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.darkGray)
        self.setPalette(p)
        oImage = QImage("kobuki_new.jpg")
        oImage.scaled(300,200)
        #sImage = oImage.scaled(QSize(300,200))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)
        self.pushButton.clicked.connect(self.Login) #button login 
        self.text = self.findChild(QTextEdit,"textEdit") #Getting the text edit input the username on the system
        self.text2 = self.findChild(QLineEdit,"lineEdit") #Getting the password input
        self.text2.setEchoMode(QLineEdit.Password) #QLine edit for hiding the password 
        self.label.setStyleSheet("color:white") 
        self.label_2.setStyleSheet("color:white")
        self.label_3.setStyleSheet("color:white")
        query()   #Query data database 
        #update()  #Update data rethrieve the data 
    def Login(self):
            print("Logging into the database......")
            usernamedata = self.text.toPlainText()
            passworddata = self.text2.text() # This is the QLineEdit for the text hiding password data 
            #self.text2.setEchoMode(QLineEdit.Password)
            print(usernamedata,passworddata) #Getting the username and password
            #reading the cloud database and activate the new window 
            #DATABASE_URL = os.environ['DATABASE_URL']
            #conn = psycopg2.connect(DATABASE_URL, sslmode='require') 
            conn = psycopg2.connect(
               DATABASE_URL,
               sslmode='require',
            )
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS customers
            (index Text,
            first_name Text,
            last_name Text,
            e_mail Text,
            password Text,
            address Text,
            payment_status Text,
            cardholder Text,
            schedule Text,
            recharge Text);''')
            # Create a cursor
            c = conn.cursor()
            #Grab stuff from online database 
            c.execute("SELECT*FROM customers")
            records = c.fetchall() 
            print(records[0])
            print("Amount of customers:",len(records)) #Find the amout of the customer
            am_customers = len(records)
            for rec in range(0,len(records)):
                   #print(records[rec][3],records[rec][4])
                   if usernamedata == records[rec][3]:
                       print("Username correct!")
                       if passworddata == records[rec][4]:
                               print("Password correct!")
                               #Create the title username data 
                               if client_username != []: 
                                  client_username.clear() 
                               if client_username == []:
                                  print("Getting the name record into the client username array to get the new title name")
                                  client_username.append(str(records[rec][1]) +"\t"+str(records[rec][2])) #Working user title created on the gui 
                               self.w = MainWindow2()
                               self.w.show() 
                               self.hide() 
                               break
                   
            conn.close()

#Scan host devices name in the local network 
def pinger(job_q, results_q):
    """
    Do Ping
    :param job_q:
    :param results_q:
    :return:
    """
    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def map_network(pool_size=255):
    """
    Maps the network
    :param pool_size: amount of parallel ping processes
    :return: list of valid ip addresses
    """

    ip_list = list()

    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

    for p in pool:
        p.start()

    # cue hte ping processes
    for i in range(1, 255):
        jobs.put(base_ip + '{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    # collect he results
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)

    return ip_list
class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        
        #UDP socket client 
        BUFF_SIZE = 65536
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        host_name = socket.gethostname()
        message = b'Hello'
        port = 9800
        client_socket.sendto(message,(hostip_mem[0],port))
        fps,st,frames_to_count,cnt = (0,0,20,0) 
        self.ThreadActive = True
        while self.ThreadActive:
        
            packet,_ = client_socket.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet,' /')
            npdata = np.fromstring(data,dtype=np.uint8)
            Image = cv2.imdecode(npdata,1)
            Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
            Image = cv2.putText(Image,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),1)
            FlippedImage = cv2.flip(Image, 1)
            ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(591, 571, Qt.KeepAspectRatio) 
            self.ImageUpdate.emit(Pic)
            #cv2.imshow("Receiving video",Image)
            key = cv2.waitKey(1) & 0xFF 
            if key == ord('q'):
                client_socket.close() 
                break 
            
            if cnt == frames_to_count:
                     try:
                         fps = round(frames_to_count/time.time()-st) 
                         st=time.time() 
                         cnt=0
                     except:
                         pass 
            cnt+=1              
                
    def stop(self):
        self.ThreadActive = False
        self.quit()
def query():
      #Getting the host url https://dashboard.heroku.com/apps 
      #DATABASE_URL = os.environ['DATABASE_URL']
      #conn = psycopg2.connect(DATABASE_URL, sslmode='require') 
      conn = psycopg2.connect(
               DATABASE_URL,
               sslmode='require',
      )
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS customers
      (index Text,
      first_name Text,
      last_name Text,
      e_mail Text,
      password Text,
      address Text,
      payment_status Text,
      Cardholder Text,
      schedule Text,
      Recharge Text);
      ''')
      conn.commit()
      conn.close()
      

def main():
    app = QtWidgets.QApplication(sys.argv)
     
    main = MainWindow()
    main.show()
    
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
     main()
     