import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import json
import io
import locale
print(locale.getpreferredencoding())
import math
import cv2
# from tqdm.notebook import tqdm
from tqdm import tqdm
import numpy as np
import locale

def getpreferredencoding(do_setlocale = True):
    return "UTF-8"
locale.getpreferredencoding = getpreferredencoding
from werkzeug.utils import secure_filename
import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

from flask import Flask, request, jsonify
from yolox.tracker.byte_tracker import BYTETracker, STrack
from onemetric.cv.utils.iou import box_iou_batch
from dataclasses import dataclass
import yolox
from supervision.draw.color import ColorPalette
from supervision.geometry.dataclasses import Point
from supervision.video.dataclasses import VideoInfo
from supervision.video.source import get_video_frames_generator
from supervision.video.sink import VideoSink
from supervision.notebook.utils import show_frame_in_notebook
from supervision.tools.detections import Detections, BoxAnnotator
from supervision.tools.line_counter import LineCounter, LineCounterAnnotator
from typing import List
from ultralytics import YOLO


@dataclass(frozen=True)
class BYTETrackerArgs:
    track_thresh: float = 0.57
    track_buffer: int = 20
    match_thresh: float = 0.8
    aspect_ratio_thresh: int = -1
    min_box_area: float = 0.0
    mot20: bool = False


model = YOLO("best16.pt")
np.float = float
np.int = int   #module 'numpy' has no attribute 'int'
np.object = object    #module 'numpy' has no attribute 'object'
np.bool = bool

CLASS_NAMES_DICT = "BillBoard"
CLASS_ID = [0]
# TARGET_VIDEO_PATH = f"./instance/BillBoardDetectionandCounting.mp4"

# converts Detections into format that can be consumed by match_detections_with_tracks function
def detections2boxes(detections: Detections) -> np.ndarray:
    return np.hstack((
        detections.xyxy,
        detections.confidence[:, np.newaxis]
    ))


# converts List[STrack] into format that can be consumed by match_detections_with_tracks function
def tracks2boxes(tracks: List[STrack]) -> np.ndarray:
    return np.array([
        track.tlbr
        for track
        in tracks
    ], dtype=float)

# matches our bounding boxes with predictions
def match_detections_with_tracks(
    detections: Detections,
    tracks: List[STrack]
) -> Detections:
    if not np.any(detections.xyxy) or len(tracks) == 0:
        return np.empty((0,))

    tracks_boxes = tracks2boxes(tracks=tracks)
    iou = box_iou_batch(tracks_boxes, detections.xyxy)
    track2detection = np.argmax(iou, axis=1)

    tracker_ids = [None] * len(detections)

    for tracker_index, detection_index in enumerate(track2detection):
        if iou[tracker_index, detection_index] != 0:
            tracker_ids[detection_index] = tracks[tracker_index].track_id

    return tracker_ids

def calculate_bbox_area(box,image_width,image_height):
    x1, y1, x2, y2 = box
    width = x2 - x1
    height = y2 - y1
    return ((width * height)* 100)/(0.65 *image_width * image_height)

def get_region(box, image_width,image_height):
  x1,y1,x2,y2 = box

  centre_billboard_x = int(x1+x2)/2
  centre_billboard_y = int(y1+y2)/2
  centre_image_x = int(image_width/2)
  centre_y = int(0.75*image_height/2)

  if((abs(centre_billboard_x - centre_image_x) <= image_width/8 and
      abs(centre_billboard_y - centre_y) <= 0.65*image_height/2)):
    return "Central"
  elif((abs(centre_billboard_x - centre_image_x) > image_width/8 and
        abs(centre_billboard_x - centre_image_x) <= 2*image_width/8 and
        abs(centre_billboard_y - centre_y) <= 0.65*image_height/2) or
        ((abs(centre_billboard_x - centre_image_x) <= image_width/8) and
         abs(centre_billboard_y - centre_y) > 0.65*image_height/2)):
    return "Near P"
  elif(abs(centre_billboard_x - centre_image_x) > 2*image_width/8 and
       abs(centre_billboard_x - centre_image_x) <= 3*image_width/8 and
       abs(centre_billboard_y - centre_y) <= 0.65*image_height/2 or
        ((abs(centre_billboard_x - centre_image_x) <= 2*image_width/8) and
         abs(centre_billboard_y - centre_y) > 0.65*image_height/2)):
    return "Mid P"
  else:
    return "Far P"


