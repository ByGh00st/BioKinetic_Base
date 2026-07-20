import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import screeninfo
import math
import time

# MODULES
import config
from filters import OneEuroFilter

# SETTINGS
pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False


class BioKineticInterface:
    def __init__(self):
        print(f"[{config.CODENAME}] Initializing Systems...")

        # Screen
        try:
            self.screen = screeninfo.get_monitors()[0]
            self.w_scr, self.h_scr = self.screen.width, self.screen.height
        except Exception:
            self.w_scr, self.h_scr = 1920, 1080

        # Mediapipe
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=0
        )

        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        # STATE
        self.drag_active = False
        self.blink_counter = 0
        self.blink_start_time = 0
        self.head_start_pose = None
        self.gaze_start_pose = None

        self.left_wink_counter = 0
        self.right_wink_counter = 0  # FIX: previously undefined -> AttributeError risk
        self.scroll_mode = False
        self.head_mouse_mode = False
        self.last_blink_time = 0

        # PERFORMANCE: frame skip counters
        self._frame_count = 0
        self.hand_process_every_n = 2   # el takibini her 2 frame'de bir işle
        self.eye_process_every_n = 1    # göz/kafa her frame işlensin (hassas timing gerekiyor)

        # EYE LANDMARK INDEX SETS (tek yerde tanımlı, tekrar yok)
        self.left_eye_idxs = [33, 133, 160, 159, 158, 144, 145, 153]
        self.right_eye_idxs = [362, 263, 387, 386, 385, 373, 374, 380]

        # FILTERS (Hand - Smooth/Stable)
        self.filter_x = OneEuroFilter(time.time(), 0, min_cutoff=config.ONE_EURO_MIN_CUTOFF, beta=config.ONE_EURO_BETA)
        self.filter_y = OneEuroFilter(time.time(), 0, min_cutoff=config.ONE_EURO_MIN_CUTOFF, beta=config.ONE_EURO_BETA)

        # FILTERS (Head - Responsive/Fast)
        self.filter_head_x = OneEuroFilter(time.time(), 0, min_cutoff=config.HEAD_MIN_CUTOFF, beta=config.HEAD_BETA)
        self.filter_head_y = OneEuroFilter(time.time(), 0, min_cutoff=config.HEAD_MIN_CUTOFF, beta=config.HEAD_BETA)

        # CAMERA
        self.camera_index = 0
        self.use_ip_cam = False
        self.cap = cv2.VideoCapture(0)
        self.configure_camera()

        # cached results (frame-skip icin)
        self._last_hand_results = None

        print(f"[{config.CODENAME}] READY.")
        print("CONTROLS: [ESC] Quit | [TAB] Switch Cam | [S] Scroll | [H] Head Mouse")

    def configure_camera(self):
        self.cap.set(cv2.CAP_PROP_FPS, config.CAMERA_FPS)
        self.cap.set(3, config.CAMERA_WIDTH)
        self.cap.set(4, config.CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def switch_camera(self):
        self.cap.release()
        if not self.use_ip_cam:
            print(f"Connecting to DroidCam: {config.DROIDCAM_URL}")
            self.cap = cv2.VideoCapture(config.DROIDCAM_URL)
            self.use_ip_cam = True
        else:
            print("Switching to Local Camera (Index 0)")
            self.cap = cv2.VideoCapture(0)
            self.use_ip_cam = False
        self.configure_camera()

    def run(self):
        while True:
            t_current = time.time()
            success, img = self.cap.read()
            if not success:
                blank = np.zeros((480, 640, 3), np.uint8)
                cv2.putText(blank, "NO SIGNAL - PRESS TAB", (100, 240), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                cv2.imshow(config.SYSTEM_NAME, blank)
                self.handle_input(cv2.waitKey(1) & 0xFF)
                continue

            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            img = cv2.flip(img, 1)
            H, W, _ = img.shape
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            self._frame_count += 1

            # PROCESS (frame-skip uygulanmış)
            if self._frame_count % self.hand_process_every_n == 0:
                self.process_hands(img, img_rgb, H, W, t_current)

            if self._frame_count % self.eye_process_every_n == 0:
                self.process_eyes(img, img_rgb, H, W, t_current)

            # UI
            cv2.putText(img, f"CAM: {'IP' if self.use_ip_cam else 'USB'}", (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
            if self.head_mouse_mode:
                cv2.putText(img, "HEAD MOUSE", (10, 60), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
            if self.scroll_mode:
                cv2.putText(img, "SCROLL", (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

            cv2.imshow(config.SYSTEM_NAME, img)
            if self.handle_input(cv2.waitKey(1) & 0xFF):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def handle_input(self, key):
        if key == 27:
            return True  # ESC
        if key == 9:
            self.switch_camera()  # TAB
        if key == ord('s'):
            self.scroll_mode = not self.scroll_mode
            self.head_mouse_mode = False
            print(f"Scroll Mode: {self.scroll_mode}")
        if key == ord('h'):
            self.head_mouse_mode = not self.head_mouse_mode
            self.scroll_mode = False
            self.head_start_pose = None
            self.gaze_start_pose = None
            print(f"Head Mouse: {self.head_mouse_mode}")
        return False

    def process_hands(self, img, img_rgb, H, W, t):
        if self.head_mouse_mode:
            return

        results = self.hands.process(img_rgb)
        self._last_hand_results = results
        if not results.multi_hand_landmarks:
            return

        for landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label  # "Left" or "Right"

            # --- CURSOR HAND ---
            if label == "Right":
                self.mp_draw.draw_landmarks(img, landmarks, self.mp_hands.HAND_CONNECTIONS)

                idx = landmarks.landmark[8]
                ix, iy = idx.x * W, idx.y * H

                margin = config.MOUSE_ROI_MARGIN
                screen_x = np.interp(ix, (margin, W - margin), (0, self.w_scr))
                screen_y = np.interp(iy, (margin, H - margin), (0, self.h_scr))

                px = self.filter_x(t, screen_x)
                py = self.filter_y(t, screen_y)

                if not self.scroll_mode:
                    pyautogui.moveTo(px, py)

                cv2.circle(img, (int(ix), int(iy)), 10, (255, 0, 0), 2)
                cv2.putText(img, "CURSOR (R)", (int(ix) + 15, int(iy)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

            # --- ACTION HAND (click / drag / scroll) ---
            elif label == "Left":
                self.mp_draw.draw_landmarks(img, landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Scroll via palm position
                wrist = landmarks.landmark[0]
                palm_y = wrist.y

                if palm_y < config.SCROLL_TRIGGER_TOP:
                    pyautogui.scroll(config.SCROLL_SENSITIVITY)
                    cv2.putText(img, "SCROLL UP", (50, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
                elif palm_y > config.SCROLL_TRIGGER_BOTTOM:
                    pyautogui.scroll(-config.SCROLL_SENSITIVITY)
                    cv2.putText(img, "SCROLL DOWN", (50, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

                # Click/drag via pinch (Index 8 - Thumb 4)
                idx_tip = landmarks.landmark[8]
                thumb_tip = landmarks.landmark[4]

                x1, y1 = int(idx_tip.x * W), int(idx_tip.y * H)
                x2, y2 = int(thumb_tip.x * W), int(thumb_tip.y * H)

                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                dist = math.hypot(x1 - x2, y1 - y2)

                color = (0, 0, 255) if self.drag_active else (0, 255, 0)
                cv2.line(img, (x1, y1), (x2, y2), color, 2)
                cv2.circle(img, (cx, cy), 5, color, -1)

                if not self.drag_active:
                    if dist < config.CLICK_THRESHOLD:
                        pyautogui.mouseDown()
                        self.drag_active = True
                        print("ACTION: DOWN (Action Hand)")
                else:
                    if dist > config.CLICK_RELEASE_THRESHOLD:
                        pyautogui.mouseUp()
                        self.drag_active = False
                        print("ACTION: UP (Action Hand)")

    def process_eyes(self, img, img_rgb, H, W, t):
        try:
            results = self.face_mesh.process(img_rgb)
            if not results.multi_face_landmarks:
                return

            lm = results.multi_face_landmarks[0].landmark

            # --- TEK SEFERLİK EAR HESABI (tekrar hesaplama kaldırıldı) ---
            ear_left = self.get_eye_ratio(lm, self.left_eye_idxs)
            ear_right = self.get_eye_ratio(lm, self.right_eye_idxs)

            # --- BLINK (both eyes) DETECTION -> single/double click ---
            if ear_left < config.BLINK_EAR_THRESHOLD and ear_right < config.BLINK_EAR_THRESHOLD:
                if time.time() - self.last_blink_time > config.BLINK_DEBOUNCE:
                    if self.blink_start_time == 0:
                        self.blink_start_time = time.time()
                    elif time.time() - self.blink_start_time > config.BLINK_MIN_DURATION:
                        self.blink_counter += 1
                        self.last_blink_time = time.time()
                        self.blink_start_time = 0
            else:
                self.blink_start_time = 0

            if self.blink_counter > 0 and time.time() - self.last_blink_time > 0.6:
                if self.blink_counter == 1:
                    print("ACTION: CLICK")
                    pyautogui.click()
                elif self.blink_counter >= 2:
                    print("ACTION: DOUBLE CLICK")
                    pyautogui.doubleClick()
                self.blink_counter = 0

            # --- SMART WINK LOGIC (tek eye state, tekrar hesaplama yok) ---
            left_closed = ear_left < config.BLINK_EAR_THRESHOLD
            right_closed = ear_right < config.BLINK_EAR_THRESHOLD

            if left_closed and not right_closed:
                self.left_wink_counter += 1
                self.right_wink_counter = 0
            elif right_closed and not left_closed:
                self.right_wink_counter += 1
                self.left_wink_counter = 0
            else:
                self.left_wink_counter = 0
                self.right_wink_counter = 0

            if self.left_wink_counter == config.WINK_CONFIDENCE_FRAMES:
                print("ACTION: LEFT WINK -> CLICK")
                pyautogui.click()

            if self.right_wink_counter == config.WINK_CONFIDENCE_FRAMES:
                print("ACTION: RIGHT WINK -> RIGHT CLICK")
                pyautogui.rightClick()

            # --- HEAD MOUSE & GAZE ---
            if self.head_mouse_mode:
                nose = lm[4]

                gaze_dx_l, gaze_dy_l = self.get_gaze_vector(lm, 33, 133, 159, 145, 468)
                gaze_dx_r, gaze_dy_r = self.get_gaze_vector(lm, 362, 263, 386, 374, 473)

                current_gaze_x = (gaze_dx_l + gaze_dx_r) / 2
                current_gaze_y = (gaze_dy_l + gaze_dy_r) / 2

                eye_cx = int((lm[33].x + lm[133].x + lm[362].x + lm[263].x) / 4 * W)
                eye_cy = int((lm[159].y + lm[145].y + lm[386].y + lm[374].y) / 4 * H)

                vis_scale = 100
                end_x = int(eye_cx + (current_gaze_x * vis_scale))
                end_y = int(eye_cy + (current_gaze_y * vis_scale))
                cv2.arrowedLine(img, (eye_cx, eye_cy), (end_x, end_y), (255, 0, 255), 2)

                if self.head_start_pose is None:
                    self.head_start_pose = (nose.x, nose.y)
                    self.gaze_start_pose = (current_gaze_x, current_gaze_y)
                    print("[CALIBRATION] Head & Gaze Zeroed.")

                head_dx = nose.x - self.head_start_pose[0]
                head_dy = nose.y - self.head_start_pose[1]

                if abs(head_dx) < config.HEAD_DEADZONE:
                    head_dx = 0
                if abs(head_dy) < config.HEAD_DEADZONE:
                    head_dy = 0

                if self.gaze_start_pose:
                    gaze_dx = current_gaze_x - self.gaze_start_pose[0]
                    gaze_dy = current_gaze_y - self.gaze_start_pose[1]
                else:
                    gaze_dx, gaze_dy = 0, 0

                cv2.putText(img, f"HEAD: X={head_dx:.3f} Y={head_dy:.3f}", (10, H - 60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
                cv2.putText(img, f"GAZE: X={gaze_dx:.3f} Y={gaze_dy:.3f}", (10, H - 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
                cv2.putText(img, f"SENS: X={config.GAZE_SENSITIVITY_X} Y={config.GAZE_SENSITIVITY_Y}", (10, H - 20), cv2.FONT_HERSHEY_PLAIN, 1, (200, 200, 200), 1)

                ear_color = (0, 0, 255) if (left_closed or right_closed) else (0, 255, 0)
                cv2.putText(img, f"EAR: L={ear_left:.2f} R={ear_right:.2f}", (10, H - 80), cv2.FONT_HERSHEY_PLAIN, 1, ear_color, 1)

                total_dx = (head_dx * config.HEAD_GAIN_X) + (gaze_dx * config.GAZE_SENSITIVITY_X)
                total_dy = (head_dy * config.HEAD_GAIN_Y) + (gaze_dy * config.GAZE_SENSITIVITY_Y)

                target_x = (self.w_scr / 2) + (total_dx * self.w_scr)
                target_y = (self.h_scr / 2) + (total_dy * self.h_scr)

                target_x = max(0, min(self.w_scr, target_x))
                target_y = max(0, min(self.h_scr, target_y))

                px = self.filter_head_x(t, target_x)
                py = self.filter_head_y(t, target_y)

                if self.blink_counter == 0:
                    pyautogui.moveTo(px, py)

            # --- VISUALIZATION (eye contours) ---
            for eye_idxs in [self.left_eye_idxs, self.right_eye_idxs]:
                mesh_points = np.array([np.multiply([lm[i].x, lm[i].y], [W, H]).astype(int) for i in eye_idxs])
                cv2.polylines(img, [mesh_points], True, (0, 255, 255), 1, cv2.LINE_AA)

            # --- SCROLL (head-based, scroll_mode) ---
            if self.scroll_mode:
                nose_y = lm[1].y * H
                cy = H / 2
                if nose_y < cy - 40:
                    pyautogui.scroll(config.SCROLL_SENSITIVITY)
                elif nose_y > cy + 40:
                    pyautogui.scroll(-config.SCROLL_SENSITIVITY)

        except (IndexError, AttributeError, ZeroDivisionError) as e:
            print(f"[process_eyes] Landmark/calc error: {e}")

    def get_gaze_vector(self, lm, inner_idx, outer_idx, top_idx, bottom_idx, iris_idx):
        p_in = lm[inner_idx]
        p_out = lm[outer_idx]
        p_top = lm[top_idx]
        p_bot = lm[bottom_idx]
        p_iris = lm[iris_idx]

        eye_width = math.hypot(p_out.x - p_in.x, p_out.y - p_in.y)
        eye_height = math.hypot(p_top.x - p_bot.x, p_top.y - p_bot.y)

        if eye_width == 0 or eye_height == 0:
            return 0, 0

        cx = (p_in.x + p_out.x) / 2
        cy = (p_top.y + p_bot.y) / 2

        raw_dx = p_iris.x - cx
        raw_dy = p_iris.y - cy

        norm_dx = raw_dx / (eye_width / 2)
        norm_dy = raw_dy / (eye_height / 2)

        return norm_dx, norm_dy

    def get_eye_ratio(self, lm, idxs):
        # idxs: [33,133,160,159,158,144,145,153] gibi 8 noktalı sırayla
        v1 = math.hypot(lm[idxs[3]].x - lm[idxs[6]].x, lm[idxs[3]].y - lm[idxs[6]].y)
        h = math.hypot(lm[idxs[0]].x - lm[idxs[1]].x, lm[idxs[0]].y - lm[idxs[1]].y)
        return v1 / h if h > 0 else 0


if __name__ == "__main__":
    app = BioKineticInterface()
    app.run()