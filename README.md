# BioKinetic_Base

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python" />
  <img src="https://img.shields.io/badge/OpenCV-Enabled-green" alt="OpenCV" />
  <img src="https://img.shields.io/badge/MediaPipe-Hands%20%2B%20Face-red" alt="MediaPipe" />
  <img src="https://img.shields.io/badge/Status-Experimental-orange" alt="Status" />
</div>

<p align="center">
  <strong>Temassız bilgisayar kontrolü için deneysel bir Python projesi.</strong>
</p>

BioKinetic_Base, kameradan alınan görüntüler üzerinden el, göz ve kafa hareketlerini algılayarak bilgisayarda fare, tıklama, sürükleme ve kaydırma gibi etkileşimleri gerçekleştiren deneysel bir kontrol sistemi projesidir. MediaPipe ve OpenCV tabanlı bu yapı, gerçek zamanlı insan-bilgisayar etkileşimi sunar. Özellikle erişilebilirlik, demo projeleri ve araştırma ortamlarında kullanılmak üzere tasarlanmıştır.

---

## ✨ Ana Özellikler

- Gerçek zamanlı el takibi
- Sağ el ile fare konumlandırma
- Sol el ile tıklama, sürükleme ve kaydırma işlevleri
- Parmaklar arası mesafeye dayalı pinch algılama
- Göz kapatma tespiti ile tek/çift tıklama
- Sol/sağ göz wink algısı ile farklı tıklama davranışları
- Kafa hareketine dayalı head mouse modu
- Göz bebeği hareketiyle yönlendirme
- DroidCam ve yerel webcam desteği
- Titreşim azaltma amaçlı One Euro Filter entegrasyonu

---

## 🧠 Proje Hakkında

Bu proje, kullanıcıların dokunmadan veya fiziksel cihaz kullanmadan bilgisayar ile etkileşime girmesine olanak tanır. Kamera görüntüsü üzerinden:

- el pozisyonu ile fare hareketi,
- el pinch hareketi ile tıklama/drag,
- göz kırpma davranışı ile tek/çift tıklama,
- kafa hareketiyle baş fare modu,
- göz bebeği yönelimine dayalı gaze kontrolü

sağlanır.

Bu sistem, özellikle aşağıdaki kullanım senaryolarında ilgi çekicidir:

- erişilebilirlik destekli bilgisayar kullanımı,
- temassız kontrol deneyimi,
- oyun veya demo uygulamaları,
- bilgisayar etkileşimi alanında araştırma ve prototip geliştirme.

---

## 🛠️ Kullanılan Teknolojiler

- Python 3.8+
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy
- ScreenInfo

---

## 🚀 Kurulum Rehberi

### 1) Depoyu Klonlayın

```bash
git clone https://github.com/ByGh00st/BioKinetic_Base.git
cd BioKinetic_Base
```

### 2) Sanal Ortam Oluşturun

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3) Bağımlılıkları Yükleyin

```bash
pip install opencv-python mediapipe pyautogui numpy screeninfo
```

### 4) Yapılandırmayı Ayarlayın

[config.py](config.py) dosyasını açın ve aşağıdaki alanları ihtiyaçlarınıza göre düzenleyin:

- kamera çözünürlüğü
- FPS değeri
- tıklama ve sürükleme eşiği
- scroll hızı
- blink ve wink algılama seviyesi
- head mouse hassasiyeti
- One Euro Filter parametreleri

DroidCam kullanacaksanız, [config.py](config.py) içindeki `DROIDCAM_URL` değerini kendi cihazınızın IP adresiyle güncelleyin.

---

## ▶️ Çalıştırma

```bash
python main.py
```

Program başlatıldığında kamera akışı açılır ve gerçek zamanlı algılama başlar. Çıkış için ESC tuşuna basın.

---

## 🎮 Kontroller

### Genel Kontroller

- ESC: Uygulamadan çıkış
- TAB: Kamera değiştir (yerel kamera / DroidCam)
- S: Scroll modu aç/kapat
- H: Head Mouse modu aç/kapat

