import os
import cv2

W = '\033[0m'
R = '\033[31m'
G = '\033[32m'
Y = '\033[33m'
B = '\033[34m'
P = '\033[35m'

video_path = "/Volumes/explorationyear2020@gmail.com - Google Drive/My Drive/Personal/Image/TSV/TSYT/Regular/20220208 Dear Pop Song MVs, Please Stop/4s-eddy-bomb.mp4"

# Read the video from specified path
cam = cv2.VideoCapture(video_path)

try:
	# creating a folder named data
	if not os.path.exists('data'):
		os.makedirs('data')

# if not created then raise error
except OSError:
	print('Error: Creating directory of data')

# frame
currentframe = 0

while(True):
	# reading from frame
	ret, frame = cam.read()
	frameCount = 5
 
	if ret:
		# if video is still left continue creating images
		name = './data/eddy ' + str(int(currentframe/frameCount)) + '.jpg'
		print('Creating ' + name)

		# writing the extracted images
		cv2.imwrite(name, frame)

		# increasing counter so that it will
		# show how many frames are created
		currentframe += frameCount
	else:
		break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
