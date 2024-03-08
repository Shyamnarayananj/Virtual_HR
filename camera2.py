# camera.py
import cv2
import PIL.Image
from PIL import Image
from PIL import ImageTk

#import f_Face_info
import time
import imutils
import argparse
import shutil
import imagehash
from deepface import DeepFace

class VideoCamera2(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

        
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        ###DF
        result = DeepFace.analyze(img_path=image, actions=['emotion'], enforce_detection=True)
    
        #result = DeepFace.analyze(img_path=frame, actions=['emotion'], enforce_detection=False)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        ###
        # Read the frame
        #_, img = cap.read()
        ######
        '''test_image_one = image
        emo_detector = FER(mtcnn=True)
        # Capture all the emotions on the image
        captured_emotions = emo_detector.detect_emotions(test_image_one)
        # Print all captured emotions with the image
        print(captured_emotions)
        #plt.imshow(test_image_one)

        # Use the top Emotion() function to call for the dominant emotion in the image
        dominant_emotion, emotion_score = emo_detector.top_emotion(test_image_one)
        print(dominant_emotion, emotion_score)
        
        self.value=str(dominant_emotion)

        ff=open("result.txt","w")
        ff.write(self.value)
        ff.close()'''
        ########
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Draw the rectangle around each face
        j = 1
        for (x, y, w, h) in faces:
            #mm=cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

            thickness = 2
            fontSize = 0.5
            step = 20
            txt = str(result[0]['dominant_emotion'])
            emotion2="Emotion: "+txt
            cv2.putText(image, emotion2, (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, fontSize, (0,255,0), thickness)
            
            j += 1

            emo=emotion2+","
            ff1=open("emotion.txt","a")
            ff1.write(emo)
            ff1.close()
            
        print(j)
        ff4=open("img.txt","w")
        ff4.write(str(j))
        ff4.close()

        ##########################
        parser1 = argparse.ArgumentParser(description="Face Info")
        parser1.add_argument('--input', type=str, default= 'webcam',
                            help="webcam or image")
        parser1.add_argument('--path_im', type=str,
                            help="path of image")
        args1 = vars(parser1.parse_args())

        type_input1 = args1['input']
        ###########################################
        '''star_time = time.time()
        #ret, frame = cam.read()
        frame = imutils.resize(image, width=720)
        
        # obtenego info del frame
        out = f_Face_info.get_face_info(frame)
        # pintar imagen
        image = f_Face_info.bounding_box(out,frame)

        end_time = time.time() - star_time    
        FPS = 1/end_time
        #cv2.putText(image,f"FPS: {round(FPS,3)}",(10,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        '''
        #############
            
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
