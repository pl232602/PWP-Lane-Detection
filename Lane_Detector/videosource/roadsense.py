import numpy as np
import cv2
from tensorflow import keras




model = keras.models.load_model(r'C:\Users\Niles Alexis\Documents\PWP Lane Detection\PWP-Lane-Detection\Lane_Detector\videosource\model.h5')

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
cap = cv2.VideoCapture(r"C:\Users\Niles Alexis\Documents\PWP Lane Detection\PWP-Lane-Detection\Lane_Detector\videosource\realvid9.MOV")

global positive_slope
global negative_slope
global positive_slope_total
global negative_slope_total
global positive_slope_avg
global negative_slope_avg

positive_slope = []
negative_slope = []

positive_slope_total = 0
negative_slope_total = 0

positive_slope_avg = 0
negative_slope_avg = 0

global px1_total
global px2_total
global py1_total
global py2_total

px1_total = 0
px2_total = 0
py1_total = 0
py2_total = 0

global mx1_total
global nx2_total
global ny1_total
global ny2_total

nx1_total = 0
nx2_total = 0
ny1_total = 0
ny2_total = 0

global px1
global px2
global py1
global py2

px1 = 0
px2 = 0
py1 = 0
py2 = 0

global nx1
global nx2
global ny1
global ny2

nx1 = 0
nx2 = 0
ny1 = 0
ny2 = 0

global box

box = 0


