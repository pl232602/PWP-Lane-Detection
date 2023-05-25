import cv2
cap = cv2.VideoCapture(r"C:\Users\Niles Alexis\Documents\PWP Lane Detection\PWP-Lane-Detection\Lane_Detector\videosource\realvid9.MOV")
from time import time


i=0
loop_time = time()
while i==0:
    ret, frame = cap.read()

    if ret == True:
        
        cv2.imshow('Output',frame)
    
    key = cv2.waitKey(1)
    if key == ord('q'):  
        cv2.destroyAllWindows()
        break
    elif key == ord('f'):
        cv2.imwrite('positive/{}.jpg'.format(loop_time),screenshot)
    