import cv2
from simple_facerec import SimpleFacerec
import time
import os
import OpenCVModule as htm

import speechrecognition as sp
#import controller as cnt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import time
import pyttsx3


engine = pyttsx3.init()
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate+10)
engine.setProperty('voice', voices[1].id)
recognizer=sr.Recognizer()
microphone=sr.Microphone()

def speak (query):
    engine.say(query)
    engine.runAndWait()

def recognize_speech():
    with microphone as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
    respose=""
    speak("Identifying speech..")
    try:
        response=recognizer.recognize_google(audio)
    except:
        response ="Error"
    return response


cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://contactlessvending-default-rtdb.firebaseio.com/",
    'storageBucket':"contactlessvending.appspot.com"
})


sfr=SimpleFacerec()
sfr.load_encoding_images("images/")

file_name=""
register=0
authloop=-1
cntr=1
bucket=storage.bucket()
mainCounter=0
selectionSpeed=9
wCam,hCam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
name=0
resize_img=0
modePositions=[(1136,196),(1000,384),(1136,581),(1050,384)]
counter=0
counterPause=0
selectionList=[-1,-1,-1]
AuthenticationList=[-1]
ImgBackground=0
modeType=4
selections=-1
ImgStudent=[]
times=1
mode0counter=1
mode1counter=1
mode2counter=1

detector=htm.handDetector(detectionCon=0.75)
tipIds=[4,8,12,16,20]

#importing all moodes to list
folderPathModes="Resources/Modes"
listImgModesPath=os.listdir(folderPathModes)
listImgModes=[]
for imgModePath in listImgModesPath:
     listImgModes.append(cv2.imread(os.path.join(folderPathModes,imgModePath)))

#importing all the icons to list
folderPathIcons="Resources/Icons"
listImgIconsPath=os.listdir(folderPathIcons)
listImgIcons=[]
for imgIconsPath in listImgIconsPath:
     listImgIcons.append(cv2.imread(os.path.join(folderPathIcons,imgIconsPath)))




