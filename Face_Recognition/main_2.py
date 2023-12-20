import cv2
import numpy as np
import face_recognition
import os
from pathlib import Path
from datetime import datetime
import tensorflow as tf
from tensorflow import keras
from model import SiameseModel

# Path = 'ImageAttendance'
# images = []
# ClassNames = []
# MyList = os.listdir(Path)
# print(MyList)
# for cl in MyList:
#     curImg = cv2.imread(f'{Path}/{cl}')
#     images.append(curImg)
#     ClassNames.append(os.path.splitext(cl)[0])
# print(ClassNames)


# def embed_image(image):
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     img = np.zeros((*image.shape[:2],3), np.uint8)
#     img[:,:,0] = img[:,:,1] = img[:,:,2] = image[:,:]
#     img = cv2.resize(img, (125,125))
#     embeddings = siameseModel.siameseNetwork((img, img, img))[0] #
#     return(embeddings)
        

# def findEncodings(images):
#     encodeList = []
#     for image in images:
#         image = face_recognition.face_locations(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         img = np.zeros((125,125,3), np.uint8)
#         img[:,:,0] = img[:,:,1] = img[:,:,2] = image[:,:]
#         img = cv2.resize(img, (125,125,3))
#         encode = siameseModel.siameseNetwork((img, img, img))[0] #
#         encodeList.append(encode)
#     return encodeList

# modelPath = './siamese_network_black_and_white-20231213T222604Z-001'
# print(f"[INFO] loading the siamese network from {modelPath}...")
# siameseNetwork = keras.models.load_model(filepath=modelPath)
# siameseModel = SiameseModel(
# 	siameseNetwork=siameseNetwork,
# 	margin=0.5,
# 	lossTracker=keras.metrics.Mean(name="loss"),
# )

# def markAttendance(name):
#     now = datetime.now()
#     fileName = "attendance" + str(now.date()) + ".csv"
#     with open (fileName ,'a+') as f:
#         if os.stat(fileName).st_size == 0:
#             f.write("name,date")
#         f.seek(0)
#         myDataList = f.readlines()
#         nameList = []
#         for line in myDataList:
#             entry = line.split(',')
#             nameList.append(entry[0])
#         if name not in nameList:
#             dtstring = now.strftime('%H:%M:%S')
#             f.writelines(f'\n{name},{dtstring}')

# encodeListKnown = findEncodings(images)
# print("Completed")


# #cap = cv2.VideoCapture(0)

# while True:
#     cap = cv2.VideoCapture(0)
    
#     success, img = cap.read()
#     imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#     facesCurrentFrame = face_recognition.face_locations(imgS)
#     encodeCurrentFrame = face_recognition.face_encodings(imgS,facesCurrentFrame)

#     for encodeFace,faceLoc in zip(encodeCurrentFrame,facesCurrentFrame):
#         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#         print(faceDis)
#         matchIndex = np.argmin(faceDis)
#         if matches[matchIndex]:
#             name = ClassNames[matchIndex].upper()
#             print (name)
#             y1,x2,y2,x1 = faceLoc
#             y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
#             cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
#             cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
#             cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
#             markAttendance(name)

    

#     cv2.imshow("WebCam",img)
#     cap.release()
#     cv2.waitKey(0)

#     #cv2.imshow("WebCam",img)
#     #key = cv2.waitKey(1)
#     #if key == ord('q'):
#     #    cap.release()
#     #    cv2.destroyAllWindows()
#     #    break


detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