### El Kontrolleri

- Sağ el: Fare işaretçisi hareketi
- Sol el: Tıklama, sürükleme ve scroll davranışı
- Parmak pinch: Tıklama/drag başlatma ve bırakma
- El bileği yüksek/alt konumu: Yukarı/aşağı scroll

### Göz ve Kafa Kontrolleri

- İki gözün birlikte kapanması: Tek tıklama / çift tıklama
- Sol göz kapatılması: Sol klik
- Sağ göz kapatılması: Sağ klik
- Kafa hareketi + göz yönelimi: Head Mouse modu

---

## ⚙️ Yapılandırma Detayları

Ayarlar [config.py](config.py) dosyasında tanımlanmıştır. Önemli parametreler:

```python
CAMERA_FPS = 60
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CLICK_THRESHOLD = 30
CLICK_RELEASE_THRESHOLD = 60
SCROLL_SENSITIVITY = 30
BLINK_EAR_THRESHOLD = 0.12
ONE_EURO_MIN_CUTOFF = 0.1
ONE_EURO_BETA = 0.1
HEAD_GAIN_X = 2.5
HEAD_GAIN_Y = 2.5
GAZE_SENSITIVITY_X = 15.0
GAZE_SENSITIVITY_Y = 20.0
```

Bu değerleri değiştirerek hassasiyeti, kararlılığı ve performansı ayarlayabilirsiniz.

---

## 📁 Proje Yapısı

- [main.py](main.py): Ana uygulama akışı, kamera işleme, kontrol mantığı ve görsel çıktı
- [config.py](config.py): Kamera, threshold, duyarlılık ve kontrol ayarları
- [filters.py](filters.py): One Euro Filter implementasyonu
- [LICENSE](LICENSE): MIT lisans bilgisi

---

## 🔄 Çalışma Mantığı

1. Kamera görüntüsü alınır.
2. MediaPipe ile el ve yüz landmark'ları tespit edilir.
3. El hareketleri fare ve click/drag mantığına dönüştürülür.
4. Göz ve kafa hareketleri analitik olarak işlenir.
5. Elde edilen veriler PyAutoGUI üzerinden sistem etkileşimine çevrilir.

---

## 💡 Örnek Kullanım Senaryoları

- Bir sunum sırasında el hareketleriyle slayt geçirme
- Erişilebilirlik amaçlı fare kullanımını azaltma
- Deneysel bir insan-bilgisayar etkileşimi prototipi
- Oyun veya demo ortamında temassız kontrol

---

## 🛠️ Sorun Giderme

### Kamera Açılmıyor

- Webcam'in bağlı olduğundan emin olun.
- Diğer uygulamalar tarafından kullanımda olmadığını kontrol edin.
- DroidCam kullanıyorsanız IP adresini doğru yazdığınızdan emin olun.

### Fare Hareketi Çok Titriyor

- `ONE_EURO_MIN_CUTOFF` ve `ONE_EURO_BETA` değerlerini artırın veya azaltın.
- `HEAD_DEADZONE` ve `GAZE_SENSITIVITY_*` değerlerini dengeleyin.
- Aydınlatma koşullarını iyileştirin.

### Tıklama Çok Sık veya Az Çalışıyor

- `CLICK_THRESHOLD` ve `CLICK_RELEASE_THRESHOLD` değerlerini ayarlayın.
- `BLINK_EAR_THRESHOLD` değerini değiştirerek hassasiyeti optimize edin.
- Kamera konumunu ve yüz pozisyonunu sabitleyin.

### Algılama Zayıfsa

- Işık seviyesini artırın.
- Kamera görüş açısını netleştirin.
- Kullanıcı yüzünün ve ellerinin görüntüde net görünmesini sağlayın.

---

## 🚧 Geliştirme Fikirleri

Bu proje deneysel bir altyapı sunmaktadır. Aşağıdaki geliştirmeler projeye değer katabilir:

