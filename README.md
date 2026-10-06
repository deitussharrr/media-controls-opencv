# GestureGlide

> **Status:** Prototype

GestureGlide is a local, webcam-based media controller. It uses hand landmarks to recognize a small set of gestures and maps them to desktop media controls and volume adjustments.

## What it does

- Swipe a closed fist left or right to move to the previous or next track.
- Pinch the thumb and index finger to adjust system volume.
- Hold a thumbs-up gesture to toggle play/pause.
- Display a live heads-up display with the detected gesture and control state.

## Technical approach

```text
Webcam frame
  → hand landmark detection (MediaPipe)
  → gesture rules and temporal checks
  → media / volume automation
  → on-screen feedback (OpenCV)
```

The prototype uses:

- [OpenCV](https://opencv.org/) for frame capture and display
- [MediaPipe](https://mediapipe.dev/) for hand tracking
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for OS-level input automation

## Quick start

**Requirements:** Python 3.9+ and a working webcam.

```bash
python -m venv venv
```

Activate the environment:

```bash
# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Install dependencies and start the controller:

```bash
pip install -r requirements.txt
python hand_control.py
```

## Gesture map

| Gesture | Action |
| --- | --- |
| Closed-fist swipe left | Previous track |
| Closed-fist swipe right | Next track |
| Thumb–index pinch | Volume control |
| Thumbs up | Play/pause |

## Limitations

- Gesture recognition is sensitive to lighting, camera placement, occlusion, and landmark-tracking quality.
- Media-key behavior depends on the operating system and its active media application.
- This repository is a prototype, not a benchmarked gesture-recognition system.
- Close other applications using the webcam before starting it.

## Possible next steps

- Measure latency and recognition reliability across lighting conditions and users.
- Add configurable gesture thresholds and a calibration flow.
- Separate recognition from OS automation to make the pipeline easier to test.

## Privacy

The application is intended to process webcam frames locally. Review the source and installed dependencies before use.

## License

No license has been selected yet. Please contact the repository owner before reusing the code.
