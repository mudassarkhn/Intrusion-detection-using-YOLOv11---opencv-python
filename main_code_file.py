import cv2
import numpy as np
from ultralytics import YOLO
import cvzone
from playsound import playsound
from matplotlib.path import Path


# Load the YOLO11 model
model = YOLO("Model/yolo11m.pt")
names = model.model.names
# print(names)

# Open the video file
cap = cv2.VideoCapture('Testing Resources/video1.mp4')

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# if you want to save the output of this system in video form
# output = cv2.VideoWriter('output10.mp4', 
#                         cv2.VideoWriter_fourcc(*'mp4v'),
#                         fps//3,  
#                         (1020, 600))

count = 0

# Initialize a dictionary to store the previous centers of track IDs
previous_centers = {}
wait_time = int((1000/fps) * 3)

# Initialize a list to store polygon points
polygon_points = []

# Mouse callback function to capture points
def draw_polygon(event, x, y, flags, param):
    global polygon_points
    if event == cv2.EVENT_LBUTTONDOWN:
        polygon_points.append((x, y))  # Add point to the polygon
    if event == cv2.EVENT_MOUSEMOVE and len(polygon_points) > 0:
        # Draw the polygon while moving the mouse
        temp_frame = frame.copy()
        cv2.polylines(temp_frame, [np.array(polygon_points)], isClosed=False, color=(0, 255, 0), thickness=2)
        cv2.imshow("RGB", temp_frame)

# Set mouse callback
cv2.namedWindow("RGB")
cv2.setMouseCallback("RGB", draw_polygon)

# Function to check if a point is inside the polygon
def is_point_in_polygon(point, polygon):
    if len(polygon) < 3:  # Check if there are enough points to form a polygon
        return False
    path = Path(polygon)
    return path.contains_point(point)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame = cv2.resize(frame, (1020, 600))
    # Run YOLO11 tracking on the frame, persisting tracks between frames
    results = model.track(frame, persist=True,classes=0)
    motion_detected = False  # Flag to check if any motion is detected in the frame
    if results[0].boxes is not None and results[0].boxes.id is not None:
        # Get the boxes (x, y, w, h), class IDs, track IDs, and confidences
        boxes = results[0].boxes.xyxy.int().cpu().tolist()  # Bounding boxes
        class_ids = results[0].boxes.cls.int().cpu().tolist()  # Class IDs
        track_ids = results[0].boxes.id.int().cpu().tolist()  # Track IDs
        confidences = results[0].boxes.conf.cpu().tolist()  # Confidence score
       
        for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
            c = names[class_id]
            x1, y1, x2, y2 = box
            
            # Calculate the center of the bounding box
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            
            # Check for motion
            if track_id in previous_centers:
                prev_center_x, prev_center_y = previous_centers[track_id]
                if (center_x, center_y) != (prev_center_x, prev_center_y):
                    motion_detected = True  # Set the flag if motion is detected
            
            # Update the previous center
            previous_centers[track_id] = (center_x, center_y)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            # cvzone.putTextRect(frame, f'{track_id}', (x1, y2), 1, 1)
            cvzone.putTextRect(frame, f'{c}: {conf:.2f}', (x1, y1), 1, 1, colorT=(255, 255, 255), colorR=(0, 0, 255))

            # Check if the center is within the polygon
            if is_point_in_polygon((center_x, center_y), polygon_points):
                motion_detected = True  # Set the flag if motion is detected
                playsound('alarm.mp3')  # Play the alarm sound
    
    cv2.putText(frame, "Motion Detection:", (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    # Display "Motion Detected" at the top of the window if motion is detected
    if motion_detected:
        cv2.putText(frame, "True", (575, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        playsound('alarm.mp3')

    # Write the frame to output video (uncomment this if you want to save the output)
    # output.write(frame)
    cv2.imshow("RGB", frame)
    if cv2.waitKey(wait_time) & 0xFF == ord("q"):          
       break

# Release everything
cap.release()
#uncomment it if you want to save the output
# output.release() 
cv2.destroyAllWindows()