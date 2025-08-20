#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoClicker Flet Uygulaması Başlatıcı
Modern ve animasyonlu Flet UI ile AutoClicker uygulaması

Kullanım:
    python run_flet_app.py

Gereksinimler:
    pip install -r requirements_flet.txt
"""

import sys
import os

# Gerekli modüllerin kontrolü
try:
    import flet as ft
    import pyautogui
    import pynput
    from PIL import Image
except ImportError as e:
    print(f"❌ Gerekli modül bulunamadı: {e}")
    print("\n📦 Gerekli modülleri yüklemek için:")
    print("pip install -r requirements_flet.txt")
    input("\nÇıkmak için Enter tuşuna basın...")
    sys.exit(1)

# Ana uygulama modülünü import et
try:
    from autoclicker_flet import main
except ImportError:
    print("❌ autoclicker_flet.py dosyası bulunamadı!")
    print("Lütfen dosyanın aynı dizinde olduğundan emin olun.")
    input("\nÇıkmak için Enter tuşuna basın...")
    sys.exit(1)

def check_dependencies():
    """Bağımlılıkları kontrol eder"""
    print("🔍 Bağımlılıklar kontrol ediliyor...")
    
    dependencies = {
        'flet': 'Flet UI framework',
        'pyautogui': 'Otomatik mouse/klavye kontrolü',
        'pynput': 'Klavye/mouse dinleme',
        'PIL': 'Görüntü işleme (Pillow)'
    }
    
    missing = []
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description}")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Eksik modüller: {', '.join(missing)}")
        print("\n📦 Yüklemek için: pip install -r requirements_flet.txt")
        return False
    
    print("\n✅ Tüm bağımlılıklar mevcut!")
    return True

def setup_pyautogui():
    """PyAutoGUI güvenlik ayarlarını yapar"""
    print("⚙️  PyAutoGUI güvenlik ayarları yapılıyor...")
    pyautogui.FAILSAFE = True  # Mouse sol üst köşeye giderse durdur
    pyautogui.PAUSE = 0.1      # İşlemler arası bekleme
    print("✅ Güvenlik ayarları tamamlandı")

def main_app():
    """Ana uygulamayı başlatır"""
    print("\n🚀 AutoClicker Flet uygulaması başlatılıyor...")
    print("\n📋 Kullanım İpuçları:")
    print("• Q tuşu ile aktif tıklamayı durdurabilirsiniz")
    print("• Mouse'u ekranın sol üst köşesine götürürseniz güvenlik nedeniyle durur")
    print("• Koordinat seçimi için mouse'a tıklayın")
    print("• Renk seçimi için istediğiniz rengin üzerine tıklayın")
    print("\n" + "="*50)
    
    try:
        # Flet uygulamasını başlat
        ft.app(
            target=main,
            name="AutoClicker Pro",
            assets_dir="assets",  # Eğer assets klasörü varsa
        )
    except Exception as e:
        print(f"\n❌ Uygulama başlatma hatası: {e}")
        print("\n🔧 Olası çözümler:")
        print("1. Tüm bağımlılıkların yüklü olduğundan emin olun")
        print("2. Python sürümünüzün 3.7+ olduğundan emin olun")
        print("3. Yönetici olarak çalıştırmayı deneyin")
        input("\nÇıkmak için Enter tuşuna basın...")
        return False
    
    return True

if __name__ == "__main__":
    print("🖱️  AutoClicker Pro - Modern Flet Edition")
    print("="*50)
    
    # Bağımlılık kontrolü
    if not check_dependencies():
        input("\nÇıkmak için Enter tuşuna basın...")
        sys.exit(1)
    
    # PyAutoGUI ayarları
    setup_pyautogui()
    
    # Ana uygulamayı başlat
    success = main_app()
    
    if success:
        print("\n✅ Uygulama başarıyla kapatıldı")
    else:
        print("\n❌ Uygulama hata ile sonlandı")
        sys.exit(1)