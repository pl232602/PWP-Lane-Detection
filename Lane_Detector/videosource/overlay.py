import cv2
import numpy as np
from videosource import camera
from tensorflow import keras

model = keras.models.load_model(r'/home/nilesosa/Documents/TensorFlow/TensorFlow/model.h5')

class Lanes():
    def __init__(self):
        self.recent_fit = []
        self.avg_fit = []

def road_lines(image):
    ##small_img = resize(image,(80,160,3))
    small_img = cv2.resize(image,(160,80),interpolation=cv2.INTER_CUBIC)
    small_img = np.array(small_img)
    small_img = small_img[None,:,:,:]

    prediction = model.predict(small_img)[0]*255
    lanes.recent_fit.append(prediction)
    if len(lanes.recent_fit) > 5:
        lanes.recent_fit = lanes.recent_fit[1:]

    lanes.avg_fit = np.mean(np.array([i for i in lanes.recent_fit]),axis = 0)

    blanks = np.zeros_like(lanes.avg_fit).astype(np.uint8)
    lane_drawn = np.dstack((blanks, lanes.avg_fit,blanks))

    ##lane_image = resize(lane_drawn,(720,1280,3))
    lane_image = cv2.resize(lane_drawn,(1280,720))
    image = cv2.resize(image,(1280,720))
    result = cv2.addWeighted(image,1,lane_image,1,0,dtype=cv2.CV_8UC1)

    return result, lane_image


lanes = Lanes()

def gen_overlay():
    for local_frame in camera.gen_frames():#generate an overlay based on the data from object detection
        frame = local_frame
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        output_frame, overlay_frame = road_lines(frame)
        
        
        ret, thresh = cv2.threshold(overlay_frame,127,255,0)
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(thresh,kernel,iterations=3)
        dilated = dilated.astype(np.uint8)
        dilated = cv2.cvtColor(dilated,cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        print("tingz:")
        contour_length = []
        for s in contours:
             contour_length.append(len(s))
        main_contour = contour_length.index(max(contour_length))
        contour_length.remove(contour_length[main_contour])
        try:
            if contour_length.index(max(contour_length)) >= main_contour:
                main_contour2 = contour_length.index(max(contour_length)) + 1
            else:
                main_contour2 = contour_length.index(max(contour_length))

            print(main_contour)
            hull0 = cv2.convexHull(contours[main_contour])
            hull1 = cv2.convexHull(contours[main_contour2])
            hull = np.vstack([hull0, hull1])
        except ValueError:
            hull = cv2.convexHull(contours[main_contour])

        rect = cv2.minAreaRect(hull)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],-1,(255,255,255),3)
        overlay_frame = frame
        yield (overlay_frame)

    pass
def obstacle_locator():
    #detect and generate objects and get a rectangular location for them
    pass
def pathway():
    #detect the location of the center line, sides, and offshoots (possible turns), and turn detection (depending on type of road detected)
    pass

def gen_rotation(): #tepmlate code for compass rotation
    while True:
        r=45
        for overlay_frame in gen_overlay():
            overlay_frame=rotatecompilecompass(local_frame,r)
            if compass_direction == "right": #set left rotation direction
                r=r+10
            elif compass_direction == "left": #set right rotation direction
                r=r-10
            elif compass_direction == "none": #set left rotation direction
                pass
            yield (overlay_frame)

def rotatecompilecompass(inputframe,angle): #rotates, filters, and overlays compass onto video frame
    global s_img
    image=s_img
    image=imutils.rotate(image,angle)
        
    y_offset=15
    x_offset=15

    y1, y2 = y_offset, y_offset + image.shape[0]
    x1, x2 = x_offset, x_offset + image.shape[1]

    alpha_s = image[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s
    for c in range(0, 3):
        inputframe[y1:y2, x1:x2, c] = (alpha_s * image[:, :, c] +
                                alpha_l * inputframe[y1:y2, x1:x2, c])
    return inputframe
