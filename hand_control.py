import os
# Suppress noisy logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import sys
import time
import math
from collections import deque

try:
    import cv2
    import mediapipe as mp
    import pyautogui
except ImportError as e:
    print("\n" + "="*60)
    print("CRITICAL ERROR: Library not found.")
    print(f"Missing: {e.name}")
    print("="*60)
    print("Please run: pip install -r requirements.txt")
    print("="*60 + "\n")
    sys.exit(1)

# Threshold for detecting a swipe (normalized distance)
SWIPE_THRESHOLD = 0.04
# Time to wait between swipes (seconds)
COOLDOWN_TIME = 0.3

def get_finger_status(lm):
    """Returns a list of booleans: [index, middle, ring, pinky] - True if folder/closed."""
    wrist = lm.landmark[0]
    tips_ids = [8, 12, 16, 20]
    pip_ids = [6, 10, 14, 18]
    
    status = []
    for tip_id, pip_id in zip(tips_ids, pip_ids):
        tip = lm.landmark[tip_id]
        pip = lm.landmark[pip_id]
        dist_tip = (tip.x - wrist.x)**2 + (tip.y - wrist.y)**2
        dist_pip = (pip.x - wrist.x)**2 + (pip.y - wrist.y)**2
        status.append(dist_tip < dist_pip)
    return status

def is_fist(lm):
    # All 4 fingers folded
    return all(get_finger_status(lm))

def is_thumb_up(lm):
    status = get_finger_status(lm)
    # 4 fingers folded + thumb above IP
    if not all(status):
        return False
    return lm.landmark[4].y < lm.landmark[3].y - 0.05

def run_program():
    print("="*60)
    print("   Hand Gesture Media Control (Camera Mode)")
    print("="*60)
    print("• Swipe LEFT/RIGHT  -> Track Prev/Next ⏮️ ⏭️")
    print("• Pinch Thumb+Index -> Volume Control 🔊")
    print("  (Fold Middle, Ring, Pinky to activate)")
    print("• Thumb UP          -> Play / Pause ⏯️")
    print("• Press 'q' to STOP")
    print("-" * 60)

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    mp_face = mp.solutions.face_detection
    face_detector = mp_face.FaceDetection(min_detection_confidence=0.5)

    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    history = deque(maxlen=10) 
    last_trigger_time = 0
    missed_fist_frames = 0
    
    # Pinch Volume State
    last_pinch_dist = None
    pinch_cooldown = 0
    
    cap = None

    try:
        while True:
            if cap is None or not cap.isOpened():
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    time.sleep(1)
                    continue
            
            success, image = cap.read()
            if not success:
                cap.release()
                cv2.destroyAllWindows()
                cap = None
                continue
            
            image = cv2.flip(image, 1)
            h, w, _ = image.shape
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_image)
            current_time = time.time()
            
            status_text = "Searching..."
            color = (0, 255, 255)
            
            if results.multi_hand_landmarks:
                face_results = face_detector.process(rgb_image)
                face_boxes = []
                if face_results.detections:
                    for detection in face_results.detections:
                        bboxC = detection.location_data.relative_bounding_box
                        face_boxes.append({
                            'xmin': bboxC.xmin - 0.05, 'ymin': bboxC.ymin - 0.05,
                            'xmax': bboxC.xmin + bboxC.width + 0.05, 'ymax': bboxC.ymin + bboxC.height + 0.05
                        })

                active_hand = None
                for hand_lm in results.multi_hand_landmarks:
                    wrist = hand_lm.landmark[0]
                    is_face = any(f['xmin'] < wrist.x < f['xmax'] and f['ymin'] < wrist.y < f['ymax'] for f in face_boxes)
                    if not is_face:
                        active_hand = hand_lm
                        mp_draw.draw_landmarks(image, active_hand, mp_hands.HAND_CONNECTIONS)
                        break

                if active_hand:
                    lm = active_hand
                    fingers = get_finger_status(lm) # [index, middle, ring, pinky]
                    fist_detected = all(fingers)
                    thumb_up_detected = is_thumb_up(lm)
                    
                    # Pinch Volume detection: Middle, Ring, Pinky folded, Index might be open
                    pinch_mode = fingers[1] and fingers[2] and fingers[3]
                    
                    if pinch_mode and not thumb_up_detected:
                        # Calculate distance between thumb tip (4) and index tip (8)
                        t = lm.landmark[4]; i = lm.landmark[8]
                        dist = math.sqrt((t.x - i.x)**2 + (t.y - i.y)**2)
                        
                        # Draw pinch line
                        x1, y1 = int(t.x * w), int(t.y * h)
                        x2, y2 = int(i.x * w), int(i.y * h)
                        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 2)
                        cv2.circle(image, (x1, y1), 5, (255, 0, 255), -1)
                        cv2.circle(image, (x2, y2), 5, (255, 0, 255), -1)

                        status_text = "🤏 PINCH VOLUME"
                        color = (255, 0, 255)

                        if last_pinch_dist is not None:
                            diff = dist - last_pinch_dist
                            if abs(diff) > 0.01: # Sensitivity threshold
                                if diff > 0:
                                    pyautogui.press('volumeup')
                                    print("🔊 Volume UP")
                                else:
                                    pyautogui.press('volumedown')
                                    print("🔉 Volume DOWN")
                                last_pinch_dist = dist # Update base
                        else:
                            last_pinch_dist = dist
                    else:
                        last_pinch_dist = None

                    # Media Toggle / Play Pause
                    if thumb_up_detected:
                        status_text = "👍 PLAY / PAUSE"
                        color = (255, 255, 0)
                        if current_time - last_trigger_time > 1.2:
                             pyautogui.press('playpause')
                             last_trigger_time = current_time
                             cv2.putText(image, "PLAY/PAUSE", (w//2-100, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)

                    # Swipe Detection (Fist Only)
                    elif fist_detected:
                        status_text = "✊ FIST (SWIPE)"
                        color = (0, 255, 0)
                        x0 = lm.landmark[0].x; y0 = lm.landmark[0].y
                        x9 = lm.landmark[9].x; y9 = lm.landmark[9].y
                        history.append({'x': (x0+x9)/2, 'y': (y0+y9)/2, 't': current_time})
                        
                        if len(history) >= 3 and (current_time - last_trigger_time > COOLDOWN_TIME):
                            start = history[0]; end = history[-1]
                            dx = end['x'] - start['x']; dy = end['y'] - start['y']
                            if abs(dx) > SWIPE_THRESHOLD and abs(dx) > abs(dy):
                                if dx < 0:
                                    pyautogui.press('prevtrack')
                                    cv2.putText(image, "<< PREV", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
                                else:
                                    pyautogui.press('nexttrack')
                                    cv2.putText(image, "NEXT >>", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
                                last_trigger_time = current_time
                                history.clear()
                    else:
                        if len(history) > 0: history.clear()

            # Draw Status UI
            cv2.rectangle(image, (0, 0), (250, 70), (0, 0, 0), -1)
            cv2.putText(image, status_text, (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            cv2.imshow("Hand Control - Media Center", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    except KeyboardInterrupt:
        pass
    finally:
        if cap: cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_program()


