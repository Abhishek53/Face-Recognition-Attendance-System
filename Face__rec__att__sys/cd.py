#problems:resizing and a rect coming for creopped img

import requests
import cv2,sys,os,time
import numpy as np
import dlib
import image_processing
import update_database


detector=dlib.get_frontal_face_detector()
shape_file='Haar/shape_predictor_5_face_landmarks.dat'
predictor = dlib.shape_predictor(shape_file)
haar_eye='Haar/haarcascade_eye.xml'
eye_haar_cascade=cv2.CascadeClassifier(haar_eye)


#directries to store the pictures
IY_face_data='image_database/Internet_yale'
S_face_data='image_database/Student'


#name is taken as an argument while running the prog
fn_name=sys.argv[1]
usn=sys.argv[2]

	

while True:
	print '*************************choose your category************************* \n\n 1.Student \n 2.Internet_yale\n\n'
	opt=input() 
	if(opt==1):
		path=os.path.join(S_face_data,fn_name)

		file_u=open('Student.txt','a')
		print('opned')
		file_u.write("\n")	
		file_u.write("1BG16CS"+str(usn)+"---"+str(fn_name)+"---AB---AB---AB---AB---AB---AB")
		print('printed')
		file_u.close()
		break


	elif(opt==2):
		path=os.path.join(IY_face_data,fn_name)
		file_u=open('Internet_yale.txt','a')
		print('opned')
		file_u.write("\n")
		file_u.write("1BG16CS"+str(usn)+"---"+str(fn_name)+"---AB---AB---AB---AB---AB---AB")
		print('printed')
		file_u.close()
		break
print opt
"""if(opt==1):
#update_database.create_new('Student')
if(opt==2):
#update_database.create_new('Internet_yale')
"""
rollno=int(usn)+0
directory=path+':'+str(rollno)
print directory	
if not os.path.isdir(directory):
	os.mkdir(directory)

(im_width,im_height)=(105,105)


print '<<<<<<<<<<<<<<<<<<<<<<CAPTURING PICTURES OF YOU!>>>>>>>>>>>>>>>>>>>>>>'
print '<<<<<<<<<<<<<<<<<<<<<<Give some expressions>>>>>>>>>>>>>>>>>>>>>>\n\n'
print '!!!!!!!!!!!!!!!!!!PRESS \'q\' TO STOP CAPTURING PICTURES!!!!!!!!!!!!!!!!!!'


#webcam=cv2.VideoCapture(0)
url='http://192.168.43.1:8080/photoaf.jpg'
count=0
while count<25:
	#(rect,im)=webcam.read()
	img_resp=requests.get(url)
	img_arr=np.array(bytearray(img_resp.content),dtype=np.uint8)
	im=cv2.imdecode(img_arr,1)
	
	im=cv2.flip(im,1,0)
	gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	hist_gray=image_processing.image_process_hist(gray)
  	#cv2.imshow('processed',hist_gray)
	
	faces=detector(hist_gray,1)
	for(i,rect) in enumerate(faces):
			gr=hist_gray[rect.top():rect.bottom(),rect.left():rect.right()]		
  		
			eyes=eye_haar_cascade.detectMultiScale(gr)
			for(ex,ey,ew,eh) in eyes:
				col_face=hist_gray[rect.top()+10:rect.bottom(), rect.left():rect.right()]	
				out_im=cv2.cvtColor(hist_gray,cv2.COLOR_GRAY2BGR)
			        cv2.imshow('colface',col_face)
				faces_alg = dlib.full_object_detections()
				faces_alg.append(predictor(out_im, faces[i]))
				images_alg = dlib.get_face_chips(out_im, faces_alg, size=100)
			#cv2.imshow('out_im',col_face)
			#cv2.waitKey(100)
	
				if(len(images_alg)<1):
					algn_face=col_face
				
					algn_face = cv2.cvtColor(algn_face, cv2.COLOR_BGR2Gray)
					print('len < 1')    
				else:
					for img_alg in images_alg:
    						algn_face = cv2.cvtColor(img_alg, cv2.COLOR_RGB2GRAY)
						cv2.imshow('out_im',algn_face)
						cv2.waitKey(100)
	    
					#algn_face= cv2.cvtColor(algn_face, cv2.COLOR_RGB2GRAY)
						print('len > 1')

			#algn_face=hist_gray[rect.top()+10:rect.bottom(), rect.left():rect.right()]	
			
			#cv2.imshow('aligned face',algn_face)
			#cv2.waitKey(50)
						gray_face=algn_face
						gray_face=image_processing.image_process_hist(algn_face)
				gray_face=cv2.resize((gray_face),(im_width,im_height))
				gray_face=gray_face[7:105, 0:105]	
				gray_face=cv2.resize((gray_face),(100,100))
			
				cv2.imshow('algn_gray',gray_face)
				cv2.waitKey(50)
				print 'Enter 1 to approve'
			
				tv=input()
				if(tv==1):

					pin=sorted([int(n[:n.find('.')])for n in os.listdir(path+':'+str(rollno))
                    				if n[0]!='.']+[0])[-1]+1
					cv2.imwrite('%s/%s.png'%(path+':'+str(rollno),pin),gray_face)
					count+=1
			
				else:
					print 'not taken'
	
				cv2.rectangle(im, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0, 255, 0), 2)
				cv2.rectangle(im, (rect.left(), rect.top() ), (rect.right(),rect.top()+25), (0, 255, 0), cv2.FILLED)
				cv2.putText(im, fn_name, (rect.left() +6, rect.top() +20), cv2.FONT_HERSHEY_PLAIN,2,(0, 0, 255))
			
			
	cv2.namedWindow("window", cv2.WINDOW_NORMAL)
	cv2.resizeWindow('image', 1200,1200)
	cv2.imshow("window",im)
	if cv2.waitKey(1) & 0xFF==ord('q'):
		break

print str(count)+'no of picutes are taken and saved to'+fn_name+'folder'
cv2.destroyAllWindows()



			 

