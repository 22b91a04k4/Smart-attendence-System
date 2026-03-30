# Smart Attendance System

A modern, automated attendance system using **facial recognition** powered by deep learning. This system automatically marks attendance when it recognizes a student's face using a trained Keras neural network model.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Prerequisites & Installation](#prerequisites--installation)
5. [Project Structure](#project-structure)
6. [Configuration Guide](#configuration-guide)
7. [How It Works](#how-it-works)
8. [Usage Instructions](#usage-instructions)
9. [File Descriptions](#file-descriptions)
10. [Hardware Requirements](#hardware-requirements)
11. [Troubleshooting](#troubleshooting)
12. [Future Enhancements](#future-enhancements)

---

## 📌 Project Overview

The **Smart Attendance System** is an intelligent solution that:

- **Captures video** from a webcam in real-time
- **Recognizes student faces** using a pre-trained Keras deep learning model
- **Automatically logs attendance** in an Excel spreadsheet with timestamps
- **Alerts via Arduino** when a student is recognized or an unknown person is detected
- **Prevents duplicate entries** by tracking already marked students
- **Displays live feedback** on the video feed showing confidence levels

This eliminates the need for manual attendance marking and provides a secure, automated solution for educational institutions.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Real-time Facial Recognition** | Detects and recognizes faces in live video feed |
| **Deep Learning Model** | Uses a pre-trained Keras neural network for high accuracy |
| **Automatic Logging** | Records attendance instantly in Excel with timestamp |
| **Arduino Integration** | Sends signals to control LEDs/Buzzer for audio-visual feedback |
| **Confidence Display** | Shows recognition confidence percentage on video |
| **Duplicate Prevention** | Prevents marking the same student multiple times |
| **Unknown Person Alert** | Alerts when an unrecognized person is detected |
| **Data Persistence** | All attendance records saved in an Excel file |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SMART ATTENDANCE SYSTEM                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐        ┌──────────────┐    ┌────────────┐ │
│  │   Webcam  ──┼────────→│  OpenCV    ──┼───→│  Keras ML  │ │
│  │   Input     │        │  (Image     │    │   Model    │ │
│  └──────────────┘        │   Processing)  └────────────┘ │
│                          │                │        │       │
│                          └────────────────┘        │       │
│                                                     ↓       │
│                          ┌──────────────────┐      │       │
│                          │  Recognition    ←──────┘       │
│                          │  (Match Student)                │
│                          └────────┬─────────┘              │
│                                   │                        │
│              ┌────────────────────┼────────────────────┐  │
│              ↓                    ↓                    ↓  │
│         ┌──────────┐         ┌──────────┐      ┌──────────┐ │
│         │  Excel   │         │  Arduino │      │ Display  │ │
│         │ Logging  │         │  Alerts  │      │ (Video)  │ │
│         └──────────┘         └──────────┘      └──────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Prerequisites & Installation

### System Requirements
- **Python 3.7+** (Recommended: Python 3.8 or 3.9)
- **Windows 10/11** (or compatible OS with USB ports)
- **Webcam** (integrated or USB)
- **Arduino Board** (Optional, for LED/Buzzer feedback)
- **COM Port** (for Arduino communication)

### Step 1: Install Python Dependencies

Open a terminal/command prompt and run:

```bash
pip install opencv-python tensorflow keras numpy openpyxl pyserial
```

**Package Details:**
- `opencv-python` - Computer vision library for webcam capture & image processing
- `tensorflow` - Deep learning framework (required by Keras)
- `keras` - Neural network model library
- `numpy` - Numerical computing library
- `openpyxl` - Excel file manipulation
- `pyserial` - Serial communication with Arduino

### Step 2: Download/Prepare Files

Ensure you have these files in your project directory:
- `keras_Model.h5` - Pre-trained facial recognition model
- `labels.txt` - List of student names (labels)
- `main.py` - Main application script
- `attendance.xlsx` - Auto-created upon first run

---

## 📁 Project Structure

```
Smart-Attendance-System/
│
├── main.py                    # Main application script
├── keras_Model.h5             # Pre-trained deep learning model
├── labels.txt                 # Student labels/names
├── attendance.xlsx            # Attendance log (auto-generated)
└── README.md                  # This file
```

---

## ⚙️ Configuration Guide

### 1. **Update Student Data**

In `main.py`, modify the student dictionary with your actual data:

```python
student_data = {
    "SP NAIDU": {"class": "10th", "roll": "1"},
    "SUBHASH":  {"class": "10th", "roll": "2"},
    "SARFARAJ": {"class": "10th", "roll": "3"},
    "GIRL":     {"class": "10th", "roll": "4"},
}
```

**How to use:**
- Student names must **exactly match** the labels in your model
- Add all students who will be recognized by the system
- Include their class and roll numbers

### 2. **Update Model Class Names**

```python
class_names = ["SP NAIDU", "SUBHASH", "SARFARAJ", "GIRL", "UNKNOW"]
```

- These must match the training labels from your dataset
- **"UNKNOW"** should always be the last label (for unrecognized persons)

### 3. **Configure Arduino Connection**

```python
try:
    arduino = serial.Serial('COM5', 9600, timeout=1)
except:
    arduino = None  # Optional - system works without Arduino
```

**Steps:**
1. Find your Arduino COM port:
   - Windows: Device Manager → Ports (COM & LPT) → Arduino COM port
2. Replace `'COM5'` with your actual port (e.g., `'COM3'`, `'COM4'`)
3. Ensure baud rate matches Arduino configuration (default: 9600)

### 4. **Webcam Selection**

```python
cam = cv2.VideoCapture(0)  # 0 = default webcam
```

- Change `0` if using a different camera (e.g., `1`, `2` for multiple cameras)

---

## 🔬 How It Works

### Step-by-Step Process

1. **Capture Frame**
   - Webcam captures a live video frame in real-time
   - Resolution: 1280x720 or system default

2. **Image Preprocessing**
   ```python
   img = cv2.resize(frame, (224, 224))  # Resize to model input size
   img_array = (img_array / 127.5) - 1.0  # Normalize pixel values
   ```
   - Resizes to 224×224 (required by Keras model)
   - Normalizes pixel values to range [-1, 1]

3. **Face Recognition (Prediction)**
   - Pre-trained Keras model analyzes the image
   - Outputs probability scores for each student label
   - Example: `[0.02, 0.15, 0.78, 0.04, 0.01]`

4. **Confidence Check**
   ```python
   if confidence > 0.80:  # 80% confidence threshold
   ```
   - Only marks attendance if confidence exceeds 80%
   - Prevents false positives

5. **Attendance Logging**
   - If recognized and not previously marked:
     - Record name, class, roll number, and timestamp
     - Save to `attendance.xlsx`
     - Send signal to Arduino for audio-visual alert

6. **Duplicate Prevention**
   ```python
   if name not in marked:  # Only mark once per session
   ```
   - Tracks already marked students
   - Prevents duplicate entries

7. **Display Feedback**
   - Shows live video with:
     - Student name
     - Confidence percentage
     - Status message (Marked/Already Marked/Unknown)
     - Color-coded display (Green: recognized, Red: unknown)

---

## 🚀 Usage Instructions

### Running the System

1. **Prepare the Environment:**
   - Connect your webcam
   - Connect Arduino (optional)
   - Ensure `keras_Model.h5` is in the directory

2. **Start the Application:**
   ```bash
   python main.py
   ```

3. **System Output:**
   ```
   Arduino Connected on COM5!
   System Started! Press 'q' to quit.
   Attendance marked: SP NAIDU at 09:45:30
   Attendance marked: SUBHASH at 09:45:45
   ```

4. **Live Video Display:**
   - A window shows real-time video feed
   - Shows recognized student and confidence percentage
   - Color-coded alerts (green for recognized, red for unknown)

5. **Stop the System:**
   - Press **'q'** on the keyboard
   - System closes gracefully and saves all data

---

## 📄 File Descriptions

### `main.py` - Main Application Script

**Sections:**

| Section | Purpose |
|---------|---------|
| **MODEL LOAD** | Loads the pre-trained Keras model from `keras_Model.h5` |
| **STUDENT DATA** | Dictionary storing student information (class, roll number) |
| **ARDUINO SETUP** | Establishes serial connection for hardware alerts |
| **EXCEL SETUP** | Creates/opens attendance log file |
| **WEBCAM** | Initializes webcam for live video capture |
| **Main Loop** | Continuously processes frames and marks attendance |

### `keras_Model.h5` - Neural Network Model

- Pre-trained deep learning model (Keras/TensorFlow format)
- Trained on facial images of students
- Input: 224×224 pixel RGB image
- Output: Probability scores for each student + "UNKNOWN"
- **Size:** ~100+ MB (depending on model architecture)

**Model Architecture Typically Used:**
- MobileNet, ResNet, or custom CNN
- Trained with dataset containing student photos
- Categories: One per student + one for "Unknown" persons

### `labels.txt` - Model Labels

Contains the names of all recognized students:
```
SP NAIDU
SUBHASH
SARFARAJ
GIRL
UNKNOW
```

**Must match exactly with:**
- `class_names` in `main.py`
- Training labels from the Keras model

### `attendance.xlsx` - Attendance Log

Auto-generated Excel file with columns:

| Column | Description | Example |
|--------|-------------|---------|
| Name | Student name | SP NAIDU |
| Class | Student class | 10th |
| Roll Number | Student roll | 1 |
| In Time | Check-in timestamp | 09:45:30 |

**Features:**
- Auto-creates on first run
- Appends new records each time
- Timestamps in HH:MM:SS format
- Can be opened in Excel/Google Sheets

---

## 🛠️ Hardware Requirements

### Essential Components
| Item | Purpose | Notes |
|------|---------|-------|
| **Webcam** | Capture student faces | USB or integrated webcam |
| **Computer** | Run the application | Windows 10+ recommended |
| **Monitor/Display** | View live feed | Any resolution works |

### Optional Components (Arduino Integration)
| Item | Purpose | Specifications |
|------|---------|-----------------|
| **Arduino Board** | Send control signals | Arduino Uno/Nano recommended |
| **LED** | Visual feedback | Green for recognized, Red for unknown |
| **Buzzer** | Audio feedback | 5V active buzzer |
| **Relay Module** | Control high-power devices | 2-channel relay optional |
| **USB Cable** | Arduino connection | Standard USB-A to USB-B |

### Arduino Connection Diagram

```
Arduino → COM Port
  IO Pin 1 → Buzzer (buzzer signal 'K' for known)
  IO Pin 2 → LED Green (signal for recognized student)
  IO Pin 3 → LED Red (signal 'U' for unknown person)
  GND → Ground
  5V → Power
```

---

## 🐛 Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'keras'"
**Solution:**
```bash
pip install keras tensorflow
```

### Issue 2: "FileNotFoundError: keras_Model.h5 not found"
**Solution:**
- Ensure `keras_Model.h5` is in the same directory as `main.py`
- Check file name spelling (case-sensitive)

### Issue 3: Webcam not opening
**Solution:**
```python
# Test webcam first
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"
```
- Try changing `0` to `1` or `2` in `cv2.VideoCapture(0)`
- Check if another app is using the webcam

### Issue 4: "Arduino not connected" message
**Solution:**
- Verify USB cable connection
- Check COM port in Device Manager
- Update the correct COM port in `main.py`
- System still works without Arduino (LED/Buzzer alerts skipped)

### Issue 5: Low recognition accuracy
**Solution:**
- Ensure good lighting conditions
- Position face directly toward camera
- Train the model with better quality images
- Increase confidence threshold carefully (currently 0.80)

### Issue 6: Recognition not working at all
**Solution:**
- Verify model was trained with same preprocessing
- Check if class names in code match model training labels
- Ensure image normalization matches: `(img / 127.5) - 1.0`

### Issue 7: Excel file errors
**Solution:**
```bash
pip install --upgrade openpyxl
```
- Close `attendance.xlsx` if it's open in Excel
- Ensure write permissions to the directory

---

## 🔮 Future Enhancements

### Potential Improvements

1. **Enhanced Features**
   - [ ] Multi-face recognition (detect multiple students simultaneously)
   - [ ] Attendance reports (daily, weekly, monthly summaries)
   - [ ] Web-based dashboard for viewing attendance
   - [ ] Mobile app integration for notifications
   - [ ] QR code backup authentication

2. **Technical Upgrades**
   - [ ] Switch to YOLOv8 for faster detection
   - [ ] Add face liveness detection (prevent spoofing/photos)
   - [ ] Database integration (MySQL/PostgreSQL instead of Excel)
   - [ ] Cloud storage for backup
   - [ ] Multi-camera support for large classrooms

3. **Security Features**
   - [ ] Encryption of attendance data
   - [ ] User authentication/login system
   - [ ] Audit logs for all changes
   - [ ] Photo capture of each attendance record

4. **User Experience**
   - [ ] GUI interface (Tkinter/PyQt)
   - [ ] Configuration file instead of hardcoding values
   - [ ] Email notifications to parents
   - [ ] Absence alerts
   - [ ] Manual override capability

---

## 📝 License & Credits

This project is a smart attendance solution developed for educational institutions.

**Created for:** Automation of attendance marking using facial recognition

---

## ❓ FAQs

**Q: Can I use this for other purposes?**
A: Yes, the system can recognize any set of faces. Just retrain the model with your dataset.

**Q: How accurate is the system?**
A: Typically 95%+ with good lighting. Accuracy depends on training data quality.

**Q: Can I integrate with my school's database?**
A: Yes, you can modify the code to send data to a database instead of Excel.

**Q: Is the system suitable for large classrooms?**
A: Yes, but you may want to optimize for multiple faces or use higher-performance hardware.

**Q: Can I use a different face recognition model?**
A: Yes, any Keras model taking 224×224 input will work (may need preprocessing adjustments).

---

## 📧 Support & Contact

For issues, questions, or suggestions, please refer to the project documentation or contact the development team.

---

**Last Updated:** March 31, 2026

**Version:** 1.0.0
