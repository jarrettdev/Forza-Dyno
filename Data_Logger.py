#playing with ocr for frame-by-frame text analysis


from PIL import Image
import pytesseract
import cv2
import numpy as np
import os
import re
import csv
import my_files

#sorts 'xsf10, xsf1, xsf0' correctly like a human would. useful for sorting files
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

#name directory with a number that represents the run at the end of the name
def file_name_logic(directory,end_point):

#file naming logic
	dir = os.path.dirname(directory)
	for num in range(0,int(end_point)):
		#file name to check for
		arb_file = os.path.join(dir,str(num))
		#if it doesn't exist, run with this file name
		if not os.path.exists(arb_file):
			filename = arb_file
			break
	return arb_file

#check if a number is present in a string
def num_there(s):
    return any(i.isdigit() for i in s)

	#directory where the black and white 'paperfied' data will go
processed_dir = file_name_logic(str(my_files.STRIPPED_DATA_DIR), 100)
os.mkdir(processed_dir)

sorted_frames = natural_sort(os.listdir(str(my_files.IMAGE_FRAMES_DIR)))

'''
with open('frames.txt','w') as file:
	for vid_frame in natural_sort(os.listdir('C:\\Users\\Jarrett\\Documents\\Experiments\\Forza\\image_frames')):
		file.write(str(vid_frame))
'''
#color range for white numbers in forza telemetry
lower_white = np.array([0,0,210], dtype=np.uint8)
upper_white = np.array([220,240,255], dtype=np.uint8)

count = 0 



for vid_frame in sorted_frames:
	print(str(vid_frame))
	img = cv2.imread(str(my_files.IMAGE_FRAMES_DIR) + str(vid_frame), flags=cv2.IMREAD_COLOR)
	crop_img = img[145:540, 50:176]

	hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
	# Threshold the HSV image to get only white colors
	mask = cv2.inRange(hsv, lower_white, upper_white)

	# Bitwise-AND mask and original image
	res = cv2.bitwise_and(crop_img,crop_img, mask= mask)

	paperfied = cv2.bitwise_not(res)

	#cv2.imshow('original',img)

	#cv2.imshow('mask',mask)

	#cv2.imshow('res',res) 

	#cv2.imshow('paperfied',paperfied)

	#cv2.imshow('cropped',crop_img)
	#cv2.imshow('hsv',hsv)


	#k = cv2.waitKey() & 0xFF

	cv2.imwrite(str(processed_dir) + '\\' + 'processed' + str(count) + '.jpg', paperfied)


	count += 1

cv2.destroyAllWindows()

'''

=======
parameter separation
=======

'''

print(os.listdir(processed_dir))

sorted_frames = natural_sort(os.listdir(processed_dir))

os.mkdir(str(processed_dir) + '\\' 'horsepower')
os.mkdir(str(processed_dir) + '\\' 'torque')
os.mkdir(str(processed_dir) + '\\' 'boost')
os.mkdir(str(processed_dir) + '\\' 'rpm')

count = 0
for data_log in sorted_frames:
	img = cv2.imread(processed_dir + '\\' + str(data_log))

	hp_crop = img[40:70, 0:176]
	torque_crop = img[100:140, 0:176]
	boost_crop = img[170:210,0:176]
	rpm_crop = img[240:280,0:176]
	#cv2.imshow("orig", img)
	#cv2.imshow("horsepower", hp_crop)
	cv2.imwrite(str(processed_dir + '\\horsepower\\') + 'hp' + str(count) + '.jpg',hp_crop)
	#cv2.imshow("torque", torque_crop)
	cv2.imwrite(str(processed_dir + '\\torque\\') + 'torque' + str(count) + '.jpg',torque_crop)
	#cv2.imshow("boost", boost_crop)
	cv2.imwrite(str(processed_dir + '\\boost\\') + 'boost' + str(count) + '.jpg',boost_crop)
	#cv2.imshow("rpm", rpm_crop)
	cv2.imwrite(str(processed_dir + '\\rpm\\') + 'rpm' + str(count) + '.jpg',rpm_crop)
	#watch the slashes!
	
	
	count += 1
	
	#cv2.waitKey(0)
	



# INTERPRET PARAMS

param_list = []

#hp interpret

sorted_hp = natural_sort(os.listdir(str(processed_dir + '\\horsepower')))

sorted_torque = natural_sort(os.listdir(str(processed_dir + '\\torque')))

