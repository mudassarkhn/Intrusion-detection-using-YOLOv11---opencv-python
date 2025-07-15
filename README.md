# Person Detection System

This project implements a person detection system using the YOLO (You Only Look Once) model. The system processes video input, detects persons in the frames, and triggers an alarm sound when motion of person is detected within a specified polygon area.

## How It Works

1. **Model Loading**: The system loads a pre-trained YOLO model (`yolo11m.pt`) to perform object detection.
2. **Video Processing**: It captures video from a specified file and processes every third frame to optimize performance.
3. **Motion Detection**: The system tracks detected objects (persons) across frames. If a person's position changes, it flags motion detection.
4. **Polygon Area**: Users can define a polygon area on the video frame using mouse clicks. If a detected person enters this area, an alarm sound is played.
5. **Output**: The processed video frames are displayed in real-time, with bounding boxes around detected persons and an indication of motion detection.

## Requirements

To run this project, you need the following Python packages:

- `opencv-python`
- `numpy`
- `ultralytics`
- `cvzone`
- `playsound`
- `matplotlib`

You can install these packages using the following command:
```bash
pip install -r requirements.txt
```

## How to Run the Code

1. **Clone the Repository**: Clone this repository to your local machine.

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Download the YOLO Model**: Ensure you have the YOLO model file (`yolo11n.pt`) in the `Model` directory.

3. **Prepare the Video**: Place your video file (e.g., `video1.mp4`) in the `Testing videos` directory.

4. **Run the Script**: Execute the main code file.

   ```bash
   python main_code_file.py
   ```

5. **Define the Polygon**: Click on the video window to define the polygon area for motion detection.

6. **Stop the Program**: Press the 'q' key to exit the program.

## Notes

- Ensure that the `alarm.mp3` file is available in the same directory as the script for the alarm sound to work.
- Adjust the output filename in the `cv2.VideoWriter` initialization if needed.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
numpy==1.21.2
ultralytics==8.0.0
cvzone==1.5.0
playsound==1.3.0
matplotlib==3.4.3