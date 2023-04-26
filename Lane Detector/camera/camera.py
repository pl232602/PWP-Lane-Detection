import cv2
import numpy as np
import io
from threading import coniditon

def gen_frames(): #generate frames from video source 0 (usually webcam)
    cap = cv2.VideoCapture(0)
    i=0
    while i==0:
        ret, local_frame = cap.read()
        yield (local_frame)


def gen_localhttp_res(): #converts numpy array format frames into bytes to send through flask response(in camera __init__ file) and eventually to webpage (locally generated frames)
    while True:
        for overlay_frame in gen_frames():
            byteframe=cv2.imencode('.jpg', overlay_frame)[1].tobytes()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return False
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
               + byteframe + b'\r\n')
