import cv2
import mediapipe as mp
import socket
import json
import time

# UDP
UDP_IP = "127.0.0.1"
UDP_PORT = 5065
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# initial
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

def cc(landmarks):
    lmks = []
    for _ in landmarks:
        x = _.x * 0.3
        y = _.y * 0.3
        z = _.z * 0.7

        lmks.append({
            "x": x,
            "y": 1 - y,
            "z": -z,
            "id": len(lmks)
        })
    return lmks




cap = cv2.VideoCapture(0)




while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue
    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rst = hands.process(rgb_frame)
    
    data = {
        "landmarks": [],
        "timestamp": time.time()
    }
    
    if rst.multi_hand_landmarks:
        for _ in rst.multi_hand_landmarks:
            lmks = cc(_.landmark)
            data["landmarks"] = lmks
            
            if len(lmks) > 20:
                print(f"Wrist: ({lmks[0]['x']:.2f}, {lmks[0]['y']:.2f}, {lmks[0]['z']:.2f})")
                print(f"Index Tip: ({lmks[8]['x']:.2f}, {lmks[8]['y']:.2f}, {lmks[8]['z']:.2f})")
    
    # send
    data_str = json.dumps(data)
    sock.sendto(data_str.encode('utf-8'), (UDP_IP, UDP_PORT))
    
'''    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break'''

cap.release()
cv2.destroyAllWindows()
sock.close()