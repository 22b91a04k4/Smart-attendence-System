import cv2
import numpy as np
from keras.models import load_model
import serial
import openpyxl
from datetime import datetime
import os

# ============ MODEL LOAD ============
model = load_model("keras_Model.h5", compile=False)

# Labels
class_names = ["SP NAIDU", "SUBHASH", "SARFARAJ", "GIRL", "UNKNOW"]

# ============ STUDENT DATA ============
student_data = {
    "SP NAIDU": {"class": "10th", "roll": "1"},
    "SUBHASH":  {"class": "10th", "roll": "2"},
    "SARFARAJ": {"class": "10th", "roll": "3"},
    "GIRL":     {"class": "10th", "roll": "4"},
}

# ============ ARDUINO SETUP ============
try:
    arduino = serial.Serial('COM5', 9600, timeout=1)
    print("Arduino Connected on COM5!")
except:
    arduino = None
    print("Arduino not connected — LED/Buzzer skip")

# ============ EXCEL SETUP ============
excel_file = "attendance.xlsx"
if os.path.exists(excel_file):
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active
else:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Name", "Class", "Roll Number", "In Time"])
    wb.save(excel_file)

# ============ WEBCAM ============
cam = cv2.VideoCapture(0)
marked = []

print("System Started! Press 'q' to quit.")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Image preprocess
    img = cv2.resize(frame, (224, 224))
    img_array = np.array(img, dtype=np.float32)
    img_array = (img_array / 127.5) - 1.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array, verbose=0)
    index = np.argmax(prediction)
    confidence = prediction[0][index]
    name = class_names[index]

    # Display
    color = (0, 255, 0) if name != "UNKNOW" else (0, 0, 255)
    cv2.putText(frame, f"{name} ({confidence*100:.1f}%)", (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    if confidence > 0.80:

        if name == "UNKNOW":
            if arduino:
                arduino.write(b'U')
            cv2.putText(frame, "WARNING: UNKNOWN PERSON!", (20, 95),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        elif name not in marked:
            if arduino:
                arduino.write(b'K')
            marked.append(name)

            intime = datetime.now().strftime("%H:%M:%S")
            data = student_data.get(name, {"class": "N/A", "roll": "N/A"})
            ws.append([name, data["class"], data["roll"], intime])
            wb.save(excel_file)

            cv2.putText(frame, f"Welcome {name}! Attendance Marked!", (20, 95),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            print(f"Attendance marked: {name} at {intime}")

        else:
            cv2.putText(frame, f"{name} - Already Marked!", (20, 95),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
print("System Stopped.")