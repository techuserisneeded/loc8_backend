import cv2
import base64
import requests
import re
import os
import math
import ffmpeg
from app.utils.helpers import haversine_distance

api_key = os.getenv('GOOGLE_VISION_API_KEY')

def detect_text(image_content):
    vision_api_url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(api_key)
    image_content_base64 = base64.b64encode(image_content).decode('utf-8')

    payload = {
        "requests": [
            {
                "image": {
                    "content": image_content_base64
                },
                "features": [
                    {
                        "type": "TEXT_DETECTION"
                    }
                ]
            }
        ]
    }

    response = requests.post(vision_api_url, json=payload)
    data = response.json()

    return data

def get_coordinates_from_video(video_path, interval=10):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)

    frame_rate = math.ceil(frame_rate)
    frame_count = 0
    detected_texts = []

    if not cap.isOpened():
        print("Error: Failed to open video capture")
        return

    while True:

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count + interval * frame_rate)
        ret, frame = cap.read()

        if not ret:
            print("End of video")
            break

        # Convert frame to image content
        height, width, _ = frame.shape
        roi_top = int(0.85 * height)
        roi_bottom = int(0.95 * height)
        roi_left = int(0.13 * width)
        roi_right = int(0.57 * width)
        roi = frame[roi_top:roi_bottom, roi_left:roi_right]

        _, buffer = cv2.imencode('.jpg', roi)
        image_content = buffer.tobytes()

        # print('Detected text at {} seconds'.format(frame_count // frame_rate))

        api_response = detect_text(image_content)

        # Process API response
        if api_response and 'textAnnotations' in api_response['responses'][0]:
            detected_text = api_response['responses'][0]['textAnnotations'][0]['description']

            print('Detected text at {} seconds: {}'.format(frame_count // frame_rate, detected_text))

            data_from_detected_text = detected_text_to_data(detected_text)

            if data_from_detected_text != None:
                detected_texts.append(data_from_detected_text)
                
        else:
            print('No text detected at {} seconds.'.format(frame_count // frame_rate))

        frame_count += interval * frame_rate

    cap.release()
    return detected_texts

def detected_text_to_data(response_text=""):
    match = re.search( r'([0O]|\d+)km/h\s*[,.\s]*([NS]\d+\.\d+)[,.\s]*([EW]\d+\.\d+)' , response_text)
    if match:
        speed = match.group(1)
        if speed == 'O':
            speed = 0
        else:
            speed = int(speed)
            
        latitude = float(match.group(2).replace("N", ""))
        longitude = float(match.group(3).replace("E", ""))
        print(speed, latitude, longitude)


        return speed, latitude, longitude
        
    else:
        return None

def compress_video(input_file, output_file):
  input_stream = ffmpeg.input(input_file)
  output_stream = input_stream.output(output_file, crf=18)
  ffmpeg.run(output_stream)

def calculate_avg_speed_stretched(video_coordinates=[]):

    stretched_in_meters = 0.0
    avg_speed = 0

    speed = 0
    for coords in video_coordinates:
        speed = speed + int(coords['speed'])

    if len(video_coordinates) > 0:
        avg_speed = speed / len(video_coordinates)

    for i in range(len(video_coordinates) - 1):
        lat1, lon1 = video_coordinates[i]['latitude'], video_coordinates[i]['longitude']
        lat2, lon2 = video_coordinates[i + 1]['latitude'], video_coordinates[i + 1]['longitude']

        stretched_in_meters += haversine_distance(lat1, lon1, lat2, lon2)

    return avg_speed, round(stretched_in_meters, 2)
