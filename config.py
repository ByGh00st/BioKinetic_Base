# --- CONFIGURATION (HYDRA V5) ---
# SYSTEM
SYSTEM_NAME = "Bio-Kinetic Interface"
CODENAME = "MEDUSA_V5"

# VISION SENSOR
DROIDCAM_URL = "http://<YOUR_DROIDCAM_IP>:4747/video"
CAMERA_FPS = 60
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# THRESHOLDS & SENSITIVITY
CLICK_THRESHOLD = 30           # Pinch ile Tıklama mesafesi (Başlatma)
CLICK_RELEASE_THRESHOLD = 60   # Drag bırakma mesafesi (Hysteresis - Stabilite için)
ZOOM_THRESHOLD = 50            # Zoom
ZOOM_SENSITIVITY = 25          # Zoom hızı çarpanı
ZOOM_DEADZONE = 0.02           # Jitter önlemek için ölü bölge
SCROLL_SENSITIVITY = 30        # Scroll hızı per tick
BLINK_EAR_THRESHOLD = 0.12     # Göz kapalılık oranı (Çok düşük = Sadece tam kapandığında)

# --- HAND CONTROL SETTINGS ---
MOUSE_ROI_MARGIN = 150         # Kenar boşluğu (Bu değeri ARTIRIRSAN daha az el hareketi gerekir)
SCROLL_TRIGGER_TOP = 0.3       # Ekranın üst %30'una çıkınca yukarı kaydır
SCROLL_TRIGGER_BOTTOM = 0.7    # Ekranın alt %30'una inince aşağı kaydır


# TIMING (Debounce)
BLINK_DEBOUNCE = 0.4           # İki blink arası minimum süre
DOUBLE_CLICK_TIMEOUT = 0.6     # İkinci blink için maksimum bekleme süresi
BLINK_MIN_DURATION = 0.10      # Refleks kırpmaları yoksay (saniye)
WINK_CONFIDENCE_FRAMES = 3     # Kaç frame boyunca kapalı kalmalı? (False positive önleyici)

# MOTION FILTERING (One Euro Filter)
ONE_EURO_MIN_CUTOFF = 0.1
ONE_EURO_BETA = 0.1 

# HEAD MOUSE GAINS
HEAD_GAIN_X = 2.5
HEAD_GAIN_Y = 2.5
HEAD_DEADZONE = 0.005          # Kafa titremesini yoksaymak için ölü bölge

# HEAD MOTION FILTER (Daha tepkisel)
HEAD_MIN_CUTOFF = 0.4
HEAD_BETA = 0.7                # El'den daha hızlı tepki vermeli

# EYE GAZE CONTROL (Gözbebeği ile kontrol)
GAZE_SENSITIVITY_X = 15.0      # Yatay Çarpan (Extreme Boost)
GAZE_SENSITIVITY_Y = 20.0      # Dikey Çarpan (Extreme Boost)
