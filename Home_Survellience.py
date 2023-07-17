#Import the Open-CV extra functionalities
import cv2
import time
from time import sleep
import datetime
import smtplib, email, os
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import RPi.GPIO as GPIO

import datetime
capture_duration = 10
PIR_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
   

#*********************************************** Email parameters *************************************************
subject='Security Alert: A motion has been detected'
bodyText="""\
Hi,

A motion has been detected in your room.
Please check the attachement sent from rasperry pi security system.

Regards
AS Tech-Workshop

"""
SMTP_SERVER='smtp-mail.outlook.com'
SMTP_PORT=587
USERNAME='openlab115@outlook.com'
PASSWORD='ahpd@115'
RECIEVER_EMAIL='openlab115@gmail.com'

#This is to pull the information about what each object is called
classNames = []
classFile = "/home/r7/Desktop/Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")


#This is to pull the information about what each object should look like
configPath = "/home/r7/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/r7/Desktop/Object_Detection_Files/frozen_inference_graph.pb"

#This is some set up values to get good results
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

#This is to set up what the drawn box size/colour is and the font/size/colour of the name tag and confidence label   
def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
#Below has been commented out, if you want to print each sighting of an object to the console you can uncomment below     
#print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className=='cat':
                print('not a person')
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0] +10,box[1] +30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0] +200,box[1] +30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                
                
            if className=='person':
                print("person found")
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0] +10,box[1] +30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0] +200,box[1] +30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    filename_part1="surveillance"
                    file_ext=".avi"
                    now = datetime.datetime.now()
                    current_datetime = now.strftime("%d-%m-%Y_%H:%M:%S")
                    filename=filename_part1+"_"+current_datetime+file_ext
                    filepath="/home/r7/Desktop/Object_Detection_Files/"
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    out = cv2.VideoWriter(filepath+filename,fourcc, 20.0, (640,480))

                    start_time = time.time()
                    while( int(time.time() - start_time) < capture_duration ):
                        ret, frame = cap.read()
                        if ret==True:
                            out.write(frame)
                            
                    send_email(filename,filepath)


                    
    
    return img,objectInfo
def send_email(filename,filepath):
 message=MIMEMultipart()
 message["From"]=USERNAME
 message["To"]=RECIEVER_EMAIL
 message["Subject"]=subject

 message.attach(MIMEText(bodyText, 'plain'))
 attachment=open(filepath+filename, "rb")

 mimeBase=MIMEBase('application','octet-stream')
 mimeBase.set_payload((attachment).read())

 encoders.encode_base64(mimeBase)
 mimeBase.add_header('Content-Disposition', "attachment; filename= " +filename)

 message.attach(mimeBase)
 text=message.as_string()

 session=smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
 session.ehlo()
 session.starttls()
 session.ehlo()

 session.login(USERNAME, PASSWORD)
 session.sendmail(USERNAME, RECIEVER_EMAIL, text)
 session.quit
 print("Email sent")

#Below determines the size of the live feed window that will be displayed on the Raspberry r7 OS
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    cap.set(3,640)
    cap.set(4,480)
 
    #cap.set(10,70)
 
#Below is the never ending loop that determines what will happen when an object is identified.    
    while True:
            if GPIO.input(PIR_PIN):
                print("Motion detected")
                motion_detected = True
                success, img = cap.read()
    #Below provides a huge amount of controll. the 0.45 number is the threshold number, the 0.2 number is the nms number)
                result, objectInfo = getObjects(img,0.7,0.2)
            #print(objectInfo)
                cv2.imshow("Output",img)
                cv2.waitKey(1)
                sleep(0.5)
            
            else:
                print("Motion stopped")
                motion_detected = False
                sleep(0.5)
            
