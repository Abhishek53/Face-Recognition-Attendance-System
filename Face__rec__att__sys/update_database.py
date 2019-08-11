import xlwt
from xlutils.copy import copy
import xlrd 
from datetime import datetime
style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
style2 = xlwt.easyxf('font: name Times New Roman, color-index green, bold on',
    num_format_str='#,##0.00')

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

"""style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')




ws.write(0, 0, 'cse-A', style0)
ws.write(1, 0, datetime.now(), style1)

ws.write()
ws.write(2, 0, 'mathematics')
ws.write(2, 1, 'oops')
ws.write(2, 2, 'DC')

wb.save('example.xls')"""
def update_att(ID,name,time,wku):
	
	j=ID+2
	
	if(time==5):
		i=2
	elif(time==10):
		i=3
	elif(time==15):
		i=4
	elif(time==20):
		i=5
	elif(time==25):
		i=6
	else:
		print("invalid time session")
		return
	rb=xlrd.open_workbook('Attendance_database/'+str(wku)+'.xls')
	#r_sheet=wov.sheet_by_index(0)
	woverw=copy(rb)
	w_sheet=woverw.get_sheet(0)
	w_sheet._cell_overwrite_ok = True
	#ws.write(j, i, 'P', style2)
	w_sheet.write(j, i, 'P', style2)
	
	#woverw.get_sheet(0).write(j, i, 'P', style2)
	print wku
	#wb.save('Attendance_database/'+str(wku)+'.xls')
	woverw.save('Attendance_database/'+str(wku)+'.xls')
	print('Attendance_database/'+str(wku)+'.xls')
	w_sheet._cell_overwrite_ok = False
	return
def create_new(wk):
	"""style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
	style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

	wb = xlwt.Workbook()
	ws = wb.add_sheet('A Test Sheet')"""

	(usn,name,s1,s2,s3,s4,s5,s6,a,b,c,d,e,f,g,h,information,i)=([],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],10)
	print wk
	if(wk=='Student'):
		open_file = open('Student.txt', 'r')

	elif(wk=='Internet_yale'):
		open_file = open('Internet_yale.txt', 'r')
		print 'read iy'
	else:
		print('No text file loaded')
		return 

	for line in open_file:
 		if line:
			print(line)
  			a,b,c,d,e,f,g,h= line.split('---')
			usn.append(a)
        		name.append(b)
			s1.append(c)
			s2.append(d)
			s3.append(e)
			s4.append(f)
			s5.append(g)
			s6.append(h)

	open_file.close()
	j=0
	print(len(usn))
	ws._cell_overwrite_ok = True
	
	for i in range(0,len(usn)):
		for j in range(0,len(usn)):
			if(i==0):
				ws.write(j, i, str(usn[j]), style0)
			if(i==1):
				ws.write(j, i, str(name[j]), style0)
			if(i==2):
				ws.write(j, i, str(s1[j]), style0)
			if(i==3):
				ws.write(j, i, str(s2[j]), style0)
			if(i==4):
				ws.write(j, i, str(s3[j]), style0)
			if(i==5):
				ws.write(j, i, str(s4[j]), style0)
			if(i==6):
				ws.write(j, i, str(s5[j]), style0)
			if(i==7):
				ws.write(j, i, str(s6[j]), style0)
		print(i)
	print(wk)
	wb.save('Attendance_database/'+str(wk)+'.xls')
	print('Attendance_database/'+str(wk)+'.xls')
	ws._cell_overwrite_ok = False
	
#create_new()