sorted_boost = natural_sort(os.listdir(str(processed_dir + '\\boost')))

sorted_rpm = natural_sort(os.listdir(str(processed_dir + '\\rpm')))


#pytesseract init

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

hp_list = []
tq_list = []

#extract hp data
#keep track of index of current file
count = -1



for hp_reading in sorted_hp: 
	cleaned_hp = None
	#open the paperfied hp img and read it
	hp_img = Image.open(str(processed_dir + '\\horsepower') + '\\' + str(hp_reading))
	count += 1
	text = pytesseract.image_to_string(hp_img, lang='eng')
	# if it can't read 'hp', its unlikely the numeric value will be accurate
	if('hp' in text):
		filtered_str = ''.join(text.replace('POWER','').strip().split('hp')[0].replace('.',','))

		if(num_there(filtered_str)):
			cleaned_hp = str(filtered_str).replace('S','5')
			print(cleaned_hp + '' + str(count))
			hp_list.append(cleaned_hp)
			param_list.append ({'Horsepower' : cleaned_hp, 'Torque': None, 'RPM' : None})
	else:
		param_list.append({'Horsepower' : None, 'Torque': None, 'RPM' : None})
		print('override append ' + str(count) + 'sorted_hp = ' + str(len(sorted_hp)))

	#last chance to fill out empty values 
	try:
		param_list[int(count)]
	except:
		param_list.append({'Horsepower' : None, 'Torque': None, 'RPM' : None})
		print('override append ' + str(count) + 'sorted_hp = ' + str(len(sorted_hp)))


print(hp_list)

with open('hps.txt','w') as file:
	for hp in hp_list:
		file.write(hp + '\n')

#extract torque data

#keep track of index of current file
count = -1
for torque_reading in sorted_torque: 
	demo = Image.open(str(processed_dir + '\\torque') + '\\' + str(torque_reading))
	count += 1
	text = pytesseract.image_to_string(demo, lang='eng')
	if(('ft' in text) or ('lb' in text)):
		filtered_str = ''.join(text.strip().split('ft')[0].replace('.',','))

		if(num_there(filtered_str)):
			cleaned_torque = str(filtered_str).replace('S','5')
			print(cleaned_torque + ' ' + str(count) + ' ' + str(len(param_list)))
			tq_list.append(cleaned_torque)
			param_list[int(count)]['Torque'] = cleaned_torque
	else:
		param_list[int(count)]['Torque'] = None




print(str(tq_list) + ' ' + str(count))

#extract rpm data

#keep track of index of current file
count = -1
for rpm_reading in sorted_rpm: 
	rpm_img = Image.open(str(processed_dir + '\\rpm') + '\\' + str(rpm_reading))
	count += 1
	text = pytesseract.image_to_string(rpm_img, lang='eng')
	if(num_there(rpm_reading)):
		filtered_str = ''.join(text.strip())
		'''
		clean up the rpm so that if there's 4+ digits, the first period is 
		replaced by a comma and the last period (and anything after) is dropped
		ex : 1.092.2 --> 1,092 and 11.093.4 --> 11,093

		'''
		
		filtered_str = filtered_str[:-2].replace('.',',')

		#throw it out if silly number... ex: 6,79
		if len(filtered_str) == 4 and ',' in filtered_str:
			filtered_str = None



		if(filtered_str is not None):
			cleaned_rpm = str(filtered_str).replace('S','5')
			print(cleaned_rpm + ' ' + str(count))
			tq_list.append(cleaned_rpm)
			param_list[int(count)]['RPM'] = cleaned_rpm
	else:
		param_list[int(count)]['RPM'] = None

	#last chance to fill out empty values 
	try:
		param_list[int(count)]['RPM']
	except:
		param_list[int(count)]['RPM'] = None
		print('override append ' + str(count) + ' sorted_rpm = ' + str(len(sorted_rpm)))

print(str(param_list))

'''
========
OUTPUT TO CSV
========
'''

with open('data_log.csv','w') as csv_file:
	csv_file.write('RPM,Horsepower,Torque\n') 
	csv_file.close()

datalog_csv = open('data_log.csv','a',encoding='utf-8',newline='')

for data_chunk in param_list:
	csv.DictWriter(datalog_csv,['RPM','Horsepower','Torque']).writerow({'RPM':str(data_chunk['RPM']), 'Horsepower':str(data_chunk['Horsepower']),
							'Torque':str(data_chunk['Torque'])})

datalog_csv.close()
