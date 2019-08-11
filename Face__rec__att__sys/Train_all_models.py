import cv2,sys,os,time
import numpy as np


IY_face_data='image_database/Internet_yale'
S_face_data='image_database/Student'

EigenFace = cv2.face.EigenFaceRecognizer_create()      
FisherFace = cv2.face.FisherFaceRecognizer_create()     
#LBPHFace = cv2.face.LBPHFaceRecognizer_create(1, 1, 7,7) 
LBPHFace = cv2.face.LBPHFaceRecognizer_create() 
#path=T_face_data
i=0
def Train_models(path,wk):
	(faces,lables,names,id,Ids)=([],[],{},0,[])
	print(len(faces))
	
	
	for(subdirs,dirs,files) in os.walk(path):
		for subdir in dirs:
			names[id]=subdirs
			subjectpath=os.path.join(path,subdir)
			for filename in os.listdir(subjectpath):
				org_path=subjectpath+'/'+filename
				lable=id				
				im=cv2.imread(org_path,0)
				faces.append(im)
				lables.append(int(lable))
			print("%s :%d|"%(subdir,id))
        		id += 1
	
	lables=np.array(lables)
	faces=[np.array(lis, 'uint8') for lis in faces]

	#Train all models
	print('\n\n\nStarted Training Eigen model')
	print(len(faces))
	print(len(lables))
	start=time.time()
	EigenFace.train(faces,lables)
	print('Trained Eigen model in: '+str(time.time()-start))
	EigenFace.save('Trained_models_xml/'+wk+'/'+wk+'Eigendata.xml')
	
	print('\n\n\nStarted Training Fisher model')
	print(len(faces))
	print(len(lables))
	start=time.time()
	FisherFace.train(faces,lables)
	print('Trained Fisher model in: '+str(time.time()-start))
	FisherFace.save('Trained_models_xml/'+wk+'/'+wk+'Fisherdata.xml')

	print('\n\n\nStarted Training LBPH model')
	print(len(faces))
	print(len(lables))	
	start=time.time()
	LBPHFace.train(faces,lables)
	print('Trained LBPH model in: '+str(time.time()-start))
	LBPHFace.save('Trained_models_xml/'+wk+'/'+wk+'LBPHdata.xml')


Train_models(IY_face_data,'Internet_yale')
Train_models(S_face_data,'Student')
