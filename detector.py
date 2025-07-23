import numpy as np

def process_answer_sheet(pil_img):
    img = np.array(pil_img.convert("L"))  # grayscale
    # TODO: Replace with real detection logic using OpenCV
    student_id = "12345678"
    answers = {i + 1: ["A"] for i in range(120)}  # placeholder: all A
    return student_id, answers