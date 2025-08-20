# 🖱️ AutoClicker Pro - Modern Flet Edition

PyQt5 tabanlı AutoClicker uygulamasının **Flet** ile modern, animasyonlu ve kullanıcı dostu tasarıma sahip yeni versiyonu.

## ✨ Özellikler

### 🎯 Tek Nokta Tıklama
- Manuel koordinat girişi veya ekrandan konum seçimi
- Ayarlanabilir tıklama aralığı
- Renk bazlı tıklama kontrolü
- Gerçek zamanlı mouse pozisyon takibi

### 📋 Sıralı Tıklama
- Çoklu koordinat listesi yönetimi
- Sıralı koordinat tıklama
- Koordinat bazlı renk kontrolü
- Dinamik koordinat ekleme/silme

### 🎨 Gelişmiş Renk Kontrolü
- Ekrandan renk seçimi (mouse ile)
- Manuel RGB renk girişi
- Çoklu renk listesi desteği
- Ayarlanabilir renk toleransı (0-50)
- Renk önizleme ile görsel liste

### ⌨️ Klavye Kısayolları
- **Q tuşu**: Aktif tıklamayı anında durdurur
- Güvenlik: Mouse sol üst köşeye giderse otomatik durur

### 🎨 Modern UI Tasarımı
- **Flet** framework ile modern arayüz
- Animasyonlu butonlar ve geçişler
- Kart tabanlı (Card-based) düzen
- Responsive tasarım
- Sekme tabanlı navigasyon
- Gerçek zamanlı durum güncellemeleri
- Modern renk paleti ve ikonlar

## 📦 Kurulum

### Gereksinimler
- Python 3.7+
- Windows/Linux/macOS

### Adım 1: Bağımlılıkları Yükleyin
```bash
pip install -r requirements_flet.txt
```

### Adım 2: Uygulamayı Çalıştırın
```bash
python run_flet_app.py
```

veya doğrudan:
```bash
python autoclicker_flet.py
```

## 🚀 Kullanım Kılavuzu

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

### 🎨 Renk Kontrolü Detayları

- **Ekrandan Renk Seçimi:** Mouse ile istediğiniz pikselin rengini seçin
- **Manuel Renk Seçimi:** RGB değerlerini (0-255) manuel olarak girin
- **Renk Toleransı:** Benzer renkleri kabul etme aralığı (0=tam eşleşme, 50=çok esnek)
- **Çoklu Renk:** Birden fazla renk ekleyebilir, herhangi biri eşleştiğinde tıklama yapar

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler
- **Flet**: Modern UI framework
- **PyAutoGUI**: Mouse/klavye otomasyonu
- **Pynput**: Klavye/mouse dinleme
- **Pillow (PIL)**: Görüntü işleme ve renk algılama
- **Threading**: Çoklu thread desteği

### Güvenlik Özellikleri
- **Failsafe**: Mouse sol üst köşeye giderse otomatik durur
- **Q Tuşu**: Acil durdurma
- **Thread Safety**: Güvenli çoklu thread işlemleri
- **Hata Yönetimi**: Kapsamlı hata yakalama ve kullanıcı bildirimleri

### Performans
- **Düşük CPU Kullanımı**: Optimize edilmiş thread yapısı
- **Gerçek Zamanlı**: 100ms'de mouse pozisyon güncellemesi
- **Responsive UI**: Animasyonlu ve akıcı arayüz

## 📱 Platform Desteği

- ✅ **Windows** (Test edildi)
- ✅ **Linux** (Desteklenir)
- ✅ **macOS** (Desteklenir)

## 🆚 PyQt5 Versiyonundan Farklar

### ✨ Yeni Özellikler
- Modern Flet UI framework
- Animasyonlu butonlar ve geçişler
- Kart tabanlı düzen
- Responsive tasarım
- Gelişmiş renk önizleme
- Daha iyi hata mesajları
- Modern ikonlar ve tipografi

### 🔄 Korunan Özellikler
- Tüm tıklama fonksiyonları
- Renk kontrolü algoritmaları
- Klavye kısayolları
- Thread yapısı
- Güvenlik özellikleri

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
- Linux'ta: `sudo apt-get install python3-tk python3-dev`
- macOS'ta: Accessibility izinleri verin
- Windows'ta: Yönetici olarak çalıştırın

### Renk Algılama Sorunları
- Renk toleransını artırın (10-30 arası)
- Farklı renk örnekleri ekleyin
- Ekran çözünürlüğünü kontrol edin

## 📄 Lisans

Bu proje açık kaynak kodludur ve eğitim amaçlıdır. Sorumlu kullanım için lütfen yerel yasalara uyun.

## 🤝 Katkıda Bulunma

Hata raporları, özellik istekleri ve kod katkıları memnuniyetle karşılanır!

---

**🎉 Modern AutoClicker deneyiminin keyfini çıkarın!**