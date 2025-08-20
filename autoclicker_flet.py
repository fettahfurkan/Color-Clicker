import flet as ft
import threading
import time
import pyautogui
from pynput import keyboard
from pynput.mouse import Listener as MouseListener
from PIL import ImageGrab
from typing import Optional, List, Tuple, Dict
import asyncio

class ClickingThread(threading.Thread):
    """Tıklama işlemini ayrı thread'de çalıştırır"""
    
    def __init__(self, x, y, interval, coordinate_color=None, color_tolerance=10, status_callback=None):
        super().__init__()
        self.x = x
        self.y = y
        self.interval = interval
        self.is_running = True
        self.coordinate_color = coordinate_color
        self.color_tolerance = color_tolerance
        self.status_callback = status_callback
        self.daemon = True
        
    def run(self):
        while self.is_running:
            try:
                should_click = True
                if self.coordinate_color:
                    current_color = self.get_pixel_color(self.x, self.y)
                    if current_color:
                        should_click = self.color_matches(current_color, self.coordinate_color, self.color_tolerance)
                        if should_click:
                            self.update_status(f"Renk eşleşti, tıklandı: ({self.x}, {self.y}) - Hedef: {self.coordinate_color}, Mevcut: {current_color}")
                        else:
                            self.update_status(f"Renk eşleşmedi: ({self.x}, {self.y}) - Hedef: {self.coordinate_color}, Mevcut: {current_color}")
                    else:
                        should_click = False
                        self.update_status(f"Renk okunamadı: ({self.x}, {self.y})")
                else:
                    self.update_status(f"Tıklandı: ({self.x}, {self.y}) - Renk şartı yok")
                
                if should_click:
                    pyautogui.click(self.x, self.y)
                    
                time.sleep(self.interval)
            except Exception as e:
                self.update_status(f"Hata: {e}")
                break
    
    def get_pixel_color(self, x, y):
        """Belirtilen koordinattaki pixel rengini alır"""
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            pixel_color = screenshot.getpixel((0, 0))
            return pixel_color[:3]
        except Exception:
            return None
    
    def color_matches(self, color1, color2, tolerance):
        """İki rengin tolerans dahilinde eşleşip eşleşmediğini kontrol eder"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return (abs(r1 - r2) <= tolerance and 
                abs(g1 - g2) <= tolerance and 
                abs(b1 - b2) <= tolerance)
    
    def update_status(self, message):
        if self.status_callback:
            self.status_callback(message)
                
    def stop(self):
        self.is_running = False

class SequentialClickingThread(threading.Thread):
    """Sıralı tıklama işlemini ayrı thread'de çalıştırır"""
    
    def __init__(self, coordinates: List[dict], interval: float, color_tolerance: int, 
                 color_list: Optional[List[Tuple[int, int, int]]] = None, status_callback=None):
        super().__init__()
        self.coordinates = coordinates
        self.interval = interval
        self.color_tolerance = color_tolerance
        self.is_running = True
        self.current_index = 0
        self.color_list = color_list or []
        self.status_callback = status_callback
        self.daemon = True
        
    def run(self):
        while self.is_running and self.coordinates:
            try:
                coord = self.coordinates[self.current_index]
                x, y = coord['x'], coord['y']
                
                should_click = True
                if self.color_list:
                    current_color = self.get_pixel_color(x, y)
                    if current_color:
                        should_click = self.check_color_match(current_color)
                        if should_click:
                            self.update_status(f"Koordinat {self.current_index + 1} renk eşleşti, tıklandı: ({x}, {y}) - Mevcut: {current_color}")
                        else:
                            self.update_status(f"Koordinat {self.current_index + 1} renk eşleşmedi: ({x}, {y}) - Mevcut: {current_color}")
                    else:
                        should_click = False
                        self.update_status(f"Koordinat {self.current_index + 1} renk okunamadı: ({x}, {y})")
                else:
                    self.update_status(f"Koordinat {self.current_index + 1} tıklandı: ({x}, {y}) - Renk şartı yok")
                
                if should_click:
                    pyautogui.click(x, y)
                
                self.current_index = (self.current_index + 1) % len(self.coordinates)
                time.sleep(self.interval)
            except Exception as e:
                self.update_status(f"Hata: {e}")
                break
    
    def get_pixel_color(self, x, y):
        """Belirtilen koordinattaki pixel rengini alır"""
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            pixel_color = screenshot.getpixel((0, 0))
            return pixel_color[:3]
        except Exception:
            return None
    
    def check_color_match(self, current_color):
        """Mevcut rengin listede olup olmadığını kontrol eder"""
        if not self.color_list:
            return True
        for target_color in self.color_list:
            if self.color_matches(current_color, target_color, self.color_tolerance):
                return True
        return False
    
    def color_matches(self, color1, color2, tolerance):
        """İki rengin tolerans dahilinde eşleşip eşleşmediğini kontrol eder"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return (abs(r1 - r2) <= tolerance and 
                abs(g1 - g2) <= tolerance and 
                abs(b1 - b2) <= tolerance)
    
    def update_status(self, message):
        if self.status_callback:
            self.status_callback(message)
                
    def stop(self):
        self.is_running = False

class AreaScanThread(threading.Thread):
    """Ekranda alan tarar ve koşullu tıklama yapar"""
    
    def __init__(self, scan_area: Dict, target_colors: List[Tuple[int, int, int]], 
                 coordinates_if_found: List[dict], coordinates_if_not_found: List[dict],
                 interval: float, color_tolerance: int, status_callback=None):
        super().__init__()
        self.scan_area = scan_area  # {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        self.target_colors = target_colors
        self.coordinates_if_found = coordinates_if_found
        self.coordinates_if_not_found = coordinates_if_not_found
        self.interval = interval
        self.color_tolerance = color_tolerance
        self.is_running = True
        self.status_callback = status_callback
        self.current_index_found = 0
        self.current_index_not_found = 0
        self.daemon = True
        
    def run(self):
        while self.is_running:
            try:
                # Alanda renk arama
                color_found = self.scan_area_for_colors()
                
                if color_found:
                    # Renk bulundu - "bulundu" listesinden tıkla
                    if self.coordinates_if_found:
                        coord = self.coordinates_if_found[self.current_index_found]
                        x, y = coord['x'], coord['y']
                        pyautogui.click(x, y)
                        self.update_status(f"🎯 Renk BULUNDU! Koordinat {self.current_index_found + 1} tıklandı: ({x}, {y})")
                        self.current_index_found = (self.current_index_found + 1) % len(self.coordinates_if_found)
                    else:
                        self.update_status("🎯 Renk bulundu ama 'Renk Bulundu' koordinat listesi boş!")
                else:
                    # Renk bulunamadı - "bulunamadı" listesinden tıkla
                    if self.coordinates_if_not_found:
                        coord = self.coordinates_if_not_found[self.current_index_not_found]
                        x, y = coord['x'], coord['y']
                        pyautogui.click(x, y)
                        self.update_status(f"❌ Renk BULUNAMADI! Koordinat {self.current_index_not_found + 1} tıklandı: ({x}, {y})")
                        self.current_index_not_found = (self.current_index_not_found + 1) % len(self.coordinates_if_not_found)
                    else:
                        self.update_status("❌ Renk bulunamadı ama 'Renk Bulunamadı' koordinat listesi boş!")
                
                time.sleep(self.interval)
            except Exception as e:
                self.update_status(f"Hata: {e}")
                break
    
    def scan_area_for_colors(self):
        """Belirtilen alanda hedef renkleri arar"""
        try:
            x1, y1 = self.scan_area['x1'], self.scan_area['y1']
            x2, y2 = self.scan_area['x2'], self.scan_area['y2']
            
            # Alan görüntüsünü al
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            width, height = screenshot.size
            
            # Her pixel'i kontrol et (performans için her 3. pixel)
            for y in range(0, height, 3):
                for x in range(0, width, 3):
                    try:
                        pixel_color = screenshot.getpixel((x, y))[:3]
                        
                        # Hedef renklerle karşılaştır
                        for target_color in self.target_colors:
                            if self.color_matches(pixel_color, target_color, self.color_tolerance):
                                return True
                    except:
                        continue
            
            return False
        except Exception:
            return False
    
    def color_matches(self, color1, color2, tolerance):
        """İki rengin tolerans dahilinde eşleşip eşleşmediğini kontrol eder"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return (abs(r1 - r2) <= tolerance and 
                abs(g1 - g2) <= tolerance and 
                abs(b1 - b2) <= tolerance)
    
    def update_status(self, message):
        if self.status_callback:
            self.status_callback(message)
                
    def stop(self):
        self.is_running = False

class AutoClickerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🖱️ AutoClicker Color"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.width = 457
        self.page.window.height = 543
        self.page.window.resizable = True
        self.page.padding = 10
        
        # Renk teması
        self.primary_color = ft.Colors.BLUE_600
        self.secondary_color = ft.Colors.BLUE_100
        self.success_color = ft.Colors.GREEN_600
        self.error_color = ft.Colors.RED_600
        self.warning_color = ft.Colors.ORANGE_600
        
        # Değişkenler
        self.click_x = 0
        self.click_y = 0
        self.click_interval = 1.0
        self.is_clicking = False
        self.click_thread = None
        self.selecting_position = False
        self.mouse_listener = None
        
        # Sıralı tıklama için değişkenler
        self.coordinates_list = []
        self.sequential_thread = None
        self.is_sequential_clicking = False
        self.adding_coordinate = False
        
        # Renk kontrolü için değişkenler
        self.color_list: List[Tuple[int, int, int]] = []
        self.color_check_enabled = False
        self.selecting_color = False
        self.color_tolerance = 10
        
        # Alan tarama için değişkenler
        self.scan_area = None  # {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
        self.coordinates_if_found = []  # Renk bulunduğunda tıklanacak koordinatlar
        self.coordinates_if_not_found = []  # Renk bulunamadığında tıklanacak koordinatlar
        self.area_scan_thread = None
        self.is_area_scanning = False
        self.selecting_area = False
        self.area_start_point = None
        
        # UI bileşenleri
        self.status_text = ft.Text(
            "Hazır - Mod seçin ve başlatın",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=self.success_color
        )
        
        # Mouse pozisyonu için timer
        self.mouse_timer = None
        
        # Klavye dinleyicisi
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        
        self.setup_ui()
        self.start_mouse_tracking()
    
    def setup_ui(self):
        """Ana UI'yi kurar"""
        # Ana başlık
        title = ft.Container(
            content=ft.Text(
                "🖱️ AutoClicker Pro",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=self.primary_color,
                text_align=ft.TextAlign.CENTER
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(bottom=10)
        )
        
        # Tab yapısı
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Tek Nokta Tıklama",
                    icon=ft.Icons.MOUSE,
                    content=self.create_single_click_tab()
                ),
                ft.Tab(
                    text="Sıralı Tıklama",
                    icon=ft.Icons.LIST,
                    content=self.create_sequential_click_tab()
                ),
                ft.Tab(
                    text="Alan Tarama",
                    icon=ft.Icons.SCANNER,
                    content=self.create_area_scan_tab()
                ),
                ft.Tab(
                    text="Yardım",
                    icon=ft.Icons.HELP,
                    content=self.create_help_tab()
                )
            ],
            expand=True
        )
        
        # Durum kartı
        status_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "📊 Durum",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=self.primary_color
                    ),
                    self.status_text
                ], spacing=5),
                padding=12
            ),
            elevation=2,
            margin=ft.margin.only(top=10)
        )
        
        # Çıkış butonu
        exit_button = ft.ElevatedButton(
            text="🚪 Çıkış",
            icon=ft.Icons.EXIT_TO_APP,
            on_click=self.exit_app,
            bgcolor=self.error_color,
            color=ft.Colors.WHITE,
            width=120,
            height=40
        )
        
        # Ana layout
        self.page.add(
            ft.Column([
                title,
                tabs,
                status_card,
                ft.Container(
                    content=exit_button,
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(top=10)
                )
            ], expand=True, spacing=10)
        )
    
    def create_single_click_tab(self):
        """Tek nokta tıklama tab'ını oluşturur"""
        # Koordinat girişleri
        self.x_input = ft.TextField(
            label="X Koordinatı",
            value=str(self.click_x),
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.y_input = ft.TextField(
            label="Y Koordinatı",
            value=str(self.click_y),
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        # Mouse pozisyonu
        self.mouse_pos_text = ft.Text(
            "Fare pozisyonu: (0, 0)",
            size=14,
            color=ft.Colors.GREY_600
        )
        
        # Konum seçme butonu
        select_position_btn = ft.ElevatedButton(
            text="🎯 Ekrandan Konum Seç",
            icon=ft.Icons.MY_LOCATION,
            on_click=self.start_position_selection,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=self.primary_color,
                elevation=2,
                animation_duration=200
            ),
            width=180
        )
        
        # Tıklama aralığı
        self.interval_input = ft.TextField(
            label="Tıklama Aralığı (saniye)",
            value=str(self.click_interval),
            width=180,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        # Renk kontrolü
        self.color_check_switch = ft.Switch(
            label="Renk kontrolünü etkinleştir",
            value=False,
            on_change=self.toggle_color_check
        )
        
        # Renk listesi
        self.color_list_view = ft.ListView(
            height=100,
            spacing=3
        )
        
        # Renk butonları
        color_buttons = ft.Row([
            ft.ElevatedButton(
                text="🎨 Ekrandan Renk Seç",
                icon=ft.Icons.COLORIZE,
                on_click=self.start_color_selection,
                style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_400, color=ft.Colors.WHITE)
            ),
            ft.ElevatedButton(
                text="🎭 Manuel Renk Seç",
                icon=ft.Icons.PALETTE,
                on_click=self.manual_color_selection,
                style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO_400, color=ft.Colors.WHITE)
            )
        ], spacing=10)
        
        # Renk toleransı
        self.color_tolerance_slider = ft.Slider(
            min=0,
            max=50,
            value=10,
            divisions=50,
            label="Renk Toleransı: {value}",
            on_change=self.update_color_tolerance
        )
        
        # Kontrol butonları
        self.start_btn = ft.ElevatedButton(
            text="▶️ Başlat",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.start_clicking,
            style=ft.ButtonStyle(
                bgcolor=self.success_color,
                color=ft.Colors.WHITE,
                elevation=3,
                animation_duration=200
            ),
            width=120
        )
        
        self.stop_btn = ft.ElevatedButton(
            text="⏹️ Durdur",
            icon=ft.Icons.STOP,
            on_click=self.stop_clicking,
            style=ft.ButtonStyle(
                bgcolor=self.error_color,
                color=ft.Colors.WHITE,
                elevation=3,
                animation_duration=200
            ),
            width=120,
            disabled=True
        )
        
        return ft.Container(
            content=ft.Column([
                # Konum seçimi kartı
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("📍 Tıklama Konumu", size=16, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            ft.Row([self.x_input, self.y_input], spacing=15),
                            self.mouse_pos_text,
                            select_position_btn
                        ], spacing=10),
                        padding=12
                    ),
                    elevation=2
                ),
                
                # Ayarlar kartı
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("⚙️ Tıklama Ayarları", size=16, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            self.interval_input
                        ], spacing=10),
                        padding=12
                    ),
                    elevation=2
                ),
                
                # Renk kontrolü kartı
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("🎨 Renk Kontrolü", size=16, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            self.color_check_switch,
                            color_buttons,
                            ft.Text("Renk Listesi:", weight=ft.FontWeight.BOLD, size=14),
                            self.color_list_view,
                            ft.Text("Renk Toleransı:", weight=ft.FontWeight.BOLD, size=14),
                            self.color_tolerance_slider,
                            ft.Row([
                                ft.ElevatedButton(
                                    text="🗑️ Seçili Rengi Sil",
                                    on_click=self.remove_selected_color,
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE)
                                ),
                                ft.ElevatedButton(
                                    text="🧹 Tümünü Temizle",
                                    on_click=self.clear_all_colors,
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_600, color=ft.Colors.WHITE)
                                )
                            ], spacing=8)
                        ], spacing=10),
                        padding=12
                    ),
                    elevation=2
                ),
                
                # Kontrol butonları kartı
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("🎮 Kontrol", size=16, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            ft.Row([self.start_btn, self.stop_btn], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
                        ], spacing=10),
                        padding=12
                    ),
                    elevation=2
                )
            ], spacing=12, scroll=ft.ScrollMode.AUTO),
            padding=15
        )
    
    def create_sequential_click_tab(self):
        """Sıralı tıklama tab'ını oluşturur"""
        # Koordinat listesi
        self.coord_list_view = ft.ListView(
            height=150,
            spacing=3
        )
        
        # Sıralı tıklama aralığı
        self.seq_interval_input = ft.TextField(
            label="Tıklama Aralığı (saniye)",
            value="1.0",
            width=180,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        # Sıralı renk kontrolü
        self.seq_color_check_switch = ft.Switch(
            label="Renk kontrolünü etkinleştir",
            value=False
        )
        
        # Sıralı kontrol butonları
        self.seq_start_btn = ft.ElevatedButton(
            text="▶️ Sıralı Başlat",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.start_sequential_clicking,
            style=ft.ButtonStyle(
                bgcolor=self.success_color,
                color=ft.Colors.WHITE,
                elevation=3
            ),
            width=140
        )
        
        self.seq_stop_btn = ft.ElevatedButton(
            text="⏹️ Sıralı Durdur",
            icon=ft.Icons.STOP,
            on_click=self.stop_sequential_clicking,
            style=ft.ButtonStyle(
                bgcolor=self.error_color,
                color=ft.Colors.WHITE,
                elevation=3
            ),
            width=140,
            disabled=True
        )
        
        return ft.Container(
            content=ft.Column([
                # Koordinat yönetimi kartı
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("📍 Koordinat Listesi", size=16, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            ft.Row([
                                ft.ElevatedButton(
                                    text="➕ Ekle",
                                    icon=ft.Icons.ADD_LOCATION,
                                    on_click=self.add_coordinate_from_screen,
                                    style=ft.ButtonStyle(bgcolor=self.primary_color, color=ft.Colors.WHITE)
                                ),
                                ft.ElevatedButton(
                                    text="🗑️ Sil",
                                    icon=ft.Icons.DELETE,
                                    on_click=self.remove_selected_coordinate,
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE)
                                ),
                                ft.ElevatedButton(
                                    text="🧹 Temizle",
                                    icon=ft.Icons.CLEAR_ALL,
                                    on_click=self.clear_all_coordinates,
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_600, color=ft.Colors.WHITE)
                                )
                            ], spacing=8),
                            self.coord_list_view
                        ], spacing=10),
                        padding=12
                    ),
                    elevation=2
                ),
                
                # Sıralı ayarlar kartı
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("⚙️ Sıralı Ayarlar", size=16, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            self.seq_interval_input,
                            self.seq_color_check_switch,
                            ft.Text(
                                "Not: Renk kontrolü etkinse, 'Tek Nokta' sekmesindeki renk listesi kullanılır.",
                                size=11,
                                color=ft.Colors.GREY_600,
                                italic=True
                            )
                        ], spacing=10),
                        padding=12
                    ),
                    elevation=2
                ),
                
                # Sıralı kontrol kartı
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("🎮 Sıralı Kontrol", size=16, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            ft.Row([self.seq_start_btn, self.seq_stop_btn], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
                        ], spacing=10),
                        padding=12
                    ),
                    elevation=2
                )
            ], spacing=12, scroll=ft.ScrollMode.AUTO),
            padding=15
        )
    
    def create_area_scan_tab(self):
        """Alan tarama tab'ını oluşturur"""
        # Alan seçimi bilgisi
        self.area_info_text = ft.Text(
            "Henüz alan seçilmedi",
            size=14,
            color=ft.Colors.GREY_600
        )
        
        # Alan tarama aralığı
        self.area_scan_interval_input = ft.TextField(
            label="Tarama Aralığı (saniye)",
            value="2.0",
            width=180,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        # Koordinat listeleri
        self.coord_if_found_list_view = ft.ListView(
            height=120,
            spacing=3
        )
        
        self.coord_if_not_found_list_view = ft.ListView(
            height=120,
            spacing=3
        )
        
        # Alan tarama kontrol butonları
        self.area_scan_start_btn = ft.ElevatedButton(
            text="🔍 Alan Taramayı Başlat",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.start_area_scanning,
            style=ft.ButtonStyle(
                bgcolor=self.success_color,
                color=ft.Colors.WHITE,
                elevation=3
            ),
            width=200
        )
        
        self.area_scan_stop_btn = ft.ElevatedButton(
            text="⏹️ Alan Taramayı Durdur",
            icon=ft.Icons.STOP,
            on_click=self.stop_area_scanning,
            style=ft.ButtonStyle(
                bgcolor=self.error_color,
                color=ft.Colors.WHITE,
                elevation=3
            ),
            width=200,
            disabled=True
        )
        
        return ft.Container(
            content=ft.Column([
                # Alan seçimi kartı
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("📐 Tarama Alanı Seçimi", size=16, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            self.area_info_text,
                            
                            # Alan seçim butonları
                            ft.Row([
                                ft.ElevatedButton(
                                    text="🎯 Alan Seç",
                                    icon=ft.Icons.CROP_FREE,
                                    on_click=self.start_area_selection,
                                    style=ft.ButtonStyle(bgcolor=self.primary_color, color=ft.Colors.WHITE),
                                    width=140
                                ),
                                ft.ElevatedButton(
                                    text="🗑️ Temizle",
                                    icon=ft.Icons.CLEAR,
                                    on_click=self.clear_selected_area,
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE),
                                    width=100
                                )
                            ], spacing=10),
                            
                            # Detaylı talimatlar
                            ft.ExpansionTile(
                                title=ft.Text("📝 Alan Seçimi Rehberi", weight=ft.FontWeight.BOLD),
                                subtitle=ft.Text("Tıklayarak talimatları görüntüleyin"),
                                controls=[
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("🎯 NASIL YAPILIR:", weight=ft.FontWeight.BOLD, color=self.primary_color),
                                            ft.Text("1. 'Alan Seç' butonuna tıklayın"),
                                            ft.Text("2. Taramak istediğiniz alanın SOL ÜST köşesine tıklayın"),
                                            ft.Text("3. Aynı alanın SAĞ ALT köşesine tıklayın"),
                                            ft.Text("4. Alan otomatik olarak seçilir ve bilgileri gösterilir"),
                                            ft.Divider(),
                                            ft.Text("💡 İPUÇLARI:", weight=ft.FontWeight.BOLD, color=self.success_color),
                                            ft.Text("• Küçük bir test alanı ile başlayın (100x100 pixel)"),
                                            ft.Text("• Çok büyük alanlar performans sorunu yaratabilir"),
                                            ft.Text("• En az 10x10 pixel boyutunda alan seçin"),
                                            ft.Text("• ESC tuşu ile seçimi iptal edebilirsiniz"),
                                            ft.Divider(),
                                            ft.Text("⚠️ UYARILAR:", weight=ft.FontWeight.BOLD, color=self.warning_color),
                                            ft.Text("• Yanlış alan seçerseniz 'Temizle' ile silebilirsiniz"),
                                            ft.Text("• Seçim sırasında dialog penceresini kapatmayın"),
                                        ], spacing=5),
                                        padding=10
                                    )
                                ]
                            )
                        ], spacing=10),
                        padding=12
                    ),
                    elevation=2
                ),
                
                # Tarama ayarları kartı
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("⚙️ Tarama Ayarları", size=16, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            self.area_scan_interval_input,
                            ft.Text(
                                "Not: Tarama için 'Tek Nokta' sekmesindeki renk listesi kullanılır",
                                size=11,
                                color=ft.Colors.GREY_600,
                                italic=True
                            )
                        ], spacing=10),
                        padding=12
                    ),
                    elevation=2
                ),
                
                # Koordinat listeleri kartı
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("📍 Koordinat Listeleri", size=16, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            
                            # Renk bulundu listesi
                            ft.Row([
                                ft.Text("🎯 Renk Bulunduğunda:", weight=ft.FontWeight.BOLD, size=14, color=self.success_color),
                                ft.ElevatedButton(
                                    text="➕",
                                    on_click=self.add_coordinate_if_found,
                                    style=ft.ButtonStyle(bgcolor=self.success_color, color=ft.Colors.WHITE),
                                    width=40, height=30
                                ),
                                ft.ElevatedButton(
                                    text="🗑️",
                                    on_click=self.remove_coordinate_if_found,
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE),
                                    width=40, height=30
                                )
                            ], spacing=10),
                            self.coord_if_found_list_view,
                            
                            # Renk bulunamadı listesi
                            ft.Row([
                                ft.Text("❌ Renk Bulunamadığında:", weight=ft.FontWeight.BOLD, size=14, color=self.error_color),
                                ft.ElevatedButton(
                                    text="➕",
                                    on_click=self.add_coordinate_if_not_found,
                                    style=ft.ButtonStyle(bgcolor=self.error_color, color=ft.Colors.WHITE),
                                    width=40, height=30
                                ),
                                ft.ElevatedButton(
                                    text="🗑️",
                                    on_click=self.remove_coordinate_if_not_found,
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE),
                                    width=40, height=30
                                )
                            ], spacing=10),
                            self.coord_if_not_found_list_view,
                        ], spacing=10),
                        padding=12
                    ),
                    elevation=2
                ),
                
                # Kontrol kartı
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("🎮 Alan Tarama Kontrolü", size=16, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            ft.Row([self.area_scan_start_btn, self.area_scan_stop_btn], spacing=15, alignment=ft.MainAxisAlignment.CENTER)
                        ], spacing=10),
                        padding=12
                    ),
                    elevation=2
                )
            ], spacing=12, scroll=ft.ScrollMode.AUTO),
            padding=15
        )
    
    def create_help_tab(self):
        """Yardım tab'ını oluşturur"""
        help_content = ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("📖 Kullanım Kılavuzu", size=20, weight=ft.FontWeight.BOLD, color=self.primary_color),
                        
                        ft.Text("🖱️ Tek Nokta Tıklama:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("• Koordinatları manuel olarak girin veya 'Ekrandan Konum Seç' butonunu kullanın"),
                        ft.Text("• Tıklama aralığını ayarlayın"),
                        ft.Text("• İsteğe bağlı olarak renk kontrolü ekleyin"),
                        ft.Text("• 'Başlat' butonuna tıklayın"),
                        
                        ft.Text("📋 Sıralı Tıklama:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("• 'Koordinat Ekle' butonu ile koordinatları ekleyin"),
                        ft.Text("• Tıklama aralığını ayarlayın"),
                        ft.Text("• İsteğe bağlı olarak renk kontrolü etkinleştirin"),
                        ft.Text("• 'Sıralı Tıklamayı Başlat' butonuna tıklayın"),
                        
                        ft.Text("🔍 Alan Tarama:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("• 'Ekrandan Alan Seç' ile taranacak alanı belirleyin"),
                        ft.Text("• 'Tek Nokta' sekmesinde aranacak renkleri ekleyin"),
                        ft.Text("• İki koordinat listesi oluşturun: 'Renk Bulundu' ve 'Renk Bulunamadı'"),
                        ft.Text("• Tarama aralığını ayarlayın"),
                        ft.Text("• 'Alan Taramayı Başlat' butonuna tıklayın"),
                        ft.Text("• Seçilen alanda renk bulunursa 'Renk Bulundu' listesinden sıralı tıklama yapar"),
                        ft.Text("• Renk bulunamazsa 'Renk Bulunamadı' listesinden sıralı tıklama yapar"),
                        
                        ft.Text("🎨 Renk Kontrolü:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("• Renk kontrolü etkinleştirildiğinde, sadece belirtilen renklerde tıklama yapılır"),
                        ft.Text("• 'Ekrandan Renk Seç' ile mouse ile renk seçebilirsiniz"),
                        ft.Text("• 'Manuel Renk Seç' ile renk paleti kullanabilirsiniz"),
                        ft.Text("• Renk toleransı ile benzer renkleri kabul edebilirsiniz"),
                        
                        ft.Text("⌨️ Klavye Kısayolları:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("• Q tuşu: Aktif tıklamayı durdurur"),
                        
                        ft.Text("⚠️ Önemli Notlar:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("• Uygulama çalışırken mouse'u ekranın sol üst köşesine götürürseniz güvenlik nedeniyle durur"),
                        ft.Text("• Koordinat seçimi sırasında mouse'a tıklayın"),
                        ft.Text("• Renk seçimi sırasında istediğiniz rengin üzerine tıklayın")
                    ], spacing=10),
                    padding=20
                ),
                elevation=3
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        return ft.Container(content=help_content, padding=20)
    
    def start_mouse_tracking(self):
        """Mouse pozisyonu takibini başlatır"""
        def update_mouse_position():
            while True:
                try:
                    x, y = pyautogui.position()
                    if hasattr(self, 'mouse_pos_text'):
                        self.mouse_pos_text.value = f"Mevcut Mouse: ({x}, {y})"
                        self.page.update()
                    time.sleep(0.1)
                except:
                    break
        
        mouse_thread = threading.Thread(target=update_mouse_position, daemon=True)
        mouse_thread.start()
    
    def start_position_selection(self, e):
        """Konum seçimini başlatır"""
        self.selecting_position = True
        self.update_status("Ekrandan konum seçmek için mouse ile tıklayın...", self.warning_color)
        
        def on_click(x, y, button, pressed):
            if pressed and self.selecting_position:
                self.click_x = x
                self.click_y = y
                self.x_input.value = str(x)
                self.y_input.value = str(y)
                self.selecting_position = False
                self.update_status(f"Konum seçildi: ({x}, {y})", self.success_color)
                self.page.update()
                return False  # Listener'ı durdur
        
        self.mouse_listener = MouseListener(on_click=on_click)
        self.mouse_listener.start()
    
    def start_color_selection(self, e):
        """Renk seçimini başlatır"""
        self.selecting_color = True
        self.update_status("Ekrandan renk seçmek için mouse ile tıklayın...", self.warning_color)
        
        def on_click(x, y, button, pressed):
            if pressed and self.selecting_color:
                color = self.get_pixel_color(x, y)
                if color:
                    self.add_color_to_list(color)
                    self.update_status(f"Renk seçildi: RGB{color}", self.success_color)
                else:
                    self.update_status("Renk seçilemedi!", self.error_color)
                self.selecting_color = False
                self.page.update()
                return False
        
        self.mouse_listener = MouseListener(on_click=on_click)
        self.mouse_listener.start()
    
    def manual_color_selection(self, e):
        """Manuel renk seçimi dialog'unu açar"""
        # Flet'te color picker henüz mevcut değil, bu yüzden RGB girişi kullanacağız
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        def add_color(e):
            try:
                r = int(r_field.value or "0")
                g = int(g_field.value or "0")
                b = int(b_field.value or "0")
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                    self.add_color_to_list((r, g, b))
                    self.update_status(f"Renk eklendi: RGB({r}, {g}, {b})", self.success_color)
                    close_dialog(e)
                else:
                    self.update_status("RGB değerleri 0-255 arasında olmalıdır!", self.error_color)
            except ValueError:
                self.update_status("Geçerli sayısal değerler girin!", self.error_color)
        
        r_field = ft.TextField(label="Kırmızı (0-255)", width=150, keyboard_type=ft.KeyboardType.NUMBER)
        g_field = ft.TextField(label="Yeşil (0-255)", width=150, keyboard_type=ft.KeyboardType.NUMBER)
        b_field = ft.TextField(label="Mavi (0-255)", width=150, keyboard_type=ft.KeyboardType.NUMBER)
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Manuel Renk Seçimi"),
            content=ft.Column([
                ft.Text("RGB değerlerini girin:"),
                ft.Row([r_field, g_field, b_field], spacing=10)
            ], height=150),
            actions=[
                ft.TextButton("İptal", on_click=close_dialog),
                ft.ElevatedButton("Ekle", on_click=add_color)
            ]
        )
        
        self.page.open(dialog)
    
    def get_pixel_color(self, x, y):
        """Belirtilen koordinattaki pixel rengini alır"""
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            pixel_color = screenshot.getpixel((0, 0))
            return pixel_color[:3]
        except Exception:
            return None
    
    def add_color_to_list(self, color: Tuple[int, int, int]):
        """Rengi listeye ekler"""
        if color not in self.color_list:
            self.color_list.append(color)
            self.update_color_list_display()
    
    def update_color_list_display(self):
        """Renk listesi görünümünü günceller"""
        self.color_list_view.controls.clear()
        for i, (r, g, b) in enumerate(self.color_list):
            color_item = ft.Container(
                content=ft.Text(
                    f"Renk {i+1}: RGB({r}, {g}, {b})",
                    color=ft.Colors.WHITE if (r * 0.299 + g * 0.587 + b * 0.114) < 128 else ft.Colors.BLACK,
                    weight=ft.FontWeight.BOLD
                ),
                bgcolor=f"rgb({r}, {g}, {b})",
                padding=10,
                border_radius=5,
                on_click=lambda e, idx=i: self.select_color_item(idx)
            )
            self.color_list_view.controls.append(color_item)
        self.page.update()
    
    def select_color_item(self, index):
        """Renk öğesini seçer"""
        self.selected_color_index = index
    
    def remove_selected_color(self, e):
        """Seçili rengi listeden siler"""
        if hasattr(self, 'selected_color_index') and 0 <= self.selected_color_index < len(self.color_list):
            del self.color_list[self.selected_color_index]
            self.update_color_list_display()
            self.update_status("Seçili renk silindi", self.success_color)
        else:
            self.update_status("Silinecek renk seçin", self.warning_color)
    
    def clear_all_colors(self, e):
        """Tüm renkleri temizler"""
        self.color_list.clear()
        self.update_color_list_display()
        self.update_status("Tüm renkler temizlendi", self.success_color)
    
    def toggle_color_check(self, e):
        """Renk kontrolünü açar/kapatır"""
        self.color_check_enabled = e.control.value
    
    def update_color_tolerance(self, e):
        """Renk toleransını günceller"""
        self.color_tolerance = int(e.control.value or "0")
    
    def add_coordinate_from_screen(self, e):
        """Ekrandan koordinat ekler"""
        self.adding_coordinate = True
        self.update_status("Koordinat eklemek için ekrandan bir nokta seçin...", self.warning_color)
        
        def on_click(x, y, button, pressed):
            if pressed and self.adding_coordinate:
                coord = {'x': x, 'y': y}
                self.coordinates_list.append(coord)
                self.update_coordinate_list_display()
                self.adding_coordinate = False
                self.update_status(f"Koordinat eklendi: ({x}, {y})", self.success_color)
                self.page.update()
                return False
        
        self.mouse_listener = MouseListener(on_click=on_click)
        self.mouse_listener.start()
    
    def update_coordinate_list_display(self):
        """Koordinat listesi görünümünü günceller"""
        self.coord_list_view.controls.clear()
        for i, coord in enumerate(self.coordinates_list):
            coord_item = ft.Container(
                content=ft.Text(
                    f"Koordinat {i+1}: ({coord['x']}, {coord['y']})",
                    weight=ft.FontWeight.BOLD
                ),
                bgcolor=ft.Colors.BLUE_50,
                padding=10,
                border_radius=5,
                border=ft.border.all(1, ft.Colors.BLUE_200),
                on_click=lambda e, idx=i: self.select_coordinate_item(idx)
            )
            self.coord_list_view.controls.append(coord_item)
        self.page.update()
    
    def select_coordinate_item(self, index):
        """Koordinat öğesini seçer"""
        self.selected_coordinate_index = index
    
    def remove_selected_coordinate(self, e):
        """Seçili koordinatı listeden siler"""
        if hasattr(self, 'selected_coordinate_index') and 0 <= self.selected_coordinate_index < len(self.coordinates_list):
            del self.coordinates_list[self.selected_coordinate_index]
            self.update_coordinate_list_display()
            self.update_status("Seçili koordinat silindi", self.success_color)
        else:
            self.update_status("Silinecek koordinat seçin", self.warning_color)
    
    def clear_all_coordinates(self, e):
        """Tüm koordinatları temizler"""
        self.coordinates_list.clear()
        self.update_coordinate_list_display()
        self.update_status("Tüm koordinatlar temizlendi", self.success_color)
    
    def start_clicking(self, e):
        """Tek nokta tıklamayı başlatır"""
        try:
            self.click_x = int(self.x_input.value or "0")
            self.click_y = int(self.y_input.value or "0")
            self.click_interval = float(self.interval_input.value or "0.0")
        except ValueError:
            self.update_status("Geçerli sayısal değerler girin!", self.error_color)
            return
        
        if self.click_x == 0 and self.click_y == 0:
            self.update_status("Önce bir konum seçin!", self.warning_color)
            return
        
        if self.click_interval <= 0:
            self.update_status("Tıklama aralığı 0'dan büyük olmalıdır!", self.error_color)
            return
        
        coordinate_color = None
        if self.color_check_enabled and self.color_list:
            coordinate_color = self.color_list[0]
        
        self.is_clicking = True
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        
        status_msg = "Renk kontrollü tıklama aktif" if coordinate_color else "Tıklama aktif"
        self.update_status(f"{status_msg} - Durdurmak için 'Q' tuşuna basın", self.error_color)
        
        self.click_thread = ClickingThread(
            self.click_x, self.click_y, self.click_interval,
            coordinate_color, self.color_tolerance,
            self.update_status_from_thread
        )
        self.click_thread.start()
        self.page.update()
    
    def stop_clicking(self, e):
        """Tek nokta tıklamayı durdurur"""
        self.is_clicking = False
        if self.click_thread:
            self.click_thread.stop()
        
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.update_status("Tıklama durduruldu", self.primary_color)
        self.page.update()
    
    def start_sequential_clicking(self, e):
        """Sıralı tıklamayı başlatır"""
        try:
            interval = float(self.seq_interval_input.value or "0.0")
        except ValueError:
            self.update_status("Geçerli bir sayısal değer girin!", self.error_color)
            return
        
        if not self.coordinates_list:
            self.update_status("Önce koordinat listesi oluşturun!", self.warning_color)
            return
        
        if interval <= 0:
            self.update_status("Tıklama aralığı 0'dan büyük olmalıdır!", self.error_color)
            return
        
        if self.seq_color_check_switch.value and not self.color_list:
            self.update_status("Renk kontrolü etkin ancak renk listesi boş!", self.warning_color)
            return
        
        self.is_sequential_clicking = True
        self.seq_start_btn.disabled = True
        self.seq_stop_btn.disabled = False
        
        status_msg = "Sıralı renk kontrollü tıklama aktif" if self.seq_color_check_switch.value else "Sıralı tıklama aktif"
        self.update_status(f"{status_msg} - Durdurmak için 'Q' tuşuna basın", self.error_color)
        
        color_list = self.color_list.copy() if self.seq_color_check_switch.value else None
        self.sequential_thread = SequentialClickingThread(
            self.coordinates_list.copy(), interval, self.color_tolerance,
            color_list, self.update_status_from_thread
        )
        self.sequential_thread.start()
        self.page.update()
    
    def stop_sequential_clicking(self, e):
        """Sıralı tıklamayı durdurur"""
        self.is_sequential_clicking = False
        if self.sequential_thread:
            self.sequential_thread.stop()
        
        self.seq_start_btn.disabled = False
        self.seq_stop_btn.disabled = True
        self.update_status("Sıralı tıklama durduruldu", self.primary_color)
        self.page.update()
    
    def update_status(self, message, color=None):
        """Durum mesajını günceller"""
        self.status_text.value = message
        if color:
            self.status_text.color = color
        self.page.update()
    
    def update_status_from_thread(self, message):
        """Thread'den gelen durum mesajını günceller"""
        def update():
            self.status_text.value = message
            self.page.update()
        
        # Thread-safe update
        self.page.run_thread(update)
    
    def on_key_press(self, key):
        """Klavye tuşu basıldığında çalışır"""
        try:
            if key.char == 'q' or key.char == 'Q':
                if self.is_clicking:
                    self.stop_clicking(None)
                elif self.is_sequential_clicking:
                    self.stop_sequential_clicking(None)
                elif self.is_area_scanning:
                    self.stop_area_scanning(None)
        except AttributeError:
            # Özel tuşlar (ESC, CTRL, vb.)
            if key == keyboard.Key.esc:
                if self.selecting_area:
                    self.selecting_area = False
                    if hasattr(self, 'area_dialog') and self.area_dialog.open:
                        self.area_dialog.open = False
                    if self.mouse_listener:
                        self.mouse_listener.stop()
                    self.update_status("Alan seçimi ESC tuşu ile iptal edildi", self.primary_color)
                    self.page.update()
    
    def exit_app(self, e):
        """Uygulamayı güvenli şekilde kapatır"""
        self.page.window.close()
      
    
    def start_area_selection(self, e):
        """Alan seçimini başlatır (iki nokta ile dikdörtgen) - İyileştirilmiş versiyon"""
        self.selecting_area = True
        self.area_start_point = None
        
        # Seçim talimatlarını göster
        instructions = """
🎯 ALAN SEÇİMİ BAŞLATILIYOR:

1️⃣ İlk tıklama: Taramak istediğiniz alanın SOL ÜST köşesine tıklayın
2️⃣ İkinci tıklama: Aynı alanın SAĞ ALT köşesine tıklayın

💡 İpucu: Küçük bir test alanı seçerek başlayın (örn: 100x100 pixel)
❌ İptal etmek için ESC tuşuna basın
        """
        
        self.update_status(instructions, self.warning_color)
        
        # Alan seçimi dialog'u göster
        self.show_area_selection_dialog()
        
        def on_click(x, y, button, pressed):
            if pressed and self.selecting_area:
                if self.area_start_point is None:
                    # İlk tıklama - başlangıç noktası
                    self.area_start_point = (x, y)
                    msg = f"✅ BAŞLANGIÇ NOKTASI: ({x}, {y})\n\nŞimdi alanın SAĞ ALT köşesine tıklayın..."
                    self.update_status(msg, self.warning_color)
                    if hasattr(self, 'area_dialog'):
                        self.area_dialog_text.value = f"Başlangıç: ({x}, {y})\nBitmek için sağ alt köşeye tıklayın..."
                        self.page.update()
                else:
                    # İkinci tıklama - bitiş noktası
                    x1, y1 = self.area_start_point
                    x2, y2 = x, y
                    
                    # Koordinatları düzenle (küçük -> büyük)
                    if x1 > x2:
                        x1, x2 = x2, x1
                    if y1 > y2:
                        y1, y2 = y2, y1
                    
                    # Alan boyutunu kontrol et
                    width = x2 - x1
                    height = y2 - y1
                    
                    if width < 10 or height < 10:
                        self.update_status("❌ Alan çok küçük! En az 10x10 pixel seçin.", self.error_color)
                        self.area_start_point = None
                        return True  # Seçime devam et
                    
                    if width > 1000 or height > 1000:
                        self.update_status("⚠️ Uyarı: Çok büyük alan seçtiniz. Performans sorunu yaşayabilirsiniz.", self.warning_color)
                    
                    # Alanı kaydet
                    self.scan_area = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
                    
                    # Alan önizlemesi oluştur
                    self.create_area_preview()
                    
                    # Bilgileri güncelle
                    area_info = f"""
🎯 ALAN SEÇİLDİ:
📍 Koordinatlar: ({x1}, {y1}) → ({x2}, {y2})
📏 Boyut: {width} x {height} pixel
📐 Toplam Alan: {width * height:,} pixel
                    """
                    
                    self.area_info_text.value = area_info
                    self.area_info_text.color = self.success_color
                    
                    # Dialog'u kapat
                    if hasattr(self, 'area_dialog'):
                        self.area_dialog.open = False
                    
                    self.selecting_area = False
                    self.area_start_point = None
                    self.update_status(f"✅ Alan başarıyla seçildi! Boyut: {width}x{height}", self.success_color)
                    self.page.update()
                    return False
        
        self.mouse_listener = MouseListener(on_click=on_click)
        self.mouse_listener.start()
    
    def show_area_selection_dialog(self):
        """Alan seçimi sırasında yardımcı dialog gösterir"""
        def close_dialog(e):
            self.area_dialog.open = False
            self.selecting_area = False
            if self.mouse_listener:
                self.mouse_listener.stop()
            self.update_status("Alan seçimi iptal edildi", self.primary_color)
            self.page.update()
        
        self.area_dialog_text = ft.Text(
            "Alan seçimi başlatıldı...\nLütfen sol üst köşeye tıklayın",
            size=14,
            weight=ft.FontWeight.BOLD
        )
        
        self.area_dialog = ft.AlertDialog(
            modal=False,
            title=ft.Text("🎯 Alan Seçimi Rehberi"),
            content=ft.Container(
                content=ft.Column([
                    self.area_dialog_text,
                    ft.Divider(),
                    ft.Text("📝 Adımlar:", weight=ft.FontWeight.BOLD),
                    ft.Text("1. Sol üst köşeye tıklayın"),
                    ft.Text("2. Sağ alt köşeye tıklayın"),
                    ft.Text("3. Alan otomatik seçilecek"),
                    ft.Divider(),
                    ft.Text("💡 En az 10x10 pixel seçin", size=12, italic=True),
                ], spacing=5),
                width=300,
                height=200
            ),
            actions=[
                ft.TextButton("❌ İptal Et", on_click=close_dialog)
            ]
        )
        
        self.page.open(self.area_dialog)
    
    def create_area_preview(self):
        """Seçilen alanın önizlemesini oluşturur"""
        if not self.scan_area:
            return
        
        try:
            x1, y1 = self.scan_area['x1'], self.scan_area['y1']
            x2, y2 = self.scan_area['x2'], self.scan_area['y2']
            
            # Seçilen alanın screenshot'ını al
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            
            # Küçük boyuta ölçekle (maksimum 200x150)
            original_width, original_height = screenshot.size
            max_width, max_height = 200, 150
            
            if original_width > max_width or original_height > max_height:
                ratio = min(max_width / original_width, max_height / original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                screenshot = screenshot.resize((new_width, new_height))
            
            # Flet için base64 formatına dönüştür (opsiyonel - şimdilik sadece boyut bilgisi)
            self.area_preview_info = f"Önizleme: {screenshot.size[0]}x{screenshot.size[1]} (Orijinal: {original_width}x{original_height})"
            
        except Exception as e:
            self.area_preview_info = f"Önizleme oluşturulamadı: {str(e)}"
    
    def clear_selected_area(self, e):
        """Seçilen alanı temizler"""
        self.scan_area = None
        self.area_info_text.value = "Henüz alan seçilmedi"
        self.area_info_text.color = ft.Colors.GREY_600
        self.update_status("Seçilen alan temizlendi", self.primary_color)
        self.page.update()
    
    def add_coordinate_if_found(self, e):
        """Renk bulunduğunda koordinat ekler"""
        self.adding_coordinate = True
        self.update_status("'Renk Bulundu' listesi için koordinat seçin...", self.warning_color)
        
        def on_click(x, y, button, pressed):
            if pressed and self.adding_coordinate:
                coord = {'x': x, 'y': y}
                self.coordinates_if_found.append(coord)
                self.update_coordinate_if_found_display()
                self.adding_coordinate = False
                self.update_status(f"'Renk Bulundu' listesine koordinat eklendi: ({x}, {y})", self.success_color)
                self.page.update()
                return False
        
        self.mouse_listener = MouseListener(on_click=on_click)
        self.mouse_listener.start()
    
    def add_coordinate_if_not_found(self, e):
        """Renk bulunamadığında koordinat ekler"""
        self.adding_coordinate = True
        self.update_status("'Renk Bulunamadı' listesi için koordinat seçin...", self.warning_color)
        
        def on_click(x, y, button, pressed):
            if pressed and self.adding_coordinate:
                coord = {'x': x, 'y': y}
                self.coordinates_if_not_found.append(coord)
                self.update_coordinate_if_not_found_display()
                self.adding_coordinate = False
                self.update_status(f"'Renk Bulunamadı' listesine koordinat eklendi: ({x}, {y})", self.success_color)
                self.page.update()
                return False
        
        self.mouse_listener = MouseListener(on_click=on_click)
        self.mouse_listener.start()
    
    def update_coordinate_if_found_display(self):
        """'Renk Bulundu' koordinat listesi görünümünü günceller"""
        self.coord_if_found_list_view.controls.clear()
        for i, coord in enumerate(self.coordinates_if_found):
            coord_item = ft.Container(
                content=ft.Text(
                    f"Koordinat {i+1}: ({coord['x']}, {coord['y']})",
                    weight=ft.FontWeight.BOLD
                ),
                bgcolor=ft.Colors.GREEN_50,
                padding=8,
                border_radius=5,
                border=ft.border.all(1, ft.Colors.GREEN_200),
                on_click=lambda e, idx=i: self.select_coordinate_if_found_item(idx)
            )
            self.coord_if_found_list_view.controls.append(coord_item)
        self.page.update()
    
    def update_coordinate_if_not_found_display(self):
        """'Renk Bulunamadı' koordinat listesi görünümünü günceller"""
        self.coord_if_not_found_list_view.controls.clear()
        for i, coord in enumerate(self.coordinates_if_not_found):
            coord_item = ft.Container(
                content=ft.Text(
                    f"Koordinat {i+1}: ({coord['x']}, {coord['y']})",
                    weight=ft.FontWeight.BOLD
                ),
                bgcolor=ft.Colors.RED_50,
                padding=8,
                border_radius=5,
                border=ft.border.all(1, ft.Colors.RED_200),
                on_click=lambda e, idx=i: self.select_coordinate_if_not_found_item(idx)
            )
            self.coord_if_not_found_list_view.controls.append(coord_item)
        self.page.update()
    
    def select_coordinate_if_found_item(self, index):
        """'Renk Bulundu' koordinat öğesini seçer"""
        self.selected_coordinate_if_found_index = index
    
    def select_coordinate_if_not_found_item(self, index):
        """'Renk Bulunamadı' koordinat öğesini seçer"""
        self.selected_coordinate_if_not_found_index = index
    
    def remove_coordinate_if_found(self, e):
        """'Renk Bulundu' listesinden seçili koordinatı siler"""
        if hasattr(self, 'selected_coordinate_if_found_index') and 0 <= self.selected_coordinate_if_found_index < len(self.coordinates_if_found):
            del self.coordinates_if_found[self.selected_coordinate_if_found_index]
            self.update_coordinate_if_found_display()
            self.update_status("'Renk Bulundu' listesinden koordinat silindi", self.success_color)
        else:
            self.update_status("'Renk Bulundu' listesinden silinecek koordinat seçin", self.warning_color)
    
    def remove_coordinate_if_not_found(self, e):
        """'Renk Bulunamadı' listesinden seçili koordinatı siler"""
        if hasattr(self, 'selected_coordinate_if_not_found_index') and 0 <= self.selected_coordinate_if_not_found_index < len(self.coordinates_if_not_found):
            del self.coordinates_if_not_found[self.selected_coordinate_if_not_found_index]
            self.update_coordinate_if_not_found_display()
            self.update_status("'Renk Bulunamadı' listesinden koordinat silindi", self.success_color)
        else:
            self.update_status("'Renk Bulunamadı' listesinden silinecek koordinat seçin", self.warning_color)
    
    def start_area_scanning(self, e):
        """Alan taramayı başlatır"""
        try:
            interval = float(self.area_scan_interval_input.value or "0.0")
        except ValueError:
            self.update_status("Geçerli bir sayısal değer girin!", self.error_color)
            return
        
        if not self.scan_area:
            self.update_status("Önce bir alan seçin!", self.warning_color)
            return
        
        if not self.color_list:
            self.update_status("Önce 'Tek Nokta' sekmesinde en az bir renk seçin!", self.warning_color)
            return
        
        if interval <= 0:
            self.update_status("Tarama aralığı 0'dan büyük olmalıdır!", self.error_color)
            return
        
        if not self.coordinates_if_found and not self.coordinates_if_not_found:
            self.update_status("En az bir koordinat listesi oluşturun!", self.warning_color)
            return
        
        self.is_area_scanning = True
        self.area_scan_start_btn.disabled = True
        self.area_scan_stop_btn.disabled = False
        
        self.update_status("🔍 Alan tarama aktif - Durdurmak için 'Q' tuşuna basın", self.error_color)
        
        self.area_scan_thread = AreaScanThread(
            self.scan_area,
            self.color_list.copy(),
            self.coordinates_if_found.copy(),
            self.coordinates_if_not_found.copy(),
            interval,
            self.color_tolerance,
            self.update_status_from_thread
        )
        self.area_scan_thread.start()
        self.page.update()
    
    def stop_area_scanning(self, e):
        """Alan taramayı durdurur"""
        self.is_area_scanning = False
        if self.area_scan_thread:
            self.area_scan_thread.stop()
        
        self.area_scan_start_btn.disabled = False
        self.area_scan_stop_btn.disabled = True
        self.update_status("Alan tarama durduruldu", self.primary_color)
        self.page.update()
    
    def cleanup(self):
        """Temizlik işlemleri"""
        self.is_clicking = False
        self.is_sequential_clicking = False
        self.is_area_scanning = False
        if self.click_thread:
            self.click_thread.stop()
        if self.sequential_thread:
            self.sequential_thread.stop()
        if self.area_scan_thread:
            self.area_scan_thread.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()

def main(page: ft.Page):
    # PyAutoGUI güvenlik ayarları
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    app = AutoClickerApp(page)
    
    def on_window_event(e):
        if e.data == "close":
            app.cleanup()
            page.window.destroy()
    
    page.window.prevent_close = True
    page.window.on_event = on_window_event

if __name__ == "__main__":
    ft.app(target=main)