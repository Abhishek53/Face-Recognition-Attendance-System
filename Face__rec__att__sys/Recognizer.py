import cv2,os,time,dlib
import numpy as np
import image_processing
import requests
import update_database
import collections
slot=5
(names,IDs,Rollnos)=({},{},{})
def updb(arr,wkf):
	    freq = collections.Counter(arr)
	    maxi=-1  
	    keyele=-1 
	    global slot
	    global minschedule
	    for key, value in freq.iteritems():
	        print key, " -> ", value
		print("\n\n")
		if(value>=maxi):
			maxi=value
			keyele=key
	    if(maxi>-1 and keyele>-1):
			#update_database.update_att(keyele+1,Rollnos[keyele],5)
			if(time.time()>=minschedule):
						slot+=5
						minschedule=time.time()+60*1
						
			print slot
			update_database.update_att(int(Rollnos[keyele]),names[keyele],slot,wkf)
	    return

def Recognize_face(model,wk):
	path='image_database/'+wk
	count=0
	update_database.create_new(wk)

	#Traverse dirs to get names
	for(sudirs, dirs,files) in os.walk(path):
		for subdir in dirs:
			if(subdir!='\0'):
				ls=str(subdir)
				a,b= ls.split(':')
				print('**************('+str(a)+','+str(b)+')***************')
				Rollnos[count]=(str(b))
				names[count]=(str(a))
			count+=1
	print names
	print Rollnos
	#print The names to test proper Traverse
	for i in range(len(names)):
		IDs[i]=i
		print("Id of %s is :%s"%(names[i],i))

	#Select model and load xml file	
	if(model=='LBPH'):
		recognizer=cv2.face.LBPHFaceRecognizer_create(1)

	elif(model=='Fisher'):
		recognizer=cv2.face.FisherFaceRecognizer_create()

	elif(model=='Eigen'):
		recognizer=cv2.face.EigenFaceRecognizer_create(10)

	#print('Trained_models_xml/'+wk+'/'+wk+model+'data.xml')
	recognizer.read('Trained_models_xml/'+wk+'/'+wk+model+'data.xml')
	print('Trained_models_xml/'+wk+'/'+wk+model+'data.xml')
	print(model=='LBPH')
	#Haar classifier
	haar_face='Haar/haarcascade_frontalface_default.xml'
	haar_eye='Haar/haarcascade_eye_tree_eyeglasses.xml'
	detector=dlib.get_frontal_face_detector()
	face_haar_cascade=cv2.CascadeClassifier(haar_face)
	eye_haar_cascade=cv2.CascadeClassifier(haar_eye)
	
	shape_file='Haar/shape_predictor_5_face_landmarks.dat'
	predictor = dlib.shape_predictor(shape_file)


	#Start recognizing
	print 'press \'q\' to quit reconition process'
	webcam=cv2.VideoCapture(0)
	end=time.time()+60*0.083333
	global minschedule
	minschedule=time.time()+60*1
	print minschedule
	count=1
	arr=[]
	#url='http://192.168.43.1:8080/photoaf.jpg'
	while True:
		(rval,im)=webcam.read()
		#print(arr)
		#img_resp=requests.get(url)
		#img_arr=np.array(bytearray(img_resp.content),dtype=np.uint8)
		#im=cv2.imdecode(img_arr,1)
		im=cv2.flip(im,1,0)
		
		gray_im=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
		#if u want to compare bw preprcessed and processed img enable 	those 2
		#cv2.imshow('preprocessed',gray)
		gray=image_processing.image_process_hist(gray_im)
		#cv2.imshow('processed',gray)
		faces=detector(gray,1)
		
		for(i,rect) in enumerate(faces):
			
			col_face=im[rect.top():rect.bottom(), rect.left():rect.right()]	
			gr=gray[rect.top():rect.bottom(), rect.left():rect.right()]	
			#cv2.imshow('hist',gray)
			#cv2.waitKey(150)
			#algn_face=image_processing.image_process_align(col_face)
			faces_alg = dlib.full_object_detections()
			faces_alg.append(predictor(im, faces[i]))
			images_alg = dlib.get_face_chips(im, faces_alg, size=100)
			
			if(len(images_alg)<1):
				algn_face=col_face
				algn_face = cv2.cvtColor(algn_face, cv2.COLOR_BGR2Gray)    
				print 'yes'
			else:
				for img_alg in images_alg:
    					algn_face = cv2.cvtColor(img_alg, cv2.COLOR_RGB2BGR)    
					algn_face= cv2.cvtColor(algn_face, cv2.COLOR_RGB2GRAY)
					#algn_face=image_processing.image_process_hist(algn_face)
			
			gray_face=image_processing.image_process_hist(algn_face)
			#cv2.imshow('algngray',gray_face)
			#cv2.waitKey(100)	
			
		
			#gray_face=gray[rect.top():rect.bottom(), rect.left():rect.right()]		
			#cv2.imshow('gray',gray_face)
			#eyes=eye_haar_cascade.detectMultiScale(gray_face)
			#for(ex,ey,ew,eh) in eyes:
			count+=1	
			cv2.rectangle(im,(rect.left(),rect.top()),(rect.right(),rect.bottom()),(0,255,0),2)
			#gray_face=cv2.resize(gray_face,(90,90))
			cv2.imshow('goingto',gray_face)
			cv2.waitKey(50)
			ID,conf=recognizer.predict(gray_face)
				
			arr.append(ID)
			if(time.time()>=end):
				updb(arr,wk)
				end=time.time()+60*0.083333
				arr=[]
	
			print (str(Rollnos[ID])+':'+str(conf))
			if(wk=='Student'):
				ID_OUT=names[ID]
			else:
				ID_OUT=Rollnos[ID]
			cv2.rectangle(im, (rect.left(), rect.top() ), (rect.right(),rect.top()+25), (0, 255, 0), cv2.FILLED)
			cv2.putText(im, str(ID_OUT)+":"+str(round(conf,2)), (rect.left()+6 , rect.top()+20), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255, 255, 255))
        
			#count+=1
		cv2.namedWindow("window", cv2.WINDOW_NORMAL)
		cv2.resizeWindow('image', 1200,1200)
		cv2.imshow("window",im)
		
		if cv2.waitKey(1) & 0xFF==ord('q'):
			break
	print count
	cv2.destroyAllWindows()

	
while True:
	print("***************Menu************\n1.Student\n2.Internet_yale")
        opt1=input("\nchoose any one category")
	print("_____models____\n1.LBPH\n2Eigen\n3.Fisher")
	opt2=input("\nchoose any one recognizer")
	
	if(opt1==1):
		if(opt2==1):
			Recognize_face('LBPH','Student')
			break 
		elif(opt2==2):
			Recognize_face('Eigen','Student')
			break 
		elif(opt2==3):
			Recognize_face('Fisher','Student')
			break  



	elif(opt1==2):
		if(opt2==1):
			Recognize_face('LBPH','Internet_yale')
			break 
		elif(opt2==2):
			Recognize_face('Eigen','Internet_yale')
			break 
		elif(opt2==3):
			Recognize_face('Fisher','Internet_yale')
			break

	
	