def draw_rectangle(frame, image_width,image_height):
  start_point_orange = (int(1*image_width/8), int(0.1*image_height))
  end_point_orange = (int(7*image_width/8),int(image_height - 0.25*image_height))
  cv2.rectangle(frame,start_point_orange,end_point_orange,(0,155,252),3)

  start_point_yellow = (int(2*image_width/8), int(0.1*image_height))
  end_point_yellow = (int(6*image_width/8),int(image_height - 0.25*image_height))
  cv2.rectangle(frame,start_point_yellow,end_point_yellow,(0,255,255),3)

  start_point_green = (int(3*image_width/8), int(0.1*image_height))
  end_point_green = (int(5*image_width/8),int(image_height - 0.25*image_height))
  cv2.rectangle(frame,start_point_green,end_point_green,(0,255,0),3)

  start_point_line_yellow = (int(3*image_width/8), int(0.1*image_height))
  end_point_line_yellow = (int(3*image_width/8), 0)
  cv2.line(frame,start_point_line_yellow , end_point_line_yellow,(0,255,255) , 3)

  start_point_line_orange_1 = (int(6*image_width/8), int(0.1*image_height))
  end_point_line_orange_1 = (int(6*image_width/8), 0)
  cv2.line(frame,start_point_line_orange_1 , end_point_line_orange_1,(0,155,252) , 3)


  start_point_line_yellow_2 = (int(5*image_width/8), int(0.1*image_height))
  end_point_line_yellow_2 = (int(5*image_width/8), 0)
  cv2.line(frame,start_point_line_yellow_2 , end_point_line_yellow_2,(0,255,255) , 3)

  start_point_line_orange_2 = (int(2*image_width/8), int(0.1*image_height))
  end_point_line_orange_2 = (int(2*image_width/8), 0)
  cv2.line(frame,start_point_line_orange_2 , end_point_line_orange_2,(0,155,252) , 3)

