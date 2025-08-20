# 🖱️ AutoClicker Pro - Modern Flet Edition

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flet](https://img.shields.io/badge/Flet-0.21.0+-green.svg)](https://flet.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

Modern ve kullanıcı dostu arayüze sahip gelişmiş AutoClicker uygulaması. **Flet** framework ile tasarlanmış, animasyonlu ve responsive tasarıma sahip.

## 📸 Ekran Görüntüleri

*Modern ve şık arayüz tasarımı*

## ✨ Özellikler

### 🎯 Tek Nokta Tıklama
- 📍 Manuel koordinat girişi veya ekrandan konum seçimi
- ⏱️ Ayarlanabilir tıklama aralığı
- 🎨 Renk bazlı tıklama kontrolü
- 🖱️ Gerçek zamanlı mouse pozisyon takibi

### 📋 Sıralı Tıklama
- 📝 Çoklu koordinat listesi yönetimi
- 🔄 Sıralı koordinat tıklama
- 🎨 Koordinat bazlı renk kontrolü
- ➕ Dinamik koordinat ekleme/silme

### 🔍 Alan Tarama (Area Scan)
- 📐 Belirli alan içinde renk tarama
- 🎯 Renk bulunduğunda/bulunamadığında farklı aksiyonlar
- 🔄 Sürekli alan izleme
- 📊 Gerçek zamanlı tarama sonuçları

### 🎨 Gelişmiş Renk Kontrolü
- 🖱️ Ekrandan renk seçimi (mouse ile)
- 🎭 Manuel RGB renk girişi
- 📋 Çoklu renk listesi desteği
- 🎚️ Ayarlanabilir renk toleransı (0-50)
- 👁️ Renk önizleme ile görsel liste

### ⌨️ Klavye Kısayolları
- **Q tuşu**: Aktif tıklamayı anında durdurur
- 🛡️ Güvenlik: Mouse sol üst köşeye giderse otomatik durur

### 🎨 Modern UI Tasarımı
- ✨ **Flet** framework ile modern arayüz
- 🎬 Animasyonlu butonlar ve geçişler
- 🃏 Kart tabanlı (Card-based) düzen
- 📱 Responsive tasarım
- 📑 Sekme tabanlı navigasyon
- 🔄 Gerçek zamanlı durum güncellemeleri
- 🎨 Modern renk paleti ve ikonlar

## 🚀 Hızlı Başlangıç

### 📥 İndirme Seçenekleri

#### 1. Hazır Executable (Önerilen)
**Windows kullanıcıları için:**
- [📦 color_clicker.exe İndir](https://github.com/fettahfurkan/color_clicker/releases/latest/download/color_clicker.exe)
- İndirdikten sonra doğrudan çalıştırabilirsiniz
- Python kurulumu gerektirmez

#### 2. Kaynak Koddan Çalıştırma
```bash
# Repoyu klonlayın
git clone https://github.com/fettahfurkan/color_clicker.git
cd color_clicker

# Bağımlılıkları yükleyin
pip install -r requirements_flet.txt

# Uygulamayı çalıştırın
python run_flet_app.py
```

### 📋 Gereksinimler
- Python 3.7+ (kaynak koddan çalıştırma için)
- Windows/Linux/macOS

## 📖 Kullanım Kılavuzu

### 🖱️ Tek Nokta Tıklama

1. **Koordinat Belirleme:**
   - Manuel olarak X, Y koordinatlarını girin
   - VEYA "🎯 Ekrandan Konum Seç" butonuna tıklayıp mouse ile seçin

2. **Ayarları Yapın:**
   - Tıklama aralığını saniye cinsinden ayarlayın
   - İsteğe bağlı olarak renk kontrolünü etkinleştirin

3. **Renk Kontrolü (Opsiyonel):**
   - "Renk kontrolünü etkinleştir" switch'ini açın
   - "🎨 Ekrandan Renk Seç" ile mouse ile renk seçin
   - VEYA "🎭 Manuel Renk Seç" ile RGB değerleri girin
   - Renk toleransını ayarlayın (varsayılan: 10)

4. **Başlatın:**
   - "▶️ Başlat" butonuna tıklayın
   - "Q" tuşu ile durdurun

### 📋 Sıralı Tıklama

1. **Koordinat Listesi Oluşturun:**
   - "➕ Koordinat Ekle" butonuna tıklayın
   - Ekrandan istediğiniz noktaları sırayla seçin
   - Gerekirse "🗑️ Seçili Koordinatı Sil" ile düzenleyin

2. **Ayarları Yapın:**
   - Koordinatlar arası tıklama aralığını ayarlayın
   - İsteğe bağlı olarak renk kontrolünü etkinleştirin

3. **Başlatın:**
   - "▶️ Sıralı Tıklamayı Başlat" butonuna tıklayın
   - Koordinatlar sırayla ve döngüsel olarak tıklanır
   - "Q" tuşu ile durdurun

### 🔍 Alan Tarama

1. **Tarama Alanı Seçin:**
   - "📐 Alan Seç" butonuna tıklayın
   - Mouse ile dikdörtgen alan çizin

2. **Hedef Renkleri Belirleyin:**
   - "🎨 Hedef Renk Ekle" ile aranacak renkleri seçin
   - Renk toleransını ayarlayın

3. **Aksiyonları Tanımlayın:**
   - Renk bulunduğunda tıklanacak koordinatları ekleyin
   - Renk bulunamadığında tıklanacak koordinatları ekleyin

4. **Taramayı Başlatın:**
   - "🔍 Alan Taramayı Başlat" butonuna tıklayın
   - "Q" tuşu ile durdurun

## 🔧 Teknik Detaylar

### 🛠️ Kullanılan Teknolojiler
- **Flet**: Modern UI framework
- **PyAutoGUI**: Mouse/klavye otomasyonu
- **Pynput**: Klavye/mouse dinleme
- **Pillow (PIL)**: Görüntü işleme ve renk algılama
- **Threading**: Çoklu thread desteği

### 🛡️ Güvenlik Özellikleri
- **Failsafe**: Mouse sol üst köşeye giderse otomatik durur
- **Q Tuşu**: Acil durdurma
- **Thread Safety**: Güvenli çoklu thread işlemleri
- **Hata Yönetimi**: Kapsamlı hata yakalama ve kullanıcı bildirimleri

### ⚡ Performans
- **Düşük CPU Kullanımı**: Optimize edilmiş thread yapısı
- **Gerçek Zamanlı**: 100ms'de mouse pozisyon güncellemesi
- **Responsive UI**: Animasyonlu ve akıcı arayüz

## 📱 Platform Desteği

- ✅ **Windows** (Test edildi)
- ✅ **Linux** (Desteklenir)
- ✅ **macOS** (Desteklenir)

## ⚠️ Önemli Notlar

1. **Güvenlik**: Uygulama çalışırken mouse'u ekranın sol üst köşesine götürürseniz güvenlik nedeniyle durur

2. **Koordinat Seçimi**: Koordinat seçimi sırasında istediğiniz noktaya mouse ile tıklayın

3. **Renk Seçimi**: Renk seçimi sırasında istediğiniz rengin üzerine mouse ile tıklayın

4. **Performans**: Çok düşük tıklama aralıkları (0.1s altı) sistem performansını etkileyebilir

5. **İzinler**: Bazı sistemlerde yönetici izni gerekebilir

## 🐛 Sorun Giderme

### Uygulama Başlamıyor
```bash
# Bağımlılıkları kontrol edin
python -c "import flet, pyautogui, pynput, PIL; print('Tüm modüller yüklü!')"

# Gerekirse tekrar yükleyin
pip install --upgrade -r requirements_flet.txt
```

### Mouse/Klavye Çalışmıyor
- **Linux**: `sudo apt-get install python3-tk python3-dev`
- **macOS**: Accessibility izinleri verin
- **Windows**: Yönetici olarak çalıştırın

### Renk Algılama Sorunları
- Renk toleransını artırın (10-30 arası)
- Farklı renk örnekleri ekleyin
- Ekran çözünürlüğünü kontrol edin

## 🤝 Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz! Lütfen:

1. Bu repoyu fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- [Flet](https://flet.dev) - Modern UI framework
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - Otomasyon kütüphanesi
- [Pynput](https://pynput.readthedocs.io/) - Input monitoring

## 📞 İletişim

- GitHub: [@fettahfurkan](https://github.com/fettahfurkan)
- Proje Linki: [https://github.com/fettahfurkan/color_clicker](https://github.com/fettahfurkan/color_clicker)

---

**🎉 Modern AutoClicker deneyiminin keyfini çıkarın!**

⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!