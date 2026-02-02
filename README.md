# 🖐️ GestureGlide: Hand-Powered Media Control

Elevate your desktop experience with **GestureGlide**. Control your music, videos, and system volume using intuitive hand gestures through your webcam. No buttons, no touch—just pure motion.

---

## ✨ Features

*   **⚡ Instant Track Switching:** Swipe your fist left or right to skip songs.
*   **🤏 Precision Pinch Volume:** Adjust volume by pinching your thumb and index finger.
*   **👍 Quick Play/Pause:** A simple thumbs-up toggles your media.
*   **👤 Smart Face-Rejection:** Uses dual-model detection to ensure your face never accidentally triggers a command.
*   **📺 On-Screen HUD:** Real-time visual feedback and gesture status.

---

## 🎮 Gesture Map

| Gesture | Action | Description |
| :--- | :--- | :--- |
| **✊ Swipe Left** | `⏮️ Previous` | Swipe a closed fist to the left. |
| **✊ Swipe Right**| `⏭️ Next` | Swipe a closed fist to the right. |
| **🤏 Pinch** | `🔊 Volume` | Fold Middle, Ring, & Pinky. Move Thumb + Index to adjust. |
| **👍 Thumbs Up** | `⏯️ Play/Pause` | Hold a thumb up to toggle media. |

---

## 🚀 Quick Start

### 1. Requirements
Ensure you have Python 3.9+ installed and a working webcam.

### 2. Setup Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run
```bash
python hand_control.py
```

---

## 🛠️ Built With

*   [**OpenCV**](https://opencv.org/) - Computer Vision foundation.
*   [**MediaPipe**](https://mediapipe.dev/) - State-of-the-art hand tracking.
*   [**PyAutoGUI**](https://pyautogui.readthedocs.io/) - Seamless OS-level automation.

---

## ⚠️ Notes
*   **Camera Conflicts:** Windows only allows one app to use the camera at a time. Close Zoom/Teams if the program can't connect.
*   **Lighting:** Works best in well-lit environments where hand landmarks are clearly visible.