- daha iyi blink/twink algılama
- daha stabil head mouse davranışı
- daha akıcı el takibi ve daha düşük gecikme
- daha güçlü hata yönetimi ve log sistemi
- klavye kontrolü ve gesture tabanlı komutlar
- daha iyi performans için model optimizasyonu

---

## 🤝 Katkı Sağlama

Katkıda bulunmak isterseniz:

1. Depoyu forklayın.
2. Değişikliklerinizi yapın.
3. Bir pull request açın.

---

## 📄 Lisans

Bu proje MIT Lisansı altında dağıtılmaktadır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👤 Geliştirici / İmza

Proje ByGhost tarafından geliştirilmiştir.

- Website: https://byghost.tr/
- LinkedIn: https://www.linkedin.com/in/byghost-tr/

## Proje Hakkında

Bu proje, kullanıcıların dokunmadan veya fiziksel cihaz kullanmadan bilgisayar ile etkileşime girmesine olanak tanır. Kamera görüntüsü üzerinden:

- el pozisyonu ile fare hareketi,
- el pinch hareketi ile tıklama/drag,
- göz kırpma davranışı ile tek/çift tıklama,
- kafa hareketiyle baş fare modu,
- göz bebeği yönelimine dayalı gaze kontrolü

sağlanır.

Bu sistem, özellikle aşağıdaki kullanım senaryolarında ilgi çekicidir:

- erişilebilirlik destekli bilgisayar kullanımı,
- temassız kontrol deneyimi,
- oyun veya demo uygulamaları,
- bilgisayar etkileşimi alanında araştırma ve prototip geliştirme.

## Ana Özellikler

- Gerçek zamanlı el takibi
- Sağ el ile fare konumlandırma
- Sol el ile tıklama, sürükleme ve kaydırma işlevleri
- Parmaklar arası mesafeye dayalı pinch algılama
- Göz kapatma tespiti ile tek/çift tıklama
- Sol/sağ göz wink algısı ile farklı tıklama davranışları
- Kafa hareketine dayalı head mouse modu
- Göz bebeği hareketiyle yönlendirme
- DroidCam ve yerel webcam desteği
- Titreşim azaltma amaçlı One Euro Filter entegrasyonu

## Kullanılan Teknolojiler

- Python 3.8+
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy
- ScreenInfo

## Kurulum Rehberi

### 1) Depoyu Klonlayın

```bash
git clone https://github.com/ByGh00st/BioKinetic_Base.git
cd BioKinetic_Base
```

### 2) Sanal Ortam Oluşturun

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3) Bağımlılıkları Yükleyin

```bash
pip install opencv-python mediapipe pyautogui numpy screeninfo
```

### 4) Yapılandırmayı Ayarlayın

[config.py](config.py) dosyasını açın ve aşağıdaki alanları ihtiyaçlarınıza göre düzenleyin:

- kamera çözünürlüğü
- FPS değeri
- tıklama ve sürükleme eşiği
- scroll hızı
- blink ve wink algılama seviyesi
- head mouse hassasiyeti
- One Euro Filter parametreleri

DroidCam kullanacaksanız, [config.py](config.py) içindeki `DROIDCAM_URL` değerini kendi cihazınızın IP adresiyle güncelleyin.

## Çalıştırma

```bash
python main.py
```

Program başlatıldığında kamera akışı açılır ve gerçek zamanlı algılama başlar. Çıkış için ESC tuşuna basın.

## Kontroller

### Genel Kontroller

- ESC: Uygulamadan çıkış
- TAB: Kamera değiştir (yerel kamera / DroidCam)
- S: Scroll modu aç/kapat
- H: Head Mouse modu aç/kapat

### El Kontrolleri

- Sağ el: Fare işaretçisi hareketi
- Sol el: Tıklama, sürükleme ve scroll davranışı
- Parmak pinch: Tıklama/drag başlatma ve bırakma
- El bileği yüksek/alt konumu: Yukarı/aşağı scroll

### Göz ve Kafa Kontrolleri

- İki gözün birlikte kapanması: Tek tıklama / çift tıklama
- Sol göz kapatılması: Sol klik
- Sağ göz kapatılması: Sağ klik
- Kafa hareketi + göz yönelimi: Head Mouse modu

