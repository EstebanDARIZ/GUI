import os

BASE_DIR = r"/home/esteban-dreau-darizcuren/doctorat/"

VIDEO_NAME = "Raie"

VIDEO_DIR = os.path.join(BASE_DIR, "dataset", "raw")
VIDEO_PATH = os.path.join(VIDEO_DIR, f"{VIDEO_NAME}.MP4")

RESULTS_DIR = os.path.join(BASE_DIR, "code", "soundDetector", "results")
FILE_PATH = os.path.join(RESULTS_DIR, f"{VIDEO_NAME}_results.txt")


