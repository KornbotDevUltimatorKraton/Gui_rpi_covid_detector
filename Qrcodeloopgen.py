import qrcode # import qrcode for the qrcode generator
import os 
genpath = "/home/kornbotdev/CovidDetectorGui/Qrgenerator/"
try:
   mode = 0o775
   os.mkdir("/home/kornbotdev/CovidDetectorGui/Qrgenerator/",mode) 
except: 
   print("Directory was created") 
for i in range(5001,5021): 
     img = qrcode.make(str(i))  #Adding the data list from the add list function here
     type(img)  # qrcode.image.pil.PilImage
     img.save(genpath+str(i)+".png")
