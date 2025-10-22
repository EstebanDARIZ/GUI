import os

BASE_DIR = r"C:\Users\edreau01\Doctorat"

VIDEO_NAME = "Lune"

VIDEO_DIR = os.path.join(BASE_DIR, "Dataset", "Raw")
VIDEO_PATH = os.path.join(VIDEO_DIR, f"{VIDEO_NAME}.MP4")

RESULTS_DIR = os.path.join(BASE_DIR, "Code", "DetectSon", "Results")
FILE_PATH = os.path.join(RESULTS_DIR, f"{VIDEO_NAME}_results.txt")