def euclidean_distance(point1, point2):
  return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def write_text(image, label, pos = (0,0),font=cv2.FONT_ITALIC, font_scale=1.1, text_color=(255, 0, 0), font_thickness=3, text_color_bg=(0,225,255)
          ):
    x, y = pos
    text_size, _ = cv2.getTextSize(label, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(image, pos, (x + text_w, y + text_h + 5), text_color_bg, -1)
    cv2.putText(image, label, (int(x), int(y + text_h + font_scale - 1)), font, font_scale, text_color, font_thickness)
    return text_size

y_thres = 70
def draw_bounding_boxes(File, output_file_path, progress_callback):

    TARGET_VIDEO_PATH = output_file_path

    byte_tracker = BYTETracker(BYTETrackerArgs())
    video_info = VideoInfo.from_video_path(File)
    generator = get_video_frames_generator(File)
    # box_annotator = BoxAnnotator(color=ColorPalette.DEFAULT, thickness=4, text_thickness=4, text_scale=2)
    line_annotator = LineCounterAnnotator(thickness=4, text_thickness=4, text_scale=2)

    # Create VideoWriter object to save the modified video
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    output_video = cv2.VideoWriter(TARGET_VIDEO_PATH, fourcc, video_info.fps, (video_info.width, video_info.height))

    # Dictionary to store the start frame and end frame of each detected billboard
    billboard_frames = {}
    billboard_regions = {}
    total_frames = video_info.total_frames

    for frame_idx, frame in enumerate(tqdm(generator, total=video_info.total_frames)):
        results = model(frame, conf=0.57)
        detections = Detections(
            xyxy=results[0].boxes.xyxy.cpu().numpy(),
            confidence=results[0].boxes.conf.cpu().numpy(),
            class_id=results[0].boxes.cls.cpu().numpy().astype(int),
        )
        mask = np.array([class_id in CLASS_ID for class_id in detections.class_id], dtype=bool)
        detections.filter(mask=mask, inplace=True)
        tracks = byte_tracker.update(
            output_results=detections2boxes(detections=detections),
            img_info=frame.shape,
            img_size=frame.shape
        )
        tracker_id = match_detections_with_tracks(detections=detections, tracks=tracks)
        detections.tracker_id = np.array(tracker_id)
        mask = np.array([tracker_id is not None for tracker_id in detections.tracker_id], dtype=bool)
        detections.filter(mask=mask, inplace=True)


        for box, tracker_id, confidence in zip(detections.xyxy, detections.tracker_id, detections.confidence):
            if tracker_id not in billboard_frames:
                # If the billboard is detected for the first time, record the start frame
                billboard_frames[tracker_id] = {'start_frame': frame_idx, 'end_frame': None, 'center': None, 'areas': [], 'confidences': []}
                billboard_regions[tracker_id] = {"Central":0,"Near P":0,"Mid P":0,"Far P":0, "Central Dist" : 0, "Near P Dist" : 0, "Mid P Dist":0, "Far P Dist":0}
            else:
                # If the billboard is already being tracked, update the end frame
                billboard_frames[tracker_id]['end_frame'] = frame_idx
            # Calculate center coordinates of the billboard
            center_x = (box[0] + box[2]) / 2
            center_y = (box[1] + box[3]) / 2
            billboard_frames[tracker_id]['center'] = (center_x, center_y)
            # Draw bounding box around the billboard
            draw_rectangle(frame, frame.shape[1],frame.shape[0])
            cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0,0,255), 3)

            # Display confidence score as label
            area = calculate_bbox_area(box, frame.shape[1], frame.shape[0])
            billboard_frames[tracker_id]['areas'].append(area)
            billboard_frames[tracker_id]['confidences'].append(confidence)
            region = get_region(box,frame.shape[1],frame.shape[0])
            region_area = region + " Dist"
            billboard_regions[tracker_id][region]+=1
            x1,y1,x2,y2 = box
            bill_centre = [int((x1+x2)/2),int((y1+y2)/2)]
            centre_img = [frame.shape[1],frame.shape[0]]

            billboard_regions[tracker_id][region_area]+= euclidean_distance(bill_centre,centre_img)
            label = f"ID:{tracker_id}"
            label1 = f"{confidence:.2f}"
            label2 = f"{calculate_bbox_area(box, frame.shape[1],frame.shape[0]):.3f}%"
            label3 = f"{get_region(box,frame.shape[1],frame.shape[0])}"
            w0,h0 = write_text(frame, label, (int(box[0]), int(box[1]) - 10 + y_thres), cv2.FONT_ITALIC, 1.1, (255, 0, 0), 3, (0,255,255))
            w,h = write_text(frame, label1, (int(box[0]), int(box[1])+ h0 + y_thres), cv2.FONT_ITALIC, 1.1, (255, 0, 0), 3, (0,255,255))
            w1,h1 = write_text(frame, label3, (int(box[0]), int(box[1]) + h + h0 + 10 + y_thres), cv2.FONT_ITALIC,1.1, (255, 0,0), 3, (0,255,255))
            write_text(frame, label2, (int(box[0]), int(box[1])+ h + h0 +  h1+ 20 + y_thres), cv2.FONT_ITALIC, 1.1, (255, 0,0), 3, (0,255,255))
        # Write the modified frame to the output video
        output_video.write(frame)

        # report the percentage
        progress_percentage = int((frame_idx + 1) / total_frames * 100)
        progress_callback(progress_percentage)

    # Release the VideoWriter object
    output_video.release()

    # After processing all frames, calculate the duration of visibility and distance to center for each billboard
    visibility_durations = {}
    average_areas = {}
    average_confidence = {}
    for tracker_id, frames in billboard_frames.items():
        start_frame = frames['start_frame']
        end_frame = frames['end_frame']
        center = frames['center']
        areas = frames['areas']
        confidences = frames['confidences']

        if confidences:
            average_confidence[tracker_id] = sum(confidences) / len(confidences)
        else:
            average_confidence[tracker_id] = 0


        if areas:
            average_area = sum(areas) / len(areas)
            average_areas[tracker_id] = average_area
        if end_frame is not None:
            visibility_duration = end_frame - start_frame + 1
            # Calculate the distance between the center of the billboard and the center of the image
            image_center = (video_info.width / 2, video_info.height / 2)
            distance_to_center = euclidean_distance(center, image_center)

            if (billboard_regions[tracker_id]['Central'])!=0:
              billboard_regions[tracker_id]['Central Dist'] = billboard_regions[tracker_id]['Central Dist']/billboard_regions[tracker_id]['Central']
              billboard_regions[tracker_id]['Central Dist'] = (billboard_regions[tracker_id]['Central Dist']*100/math.sqrt(frame.shape[1]*frame.shape[1] + frame.shape[0]*frame.shape[0]))
            if (billboard_regions[tracker_id]['Near P'])!=0:
              billboard_regions[tracker_id]['Near P Dist'] = billboard_regions[tracker_id]['Near P Dist']/billboard_regions[tracker_id]['Near P']
              billboard_regions[tracker_id]['Near P Dist'] = (billboard_regions[tracker_id]['Near P Dist']*100/math.sqrt(frame.shape[1]*frame.shape[1] + frame.shape[0]*frame.shape[0]))
            if (billboard_regions[tracker_id]['Mid P'])!=0:
              billboard_regions[tracker_id]['Mid P Dist'] = billboard_regions[tracker_id]['Mid P Dist']/billboard_regions[tracker_id]['Mid P']
              billboard_regions[tracker_id]['Mid P Dist'] = (billboard_regions[tracker_id]['Mid P Dist']*100/math.sqrt(frame.shape[1]*frame.shape[1] + frame.shape[0]*frame.shape[0]))
            if (billboard_regions[tracker_id]['Far P'])!=0:
              billboard_regions[tracker_id]['Far P Dist'] = billboard_regions[tracker_id]['Far P Dist']/billboard_regions[tracker_id]['Far P']
              billboard_regions[tracker_id]['Far P Dist'] = (billboard_regions[tracker_id]['Far P Dist']*100/math.sqrt(frame.shape[1]*frame.shape[1] + frame.shape[0]*frame.shape[0]))
            billboard_regions[tracker_id]['Central'] = billboard_regions[tracker_id]['Central']/video_info.fps
            billboard_regions[tracker_id]['Near P'] = billboard_regions[tracker_id]['Near P']/video_info.fps
            billboard_regions[tracker_id]['Mid P'] = billboard_regions[tracker_id]['Mid P']/video_info.fps
            billboard_regions[tracker_id]['Far P'] = billboard_regions[tracker_id]['Far P']/video_info.fps

            visibility_durations[tracker_id] = {
                'visibility_duration': visibility_duration/video_info.fps,
                'distance_to_center': (distance_to_center*100/math.sqrt(frame.shape[1]*frame.shape[1] + frame.shape[0]*frame.shape[0])),
                'BillBoard_Region_Duration and Distance':billboard_regions[tracker_id],
                'Average Areas': average_areas[tracker_id],
                'Confidence': average_confidence[tracker_id]
            }
            # print(video_info.fps)
    return visibility_durations



def video_processing(dest, output_file_path=f"./instance/BillBoardDetectionandCounting.mp4", progress_callback=None):
    vcd =draw_bounding_boxes(dest, output_file_path, progress_callback)
    print(vcd)
    return vcd


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(
    app.instance_path, 
    'uploads'
)
try: 
    os.makedirs(app.config['UPLOAD_FOLDER'])
except: 
    pass 

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('video')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            dest = os.path.join(
                app.config['UPLOAD_FOLDER'], 
                secure_filename(file.filename)
            )
            # Save the file on the server.
            file.save(dest)
            vcd = video_processing(dest)
            os.remove(dest)
            vcd2 = str(vcd)
            vcd3 = vcd2[0:2]
            # data = {"predicted_class": predicted_class, "accuracy": int(accuracy)}
            return jsonify({"Result": vcd2})
        except Exception as e:
            return jsonify({"error": str(e)})

    return jsonify({"msg": "working"})