def roadsense(input_frame):
    
    global positive_slope
    global negative_slope
    global positive_slope_total
    global negative_slope_total
    global positive_slope_avg
    global negative_slope_avg

    global px1_total
    global px2_total
    global py1_total
    global py2_total

    global nx1_total
    global nx2_total
    global ny1_total
    global ny2_total

    global px1
    global px2
    global py1
    global py2

    global nx1
    global nx2
    global ny1
    global ny2

    global box

    frame = input_frame
    frame = cv2.resize(frame,(1280,720))
    natural_frame = frame
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    naturalbgr_frame = cv2.cvtColor(natural_frame,cv2.COLOR_BGR2RGB)
    output_frame, overlay_frame = road_lines(frame)
    ret, thresh = cv2.threshold(overlay_frame,127,255,0)
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(thresh,kernel,iterations=3)
    dilated = dilated.astype(np.uint8)
    dilated = cv2.cvtColor(dilated,cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    ##print("tingz:")
    contour_length = []
    contour_exists = True

    for s in contours:
            contour_length.append(len(s))
    try:
        main_contour = contour_length.index(max(contour_length))
        contour_length.remove(contour_length[main_contour])
    except:
        main_contour=0
        contours=[0]
        contour_exists = False

    try:
        if contour_length.index(max(contour_length)) >= main_contour:
            main_contour2 = contour_length.index(max(contour_length)) + 1
        else:
            main_contour2 = contour_length.index(max(contour_length))

        ##print(main_contour)
        hull0 = cv2.convexHull(contours[main_contour])
        hull1 = cv2.convexHull(contours[main_contour2])
        hull = np.vstack([hull0, hull1])
    except ValueError:
        if contour_exists:
            hull = cv2.convexHull(contours[main_contour])
        else:
            pass
    if contour_exists:
        rect = cv2.minAreaRect(hull)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],-1,(33,87,229),3)
        tester = cv2.drawContours(frame,[hull],-1,(33,87,229),3)
    
    print(box)
    

    y1_roi = 0
    y2_roi = 0
    x1_roi = 0
    x2_roi = 0
    x_vals = []
    y_vals = []
    for m in box:
        x_vals.append(m[0])
        y_vals.append(m[1])

    x1_roi = min(x_vals)
    x2_roi = max(x_vals)
    y2_roi = max(y_vals)
    y1_roi = min(y_vals)
    x1_roi = int(x1_roi/2)
    ##x2_roi = 720-x1_roi

    roi = naturalbgr_frame[y1_roi:y2_roi,x1_roi:x2_roi]
    

    blue,green,red = cv2.split(roi)
    ##print(blue)
    lower = np.array([220])
    upper = np.array([255])

    mask = cv2.inRange(blue,lower,upper)

    edges = cv2.Canny(mask,50,200)

    lines = cv2.HoughLines(edges, 1, np.pi/180, 60)

    void = np.zeros((y2_roi-y1_roi,x2_roi-x1_roi,3))


    if len(positive_slope) != 0:
        px1_total = 0
        px2_total = 0
        py1_total = 0
        py2_total = 0
        positive_slope_avg = 0
        positive_slope_total = 0

    if len(negative_slope) != 0:
        nx1_total = 0
        nx2_total = 0
        ny1_total = 0
        ny2_total = 0
        negative_slope_avg = 0
        negative_slope_total = 0

    positive_slope = []

    negative_slope = []
    
    try:
        for r_theta in lines:
            arr = np.array(r_theta[0], dtype=np.float64)
            r, theta = arr
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*r
            y0 = b*r
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            ##print(x1,y1,x2,y2)
            try:
                m1=(y2-y1)/(x2-x1)
                t=0.6
                if m1 > t or m1 < -t:
                    if m1 > 0:
                        positive_slope.append([x1,x2,y1,y2,m1])
                    else:
                        negative_slope.append([x1,x2,y1,y2,m1])
                    
                    cv2.line(void, (x1, y1), (x2, y2), (0, 0, 255), 2)
            except ZeroDivisionError:
                pass



        for line in positive_slope:
            positive_slope_total = positive_slope_total + line[4]
            
            px1_total = px1_total + line[0]
            px2_total = px2_total + line[1]
            py1_total = py1_total + line[2]
            py2_total = py2_total + line[3]
        
        px1 = px1_total/len(positive_slope)
        px2 = px2_total/len(positive_slope)
        py1 = py1_total/len(positive_slope)
        py2 = py2_total/len(positive_slope)

        positive_slope_avg = positive_slope_total/len(positive_slope)
        


        py1 = (y2_roi-y1_roi)*.25

        px1 = (py1-py2+positive_slope_avg*px2)/positive_slope_avg 

        py2 = y2_roi-y1_roi

        px2 = (py2-py1+positive_slope_avg*px1)/positive_slope_avg 

        

        for line in negative_slope:
            negative_slope_total = negative_slope_total + line[4]
            nx1_total = nx1_total + line[0]
            nx2_total = nx2_total + line[1]
            ny1_total = ny1_total + line[2]
            ny2_total = ny2_total + line[3]
        
        nx1 = nx1_total/len(negative_slope)
        nx2 = nx2_total/len(negative_slope)
        ny1 = ny1_total/len(negative_slope)
        ny2 = ny2_total/len(negative_slope)
        ##print("length",len(negative_slope))

        ##print(nx1,nx2,ny1,ny2,negative_slope_avg)
        negative_slope_avg = negative_slope_total/len(negative_slope)

        ny2 = (y2_roi-y1_roi)*.25

        nx2 = (ny2-ny1+negative_slope_avg*nx1)/negative_slope_avg 

        ny1 = y2_roi-y1_roi

        nx1 = (ny1-ny2+negative_slope_avg*nx2)/negative_slope_avg 

        mx1 = (nx2+px1)/2

        my1 = (y2_roi-y1_roi)*.25

        mx2 = (nx1+px2)/2

        my2 = y2_roi-y1_roi

        if (nx2 < px1) and (((px1+px2)/2-(nx1+nx2)/2) < 700 and ((px1+px2)/2-(nx1+nx2)/2) > 150):
            cv2.line(void, (int(px1), int(py1)), (int(px2), int(py2)), (255, 0, 255), 4)
            cv2.line(frame, (int(px1+x1_roi), int(py1+y1_roi)), (int(px2+x1_roi), int(py2+y1_roi)), (0, 0, 255), 4)
        
            cv2.line(void, (int(nx1), int(ny1)), (int(nx2), int(ny2)), (255, 0, 255), 4)
            cv2.line(frame, (int(nx1+x1_roi), int(ny1+y1_roi)), (int(nx2+x1_roi), int(ny2+y1_roi)), (0, 0, 255), 4)

            cv2.line(void, (int(mx1), int(my1)), (int(mx2), int(my2)), (0, 255, 255), 4)
            cv2.line(frame, (int(mx1+x1_roi), int(my1+y1_roi)), (int(mx2+x1_roi), int(my2+y1_roi)), (0, 255, 255), 4)
        else:
            print("broken")
            

            



        
    except ZeroDivisionError:
        if (nx2 < px1 and ((px1+px2)/2-(nx1+nx2)/2) < 700 and ((px1+px2)/2-(nx1+nx2)/2) > 150):
            mx1 = (nx2+px1)/2

            my1 = (y2_roi-y1_roi)*.25

            mx2 = (nx1+px2)/2

            my2 = y2_roi-y1_roi
            cv2.line(void, (int(nx1), int(ny1)), (int(nx2), int(ny2)), (255, 0, 255), 4)
            cv2.line(void, (int(px1), int(py1)), (int(px2), int(py2)), (255, 0, 255), 4)
            cv2.line(void, (int(mx1), int(my1)), (int(mx2), int(my2)), (0, 255, 255), 4)
            cv2.line(frame, (int(px1+x1_roi), int(py1+y1_roi)), (int(px2+x1_roi), int(py2+y1_roi)), (0, 0, 255), 4)
            cv2.line(frame, (int(nx1+x1_roi), int(ny1+y1_roi)), (int(nx2+x1_roi), int(ny2+y1_roi)), (0, 0, 255), 4)
            cv2.line(frame, (int(mx1+x1_roi), int(my1+y1_roi)), (int(mx2+x1_roi), int(my2+y1_roi)), (0, 255, 255), 4)


    except TypeError:
        pass
        


        

    

    return frame


