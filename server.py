from flask import Flask, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import base64

app = Flask(__name__)

# Charger le modèle YOLO
model = YOLO("../Yolo-Weights/yolov8l.pt")
classNames = ["car", "truck", "bus", "motorbike"]

def detect_vehicles(frame):
    results = model(frame, stream=True, conf=0.2)
    totalCount = 0
    for result in results:
        class_ids = result.boxes.cls
        class_names = [model.names[int(cls_id)] for cls_id in class_ids]
        for elmt in class_names:
            if elmt in classNames:
                totalCount += 1
    return totalCount

@app.route('/process_video', methods=['POST'])
def process_video():
    data = request.get_json()
    video_data = base64.b64decode(request.json['video'])
    with open('received_segment.avi', 'wb') as f:
        f.write(video_data) 

    cap = cv2.VideoCapture('received_segment.avi')
    nparr = np.frombuffer(video_data, np.uint8)
    video = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    frame_count = 0
    vehicle_counts = []
    
    #cap = cv2.VideoCapture(video)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        if frame_count % 30 == 0:  # Traiter une frame toutes les 10 frames
            count = detect_vehicles(frame)
            vehicle_counts.append(count)
    
    total_count = sum(vehicle_counts) / len(vehicle_counts) if vehicle_counts else 0
    return jsonify({'vehicle_count': total_count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
