## Test 1

# from datetime import datetime

# now = datetime.now()

# print(str())

# fileName = "attendance" + str(now.date()) + ".csv"

# with open (fileName ,'a+') as f:
#     f.seek(0)
#     for line in f:
#         print(line)
#############################################################
# Test2

import cv2
import numpy as np
import face_recognition
import os
from pathlib import Path
from datetime import datetime
import tensorflow as tf
from tensorflow import keras
from model import SiameseModel
import config
from time import sleep

# Load the model
modelPath = config.MODEL_PATH
print(f"[INFO] loading the siamese network from {modelPath}...")
siameseNetwork = keras.models.load_model(filepath=modelPath)
siameseModel = SiameseModel(
	siameseNetwork=siameseNetwork,
	margin=0.5,
	lossTracker=keras.metrics.Mean(name="loss"),
)

# Load Har Cascade face detector
detector = cv2.CascadeClassifier(config.CASCADE_PATH)

# def load_and_preprocess_image(image_path, target_size=(125, 125)):
#     img = tf.io.read_file(image_path)
#     img = tf.image.decode_image(img, channels=3)
#     img = tf.image.resize(img, target_size)
#     img = tf.cast(img, tf.float32) / 255.0  # Normalize to [0, 1]
#     return img

# Find Face Position
def find_faces(img):
    """
    A Function to find faces position in @img

    Args:
     - img: an image
    """
    gray_faces = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
        minNeighbors=5, minSize=(30, 30))
    # Reordering the image
    for (x, y, w, h) in rects:
        face = gray[y:y + h, x:x + w]
        gray_face = np.zeros((*face.shape[:2],3), np.uint8)
        print(gray_face.shape, face.shape)
        gray_face[:,:,0] = gray_face[:,:,1] = gray_face[:,:,2] = face[:,:]
        
        gray_face = cv2.resize(gray_face, (125,125))
        gray_faces.append(gray_face)
    return gray_faces, rects

def find_embeddings(images):
    """
    A function to find each face embeddings for the faces in each image
    in @images

    Args:
     - images: a list of images
    """
    images_embeddings = []
    for image in images:
        gray_faces, rects = find_faces(image)
        for i, gray_face in enumerate(gray_faces):
            cv2.imwrite(f'temp/{i}.jpg', gray_face)

            gray_face = tf.io.read_file(f'temp/{i}.jpg')
            gray_face = tf.image.decode_image(gray_face, channels=3)
            gray_face = tf.image.resize(gray_face, (125,125))
            gray_face = tf.cast(gray_face, tf.float32) / 255.0
            gray_face = tf.expand_dims(gray_face, axis=0)

            embeddings = siameseModel.siameseNetwork((gray_face, gray_face, gray_face))[0] #
            images_embeddings.append(embeddings)
            os.remove(f'temp/{i}.jpg')
    return images_embeddings, rects

def markAttendance(name):
    now = datetime.now()
    fileName = "attendance" + str(now.date()) + ".csv"
    with open (fileName ,'a+') as f:
        if os.stat(fileName).st_size == 0:
            f.write("name,date")
        f.seek(0)
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtstring}')

# A list to save embeddings
Path = config.IMAGES_PATH
images = []
ClassNames = []
MyList = os.listdir(Path)
print(MyList)
for cl in MyList:
    curImg = cv2.imread(f'{Path}/{cl}')
    images.append(curImg)
    ClassNames.append(os.path.splitext(cl)[0])
print(ClassNames)
#-----------------
students_embedding, _ =  find_embeddings(images)
#-----------------
arrivals_embedding = []
matches = []
matched_index = -1
print(students_embedding)

while True:
    cap = cv2.VideoCapture(0)

    success, img = cap.read()
    print(success)
    if success:
        sleep(1)

        arrivals_embedding, rects = find_embeddings([img])

        for j, arrival_embedding in enumerate(arrivals_embedding):
            for i, student_embedding in enumerate(students_embedding):
                distance = tf.reduce_sum(tf.square(student_embedding - arrival_embedding), axis=-1)
                if distance < config.THRESHOLD:
                    name = ClassNames[i].upper()
                    print (name)
                    (x, y, w, h) = rects[j]
                    y1, x2, y2, x1 = y, (y + h) + 50, x + 170, (x + w) - 200
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    markAttendance(name)

            cv2.imshow("WebCam",img)
            #cap.release()
            #cv2.waitKey(0)

        #cv2.imshow("WebCam",img)
        #key = cv2.waitKey(1)
    #if key == ord('q'):
    #    cap.release()
    #    cv2.destroyAllWindows()
    #    break
                

            # else:
            #     matches.append(False)
            

# while True:
#     cap = cv2.VideoCapture(0)
    
#     success, img = cap.read()
#     #-----------------
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # detect faces in the grayscale frame
#     rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
#         minNeighbors=5, minSize=(30, 30))
#     # OpenCV returns bounding box coordinates in (x, y, w, h) order
#     # but we need them in (top, right, bottom, left) order, so we
#     # need to do a bit of reordering
#     boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
#     for (top, right, bottom, left) in boxes:
#         new_embedding = embed_image(gray[(left, top), (right, bottom)])
#         for student_embedding in students_embedding:
#             distance = tf.reduce_sum(tf.square(student_embedding - new_embedding), axis=-1)
#             if distance < config.THRESHOLD:
#                 matches.append(True)
#             else:
#                 matches.append(False)

#             apDistance = tf.reduce_sum(
#             tf.square(anchorEmbedding - positiveEmbedding), axis=-1
#         )
#         arrival_embeddings.append(embedding)
    
#     # Compare distances
#     #---------------------
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


# rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
#                     minNeighbors=5, minSize=(30, 30))