from videosource import camera
from videosource import roadsense
from videosource import detect_from_video
import cv2


global model_path
model_path = r'C:\Users\Niles Alexis\Documents\PWP Lane Detection\PWP-Lane-Detection\Lane_Detector\videosource\arrow_detection_model'

global lane_status
lane_status = 'null'

def gen_overlay():
    for local_frame in camera.gen_frames():#generate an overlay based on the data from object detection
        natural_frame = local_frame
        overlay_frame = roadsense.roadsense(local_frame)
        yield (overlay_frame, natural_frame)
    pass

def gen_object_detection():
    global lane_status
    model = detect_from_video.load_model(model_path)
    for overlay_frame, natural_frame in gen_overlay():
        layered_frame, new_lane_status = detect_from_video.run_arrow_inference(model,natural_frame, overlay_frame)
        font = cv2.FONT_HERSHEY_SIMPLEX
        if new_lane_status == "left":
            cv2.putText(layered_frame,'Currently Turning Left',(50,50),font,1,(255,255,255),3)
        elif new_lane_status == "right":
            cv2.putText(layered_frame,'Currently Turning Right',(50,50),font,1,(255,255,255),3)
        else:
            cv2.putText(layered_frame,'No Turn Lane Detected',(50,50),font,1,(255,255,255),3)
       
        print('current lane status',lane_status)
        layered_frame = overlay_frame
        yield(layered_frame)


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
