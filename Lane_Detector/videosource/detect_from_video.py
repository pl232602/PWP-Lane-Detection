import numpy as np
import argparse
import tensorflow as tf
import cv2

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile


def load_model(model_path):
    model = tf.saved_model.load(model_path)
    return model


def run_inference_for_single_image(model, image):
    image = np.asarray(image)
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis,...]
    
    # Run inference
    output_dict = model(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key: value[0, :num_detections].numpy()
                   for key, value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
   
    # Handle models with masks:
    if 'detection_masks' in output_dict:
        # Reframe the the bbox mask to the image size.
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                                    output_dict['detection_masks'], output_dict['detection_boxes'],
                                    image.shape[0], image.shape[1])      
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, tf.uint8)
        output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
    
    return output_dict

#for use with acutal videostream
def run_arrow_inference(model, image, secondary_image):
    image_np = image
    second_image = secondary_image
    output_dict = run_inference_for_single_image(model, image_np)
    detection_class='null'
    for detection in output_dict['detection_scores']:
            if detection > 0.35:
                detection_index = 0
                print('first',detection_index)
                for i in output_dict['detection_scores']:
                    if i == detection:
                        break
                    detection_index = detection_index + 1
                print('index',detection_index)
                print(output_dict['detection_boxes'][0])
                proportional_size = output_dict['detection_boxes'][detection_index]
                h,w,c = second_image.shape
                print(proportional_size)
                print(h,w,c) 
                y1 = int(h*proportional_size[0])
                x1 = int(w*proportional_size[1])
                y2 = int(h*proportional_size[2])
                x2 = int(w*proportional_size[3])
                print(x1,y1,x2,y2)
                print(output_dict['detection_scores'])
                second_image = cv2.rectangle(second_image,(x1,y1),(x2,y2),(255,0,0),5)
                detection_class = output_dict['detection_classes'][detection_index]
                print('Detection class',detection_class)
                if detection_class == 1:
                    detection_class = 'left'
                elif detection_class == 2:
                    detection_class = 'right'
    return second_image, detection_class

#for use testing
def run_inference(model, category_index, cap):
    while cap.isOpened():
        ret, image_np = cap.read()
        if not ret:
            break

        output_dict = run_inference_for_single_image(model, image_np)
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            category_index,
            instance_masks=output_dict.get('detection_masks_reframed', None),
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=.3)
        for detection in output_dict['detection_scores']:
            if detection > 0.3:
                detection_index = 0
                print('first',detection_index)
                for i in output_dict['detection_scores']:
                    if i == detection:
                        break
                    detection_index = detection_index + 1
                print('index',detection_index)
                print(output_dict['detection_boxes'][0])
                proportional_size = output_dict['detection_boxes'][detection_index]
                h,w,c = image_np.shape
                print(proportional_size)
                print(h,w,c) 
                y1 = int(h*proportional_size[0])
                x1 = int(w*proportional_size[1])
                y2 = int(h*proportional_size[2])
                x2 = int(w*proportional_size[3])
                print(x1,y1,x2,y2)
                print(output_dict['detection_scores'])
                image_np = cv2.rectangle(image_np,(x1,y1),(x2,y2),(255,0,0),5)
                detection_class = output_dict['detection_classes'][detection_index]



        cv2.imshow('object_detection', cv2.resize(image_np, (1280, 720)))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break



# python .\detect_from_video.py -m ssd_mobilenet_v2_320x320_coco17_tpu-8\saved_model -l .\data\mscoco_label_map.pbtxt -v .\myVideo.mp4
#detection_model = load_model(r'C:\Users\Niles Alexis\Documents\PWP Lane Detection\PWP-Lane-Detection\Lane_Detector\videosource\arrow_detection_model')
#category_index = label_map_util.create_category_index_from_labelmap(r'C:\Users\Niles Alexis\Documents\PWP Lane Detection\PWP-Lane-Detection\Lane_Detector\videosource\arrow_detection_model\arrowlabelmap.pbtxt', use_display_name=True)
#cap = cv2.VideoCapture(r'C:\Users\Niles Alexis\Documents\PWP Lane Detection\PWP-Lane-Detection\Lane_Detector\videosource\realvid9.MOV')
#run_inference(detection_model, category_index, cap)

