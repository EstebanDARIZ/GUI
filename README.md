#  Video Player with Detection Navigation

This project provides a simple **PySide6-based GUI** that allows you to:
- Play and pause a video.
- Display detection timestamps as red markers on the timeline.
- Jump between detections using navigation buttons.

It is designed to visualize detections or events stored as timestamps in a text file.

---

## Dependencies

This project requires **Python 3.10+** 

You can install dependencies using:

pip install -r requirements.txt

---

## Detection File Format

The detection file should be a plain text file (.txt) containing one timestamp per line, expressed in seconds.
These values are automatically converted to milliseconds for synchronization with the video player.

---

## Configuration

Set the video and detection file paths in config.py:

VIDEO_PATH = "/absolute/path/to/your/video.mp4"
FILE_PATH = "/absolute/path/to/detections.txt"

Make sure both files exist and are accessible.

---

## Running the Application

Run the graphical interface with:
python main_gui.py

---

## Author

Developed by Esteban DREAU DARUZCUREN

--- 