import cv2
import base64
import requests
import time

# change the ip to the server
server_address = "http://127.0.0.1:5000"
video_file = 'Vid1.mp4'

# Définition des configurations pour chaque intersection
intersection1 = {'red': 11, 'orange': 13, 'green': 15}
intersection2 = {'red': 16, 'orange': 18, 'green': 22}
intersection3 = {'red': 29, 'orange': 31, 'green': 33}
intersection4 = {'red': 35, 'orange': 37, 'green': 40}

def set_traffic_light(intersection, traffic_light_state):
    print(f"set_traffic_light({intersection}, {traffic_light_state})")

def capture_video_segment(duration=5):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_file, fourcc, 20.0, (640, 480))
    
    start_time = time.time()
    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break
    
    cap.release()
    out.release()
    with open(video_file, 'rb') as f:
        video_data = f.read()
    return video_data

def send_video_to_server(video_data):
    video_base64 = base64.b64encode(video_data).decode('utf-8')
    response = requests.post(f'{server_address}/process_video', json={'video': video_base64})
    return response.json()['vehicle_count']

try:
    while True:
        video_segment = capture_video_segment()
        
        total_counts = []
        zones = [
            {'x_min': 0, 'x_max': 240, 'y_min': 120, 'y_max': 280},
            {'x_min': 480, 'x_max': 720, 'y_min': 100, 'y_max': 280},
            {'x_min': 240, 'x_max': 480, 'y_min': 0, 'y_max': 120},
            {'x_min': 240, 'x_max': 480, 'y_min': 270, 'y_max': 360}
        ]
        
        for zone in zones:
            count = send_video_to_server(video_segment)
            total_counts.append(count)

        total_count_12 = total_counts[0] + total_counts[1]
        total_count_34 = total_counts[2] + total_counts[3]

        if total_count_34 > total_count_12:
            set_traffic_light(intersection1, "red")
            set_traffic_light(intersection2, "red")
            set_traffic_light(intersection3, "green")
            set_traffic_light(intersection4, "green")
        else:
            set_traffic_light(intersection1, "green")
            set_traffic_light(intersection2, "green")
            set_traffic_light(intersection3, "red")
            set_traffic_light(intersection4, "red")

        time.sleep(5)
except KeyboardInterrupt:
    pass
    #GPIO.cleanup()
