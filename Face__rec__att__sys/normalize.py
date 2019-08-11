import image_processing
import os,cv2
import dlib
detector=dlib.get_frontal_face_detector()
db='image_database/Teacher'

for(subdirs,dirs,files) in os.walk(db):
	for subdir in dirs:
		#names[id]=subdirs
		subjectpath=os.path.join(db,subdir)
		for filename in os.listdir(subjectpath):
			path=subjectpath+'/'+filename
			print path
			im=cv2.imread(path,0)
			#cv2.imshow('im',im)
			#cv2.waitKey(100)
			im=image_processing.image_preprocess(im)
			cv2.imshow('im',im)
			
			cv2.waitKey(100)
			gray=im
			faces=detector(im,1)
			for (i, rect) in enumerate(faces):
				im=gray[rect.top():rect.bottom(),rect.left():rect.right()]		
				cv2.imshow('im',im)
			
				cv2.waitKey(100)
				print(subjectpath)
				im=cv2.resize(im,(90,90))
				cv2.imwrite('%s/%s'%(subjectpath,filename),im)
			
			
