#Importing OpenCV Library
import cv2
# Import Numpy
import numpy as np
# Dlib for face detection
import dlib
#face_utils for basic operations of conversion
from imutils import face_utils


#Initializing the camera and taking the instance
cap = cv2.VideoCapture(0)

#Initializing the face detector and landmark detector
detector = dlib.get_frontal_face_detector()
path = "shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(path)

#status marking for current state
sleeping = 0
drowsy = 0
isActive = 0
status=""
color=(0,0,0)

def compute(ptA,ptB):
	dist = np.linalg.norm(ptA - ptB)
	return dist

def blinked(a,b,c,d,e,f):
	up = compute(b,d) + compute(c,e)
	down = compute(a,f)
	ratio = up/(2.0*down)

	#Checking if it is blinked
	if(ratio>0.25):
		return 2
	elif(ratio>0.21 and ratio<=0.25):
		return 1
	else:
		return 0


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    face_frame = frame.copy()
    if(faces):

      for face in faces:
          x1 = face.left()
          y1 = face.top()
          x2 = face.right()
          y2 = face.bottom()

          cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

          landmarks = predictor(gray, face)
          landmarks = face_utils.shape_to_np(landmarks)

          #The numbers are actually the landmarks which will show eye
          left_blink = blinked(landmarks[36],landmarks[37], 
            landmarks[38], landmarks[41], landmarks[40], landmarks[39])
          right_blink = blinked(landmarks[42],landmarks[43], 
            landmarks[44], landmarks[47], landmarks[46], landmarks[45])
          
          #Now judge what to do for the eye blinks
          if(left_blink==0 or right_blink==0):
            sleeping+=1
            drowsy=0
            isActive=0
            if(sleeping>6):
              status="SLEEPING !!!"
              color = (10, 10, 199)
              import winsound
              duration = 1000  # milliseconds
              freq = 440  # Hz
              winsound.Beep(freq, duration)
          elif(left_blink==1 or right_blink==1):
            sleeping=0
            isActive=0
            drowsy+=1
            if(drowsy>6):
              status="Drowsy!"
              color = (255,0,0)
          else:
            drowsy=0
            isActive+=1
            if(isActive>6):
              status="Active"
              color = (25, 194, 6)
          cv2.putText(frame, status, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)

          for n in range(0, 68):
            (x,y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)
    else:
      status="Out of Frame !!!"
      color = (255, 0, 0)
      import winsound
      duration = 1000  # milliseconds
      freq = 440  # Hz
      winsound.Beep(freq, duration)
    cv2.imshow("Frame", frame)
    cv2.imshow("Result of detector", face_frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
      	break