def Output():
    global pTime
    global ImgBackground
    global cntr
    global times
    global mode0counter
    global mode1counter
    global mode2counter
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(frame,f'FPS:{int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)
    if authloop==1:
     if name=="Devansh":
          cv2.putText(frame,"Welcome Devansh",(200,450),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
     elif name=="Unknown":
          cv2.putText(frame,"Unknown Face",(200,450),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
     else:
          cv2.putText(frame,"No Face Detected",(200,450),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
     
   
    ImgBackground=cv2.imread("Resources\Background.jpg")
    ImgBackground[139:139+480,50:50+640]=frame
    ImgBackground[0:720,847:1280]=listImgModes[modeType]
    if authloop==1:
        ImgBackground[150:150+245,953:953+225]=resize_img
    if authloop==2:
        cv2.putText(ImgBackground,("Name: "+ f'{file_name}'),(890,500),cv2.FONT_HERSHEY_COMPLEX ,1,(0,0,0),2)
        cv2.putText(ImgBackground,"Speak your name",(865,550),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
    if mainCounter!=0 and name!="Unknown" and authloop==1 :
     cv2.putText(ImgBackground,str("Credits: "+str(studentInfo['Credits'])),(980,450),cv2.FONT_HERSHEY_COMPLEX ,1,(0,0,0),2)
     cv2.putText(ImgBackground,str("Name: "+ str(studentInfo['name'])),(890,500),cv2.FONT_HERSHEY_COMPLEX ,1,(0,0,0),2)
     cv2.putText(ImgBackground,"Show 4 to Confirm Your Identity",(865,550),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
     cv2.putText(ImgBackground,"Show 2 to register as new user",(865,620),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
     cv2.putText(ImgBackground,"Show 5 to Browse the web",(865,690),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,0),2)
     times=times+1
     
     if times==3:
        speak("show 4 fingers to confirm your identity")
        speak("show 2 fingers to Register new user")
        speak("show 5 fingers to browse the Web")
    
        
     ImgBackground[150:150+245,953:953+225]=ImgStudent            #student image from databse
    if modeType==0 and mode0counter==1:
        speak("choose the  destination")
        mode0counter=mode0counter+1
    if modeType==1 and mode1counter==1:
        speak("choose no of tickets")
        mode1counter=mode1counter+1
    if modeType==2 and mode2counter==1:
        speak("confirm your choice")
        mode2counter=mode2counter+1
    if authloop==0 and selectionList[0]!=-1 and selectionList[1]!=-1 and selectionList[2]!=-1:
         cv2.putText(ImgBackground,str("credits: "+ str(studentInfo['Credits'])),(980,550),cv2.FONT_HERSHEY_COMPLEX ,1,(0,0,0),2)
         print("oolah")
     #     if cntr==1 and selectionList[0]==1 and selectionList[1]==2 and selectionList[2]==3:
     #       cntr=2                              #SERVO CODE
     #       cnt.led(selectionList[1])
     #     elif cntr==1 and selectionList[0]==2 and selectionList[1]==2 and selectionList[2]==2:
     #         cntr=2                              #SERVO CODE
     #         cnt.led1(selectionList[0]+5)     # pin 6,7,8
           
    

    ###############login page animation
    if selections==2 and authloop==1:
         cv2.ellipse(ImgBackground,(1050,650),(100,0),180,0,counter*4.6,(255,0,0),15)
    elif selections==4:
        cv2.ellipse(ImgBackground,(1050,580),(100,0),180,0,counter*4.6,(0,0,255),15)
    elif selections==-1:
        pass                          #to remove dot at position -1
    elif authloop==0:                  #elipse for selections
        cv2.ellipse(ImgBackground,modePositions[selections-1],(103,103),0,0,counter*selectionSpeed,(0,153,0),15)
    #iconlist



    if selectionList[0]!=-1:
     ImgBackground[636:636+65,133:133+65]=listImgIcons[selectionList[0]-1]  
    if selectionList[1]!=-1:
     ImgBackground[636:636+65,340:340+65]=listImgIcons[2+selectionList[1]]
    if selectionList[2]!=-1:
     ImgBackground[636:636+65,542:542+65]=listImgIcons[5+selectionList[2]]

    cv2.imshow("Background",ImgBackground)
    key=cv2.waitKey(1)
    if key==27:
        cap.release()
        cv2.destroyAllWindows()  
    
#authentication
while True:
    while AuthenticationList[0]!=4 and AuthenticationList[0]!=5 and AuthenticationList[0]!=2 or AuthenticationList[0]==-1 :
        print("hoola")
        authloop=1
        ret,frame=cap.read()
        face_location,face_names=sfr.detect_known_faces(frame)
        for face_loc,name in zip(face_location,face_names):              
            print(name)
            name1=name    
            if mainCounter==0:
                    mainCounter=1
        if mainCounter!=0 and name!="Unknown":
            if mainCounter==1:
                #Data from Database
                studentInfo=db.reference(f'Students/{name}').get()
                print(studentInfo) 
                #Image from database
                blob=bucket.get_blob(f'images/{name}.jpg')
                array=np.frombuffer(blob.download_as_string(),np.uint8)
                ImgStudent1=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                ImgStudent=cv2.resize(ImgStudent1,(225,245),interpolation = cv2.INTER_AREA)
                #update credits
            #    if selectionList==[]
            #    ref=db.reference(f'Students/{name}')
            #    studentInfo['Credits']+=10  
            #    ref.child('Credits').set(studentInfo['Credits'])
        
        Output()
        if name=="Unknown":
            print("Unknown face")
        while name=="Devansh" and AuthenticationList[0]==-1 :
                
                
                success,frame=cap.read()
                frame=detector.findHands(frame)
                lmList=detector.findPosition(frame,draw=False)
                            # print(lmList)             
                if len(lmList)!=0 and counterPause==0 and modeType<5:
                    fingers=[]
                    #thumb
                    if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
                            fingers.append(1)
                    else:
                            fingers.append(0)
                    #fingers
                    for id in range(1,5):

                        if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    # print(fingers)
                    totalFingers=fingers.count(1)
                    print(fingers) 

                #  if fingers==[0,1,0,0,0]:
                #       if selections!=1:
                #          counter=1
                #       selections=1
                    if fingers==[0,1,1,1,1]:
                        if selections!=4:
                            counter=1
                        selections=4      
                    elif fingers==[0,1,1,0,0]:
                        if selections!=2:
                            counter=1
                        selections=2   
                    elif fingers==[1,1,1,1,1]:
                        if selections!=5:
                            counter=1
                        selections=5                                
                    else:
                        selections=-1
                        counter=0
                    
                    #print(selections)
                    if counter>0:
                        counter+=1
                        #  print(counter)                     
                        if counter*selectionSpeed>360:
                            AuthenticationList[0]=selections                         
                            counter=0
                            selections=-1
                            counterPause=1
                            #  print(modeType)
                #pause function  
                if counterPause>0:
                    counterPause+=1
                    if counterPause>40:
                        counterPause=0
                print(AuthenticationList)
                
            
                Output()
        if name!="Devansh" and name!="Unknown":
            print("No Face Detected")




        ###########################################

    exit=0
    while AuthenticationList[0]==5 and exit!=1:
        
        
        driver = webdriver.Chrome()
        driver.maximize_window()
        time.sleep (1)
        speak ("Hello User! I am now online..")
        while True:
            speak("How can I help you?")
            voice= recognize_speech ().lower()
            print(voice)
            if 'open google' in voice:
                speak ('Opening google..')
                driver.execute_script("window.open('');")
                window_list = driver.window_handles
                driver.switch_to.window(window_list[-1])
                driver.get('https://google.com')
            elif 'search google' in voice:
                while True:
                    speak('What do you want to search on google...')
                    query=recognize_speech()
                    if query!='Error':
                        break
                element = driver.find_element("name","q")
                element.clear()
                element.send_keys(query)
                element.send_keys(Keys.RETURN)
            if 'open youtube' in voice:
                speak ('Opening youtube..')
                driver.execute_script("window.open('');")
                window_list = driver.window_handles
                driver.switch_to.window(window_list[-1])
                driver.get('https://youtube.com')
            elif 'search youtube' in voice:
                while True:
                    speak('What do you want to search on Youtube...')
                    query=recognize_speech()
                    speak(f'searching {query} on youtube')
                    if query!='Error':
                        break
                element = driver.find_element("name","search_query")
                element.clear()
                element.send_keys(query)
                element.send_keys(Keys.RETURN)
            elif 'switch tab' in voice:
                num_tabs=len(driver.window_handles)
                cur_tab=0
                for i in range(num_tabs):
                    if driver.window_handles[i]==driver.current_window_handle:
                        if i !=num_tabs-1:
                            cur_tab=i+1
                            break
                driver.switch_to_window(driver.window_handles[cur_tab])
            elif 'close tab' in voice:
                speak('closing current Tab...')
                driver.close()
            elif 'go back' in voice:
                speak('Going Back')
                driver.back()
            elif 'go forward' in voice:
                speak('Going forward')
                driver.forward()
            elif 'exit' in voice:
                speak('exiting, Goodbye...')
                driver.quit()
                exit =1
                break                
            else:
                speak('sorry thats not a valid command')
            time.sleep(1)
            
    while AuthenticationList[0]==2:
        authloop=2
        cam = cv2.VideoCapture(0)
        counter=0
        # If image will detected without any error, 
        # show result
        UserPath="user_img"
        image_filename ="devansh.png"
        image_path = os.path.join(UserPath, image_filename)
       


        while AuthenticationList[0]==2 :
            
            ret,frame=cam.read()
            # showing result, it take frame name and image 
            # output
            cv2.putText(frame,"stand straight for pic",(200,450),cv2.FONT_HERSHEY_COMPLEX_SMALL ,1,(0,0,255),2)
            
            key=cv2.waitKey(1)
            if key==27:
                cam.release()
                cv2.destroyAllWindows() 
                break
            counter+=1
            print(counter)
            Output()
            if counter==100:
                try:
                    file_name=sp.speech()                 
                    resize_img = cv2.resize(frame,(225,245),interpolation = cv2.INTER_AREA)
                    
                    cv2.imwrite(os.path.join(UserPath,f"{file_name}.png"), resize_img)
                    ref=db.reference('Students').update({
                        file_name:
                                {
                                    "name":file_name,
                                    "Credits":69
                                }
                                                            })
                    if os.path.isfile(image_path):
                    # Upload the specified image to Firebase Storage
                        time.sleep(1)
                        image_filename =f'{file_name}'+".png"
                        print(image_filename)
                        image_path = os.path.join(UserPath, image_filename)
                        image_filename=f'{UserPath}/{image_filename}'
                        bucket = storage.bucket()
                        blob = bucket.blob(image_filename)
                        blob.upload_from_filename(image_path)
                        print(image_path)
                        print(f"Uploaded {image_filename} to Firebase Storage")
                        time.sleep(1)
                        AuthenticationList[0]=-1
                        
                        
                    else:
                        print(f"The specified image file '{image_filename}' does not exist.")
                    counter=0       
                except:
                    break
                



    #################################################






            
                    
    #maincode
    mainCounter=0
    counter=0
    counterPause=0
    ImgBackground=0
    modeType=0
    selections=-1
    mainCounter=0
    creditCounter=0
    while AuthenticationList[0]==4:
        authloop=0
        ret,frame=cap.read()
        face_location,face_names=sfr.detect_known_faces(frame)
        for face_loc,name in zip(face_location,face_names):              
            print(name)
            name1=name         
            
            

        Output()
        if name=="Unknown":
            print("Unknown face")

        while name=="Devansh":            
                if selectionList[0]!=-1 and selectionList[1]!=-1 and selectionList[2]!=-1 and creditCounter<1:
                    ref=db.reference(f'Students/{name}')
                    studentInfo['Credits']-=10  
                    ref.child('Credits').set(studentInfo['Credits'])
                    creditCounter=1
                success,frame=cap.read()
                frame=detector.findHands(frame)
                lmList=detector.findPosition(frame,draw=False)
                                
                if len(lmList)!=0 and counterPause==0 and modeType<3:
                    fingers=[]

                    #thumb
                    if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
                            fingers.append(1)
                    else:
                            fingers.append(0)


                    #fingers
                    for id in range(1,5):

                        if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    # print(fingers)
                    totalFingers=fingers.count(1)
                    print(fingers) 

                    if fingers==[0,1,0,0,0]:
                        if selections!=1:
                            counter=1
                        selections=1
                    elif fingers==[0,1,1,0,0]:
                        if selections!=2:
                            counter=1
                        selections=2
                    elif fingers==[0,1,1,1,0]:
                        if selections!=3:
                            counter=1
                        selections=3
                    else:
                        selections=-1
                        counter=0
                    if counter>0:
                        counter+=1
                        #  print(counter)
                        cv2.ellipse(ImgBackground,modePositions[selections-1],(103,103),0,0,counter*selectionSpeed,(0,156,0),15)

                        if counter*selectionSpeed>360:
                            selectionList[modeType]=selections
                            modeType+=1
                            counter=0
                            selections=-1
                            counterPause=1
                            #  print(modeType)
                #pause function  
                if counterPause>0:
                    counterPause+=1
                    if counterPause>40:
                        counterPause=0
                
                
                print(selectionList)
                Output()

                
        if name!="Devansh" and name!="Unknown":
            print("No Face Detected")
    
    file_name=""
    register=0
    authloop=-1
    cntr=1
    mainCounter=0
    cap=cv2.VideoCapture(0)
    name=0
    resize_img=0
    counter=0
    counterPause=0
    selectionList=[-1,-1,-1]
    AuthenticationList=[-1]
    ImgBackground=0
    modeType=4
    selections=-1
    ImgStudent=[]