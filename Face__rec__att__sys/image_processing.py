import numpy as np
import cv2
import dlib


shape_file='Haar/shape_predictor_5_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_file)

def image_process_hist(gray):
	if(np.mean(gray)>110):
		equ=cv2.equalizeHist(gray)
		#return np.hstack((gray,equ))
		#print 'hist'
		return equ
		
	elif(np.mean(gray)<85):
		clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(3,3))
		#print'clache'
		return clahe.apply(gray)
	else:
		equ=cv2.equalizeHist(gray)
		#print 'hist'
		#return np.hstack((gray,equ))
		return equ

def image_process_align(im):
	
	#im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	dets = detector(im, 1)
	num_faces = len(dets)
	if num_faces == 0:
		return im
	
	faces = dlib.full_object_detections()
	for detection in dets:
    		faces.append(predictor(im, detection))

	# images = dlib.get_face_chips(im, faces, size=160, padding=0.25)
	images = dlib.get_face_chips(im, faces, size=320)
	for image in images:
    		cv_bgr_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)    
		return cv_bgr_img

	
	