## Yapılandırma Detayları

Ayarlar [config.py](config.py) dosyasında tanımlanmıştır. Önemli parametreler:

```python
CAMERA_FPS = 60
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CLICK_THRESHOLD = 30
CLICK_RELEASE_THRESHOLD = 60
SCROLL_SENSITIVITY = 30
BLINK_EAR_THRESHOLD = 0.12
ONE_EURO_MIN_CUTOFF = 0.1
ONE_EURO_BETA = 0.1
HEAD_GAIN_X = 2.5
HEAD_GAIN_Y = 2.5
GAZE_SENSITIVITY_X = 15.0
GAZE_SENSITIVITY_Y = 20.0
```

Bu değerleri değiştirerek hassasiyeti, kararlılığı ve performansı ayarlayabilirsiniz.

## Proje Yapısı

- [main.py](main.py): Ana uygulama akışı, kamera işleme, kontrol mantığı ve görsel çıktı
- [config.py](config.py): Kamera, threshold, duyarlılık ve kontrol ayarları
- [filters.py](filters.py): One Euro Filter implementasyonu
- [LICENSE](LICENSE): MIT lisans bilgisi

## Çalışma Mantığı

1. Kamera görüntüsü alınır.
2. MediaPipe ile el ve yüz landmark'ları tespit edilir.
3. El hareketleri fare ve click/drag mantığına dönüştürülür.
4. Göz ve kafa hareketleri analitik olarak işlenir.
5. Elde edilen veriler PyAutoGUI üzerinden sistem etkileşimine çevrilir.

## Örnek Kullanım Senaryoları

- Bir sunum sırasında el hareketleriyle slayt geçirme
- Erişilebilirlik amaçlı fare kullanımını azaltma
- Deneysel bir insan-bilgisayar etkileşimi prototipi
- Oyun veya demo ortamında temassız kontrol

## Sorun Giderme

### Kamera Açılmıyor

- Webcam'in bağlı olduğundan emin olun.
- Diğer uygulamalar tarafından kullanımda olmadığını kontrol edin.
- DroidCam kullanıyorsanız IP adresini doğru yazdığınızdan emin olun.

### Fare Hareketi Çok Titriyor

- `ONE_EURO_MIN_CUTOFF` ve `ONE_EURO_BETA` değerlerini artırın veya azaltın.
- `HEAD_DEADZONE` ve `GAZE_SENSITIVITY_*` değerlerini dengeleyin.
- Aydınlatma koşullarını iyileştirin.

### Tıklama Çok Sık veya Az Çalışıyor

- `CLICK_THRESHOLD` ve `CLICK_RELEASE_THRESHOLD` değerlerini ayarlayın.
- `BLINK_EAR_THRESHOLD` değerini değiştirerek hassasiyeti optimize edin.
- Kamera konumunu ve yüz pozisyonunu sabitleyin.

### Algılama Zayıfsa

- Işık seviyesini artırın.
- Kamera görüş açısını netleştirin.
- Kullanıcı yüzünün ve ellerinin görüntüde net görünmesini sağlayın.

## Geliştirme Fikirleri

Bu proje deneysel bir altyapı sunmaktadır. Aşağıdaki geliştirmeler projeye değer katabilir:

- daha iyi blink/twink algılama
- daha stabil head mouse davranışı
- daha akıcı el takibi ve daha düşük gecikme
- daha güçlü hata yönetimi ve log sistemi
- klavye kontrolü ve gesture tabanlı komutlar
- daha iyi performans için model optimizasyonu

## Katkı Sağlama

Katkıda bulunmak isterseniz:

1. Depoyu forklayın.
2. Değişikliklerinizi yapın.
3. Bir pull request açın.

## Lisans

Bu proje MIT Lisansı altında dağıtılmaktadır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## Geliştirici / İmza

Proje ByGhost tarafından geliştirilmiştir.

- Website: https://byghost.tr/
- LinkedIn: https://www.linkedin.com/in/byghost-tr/
