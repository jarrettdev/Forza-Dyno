import os
import cv2

#frame by frame pictures from a video

#todo: implement folder naming logic so multiple videos can be saved into frames

if not os.path.exists('images_frames'):
	os.makedirs('image_frames')


test_vid = cv2.VideoCapture('m5t.mp4')

index=0

while test_vid.isOpened():
	ret,frame = test_vid.read()
	if not ret:
		break

	name = './image_frames/frame' + str(index) + '.jpg'

	print('Extracting frames...' + name)
	cv2.imwrite(name,frame)
	index += 1
	if cv2.waitKey(10) & 0xFF == ord('q'):
		break

test_vid.release()
cv2.destroyAllWindows()