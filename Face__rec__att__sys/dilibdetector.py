import dlib,cv2
import numpy as np
import image_processing
detector = dlib.get_frontal_face_detector()
webcam=cv2.VideoCapture(0)	
while True:
		ret,image=webcam.read()
		im=cv2.flip(image,1,0)
		image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		
		gray=image_processing.image_process_hist(image)
		#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		#detect faces
		faces=detector(gray,1)
		for (i, rect) in enumerate(faces):
			cv2.rectangle(im, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0, 255, 0), 2)
			cv2.rectangle(im, (rect.left(), rect.top() ), (rect.right(),rect.top()+25), (0, 255, 0), cv2.FILLED)
			cv2.putText(im, "Human_Face", (rect.left()+6 , rect.top()+20), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0, 0, 0))
        
			
		cv2.namedWindow("DETECTOR", cv2.WINDOW_NORMAL)
		cv2.resizeWindow('im', 1200,1200)
		cv2.imshow('DETECTOR',im)
		if cv2.waitKey(10) & 0xFF == ord('q'):
        		break



# Stop the camera
webcam.release()
