Study Guard is a student productivity monitoring system that uses

computer vision to detect mobile phone usage during study sessions.

If distraction exceeds a defined threshold, a motivational video is played.



\## Features

\- Real-time mobile phone detection

\- Buffer-based trigger mechanism

\- Automatic motivational feedback



\## Tech Stack

\- Python

\- OpenCV

\- YOLO (Object Detection)

\- NumPy



\## How it works

1\. Laptop camera monitors the study session

2\. Mobile phone usage is detected using YOLO

3\. Repeated distraction triggers a warning or video(.mp4) 



\## Note

Large files such as model weights (.pt) and videos (.mp4) are excluded

from the repository and must be added locally before execution.



