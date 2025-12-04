"""
Основной класс конвертера для преобразования изображений в JPG с графическим интерфейсом.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from PIL import Image
import threading
import sys
try:
    from ttkthemes import ThemedStyle
    HAS_TTKTHEMES = True
except ImportError:
    HAS_TTKTHEMES = False
    ThemedStyle = None


class PNGtoJPGConverter:
    """
    Графическое приложение для преобразования изображений в формат JPG.
    """
    
    def __init__(self):
        """Инициализирует приложение конвертера."""
        self.root = tk.Tk()
        self.root.title("PNG to JPG Converter")
        self.root.geometry("700x500")
        
        # Определение системной темы
        self.system_theme = self._detect_system_theme()
        # Используем светлую тему по умолчанию, если не удалось определить
        self.current_theme = self.system_theme if self.system_theme in ["light", "dark"] else "light"
        
        # Загрузка настроек из файла
        self.load_settings()
        
        self.setup_ui()
        
        # После настройки UI установим значения из настроек
        self.update_ui_with_settings()
        
        # Применяем текущую тему
        self._apply_theme()
    
    def _detect_system_theme(self):
        """
        Определяет системную тему (светлая или темная).
        Возвращает 'light' или 'dark' в зависимости от системной настройки.
        """
        # Для разных операционных систем используем разные методы
        if sys.platform == "darwin":  # macOS
            try:
                import subprocess
                result = subprocess.run(
                    ["defaults", "read", "-g", "AppleInterfaceStyle"],
                    capture_output=True,
                    text=True
                )
                return "dark" if result.stdout.strip() == "Dark" else "light"
            except:
                return "light"
        elif sys.platform.startswith("win"):  # Windows
            try:
                import winreg
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return "dark" if value == 0 else "light"
            except:
                return "light"
        else:  # Linux и другие
            # Проверяем переменные окружения, которые могут указывать на тему
            desktop_session = os.environ.get("XDG_CURRENT_DESKTOP", "")
            
            # Проверяем различные настройки темы для Linux
            if "GNOME" in desktop_session.upper():
                try:
                    import subprocess
                    result = subprocess.run(
                        ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
                        capture_output=True,
                        text=True
                    )
                    if "dark" in result.stdout.lower():
                        return "dark"
                    else:
                        return "light"
                except:
                    pass
            
            # Проверяем другие возможные индикаторы темной темы
            if os.environ.get("GTK_THEME", "").lower().find("dark") != -1:
                return "dark"
                
            # Проверяем переменную COLORFGBG (часто используется в терминалах)
            colorfgbg = os.environ.get("COLORFGBG", "")
            if colorfgbg.startswith("0;") or colorfgbg.startswith("1;"):
                # Это может указывать на темную тему
                return "dark"
            
            # В противном случае используем светлую тему по умолчанию
            return "light"
    
    def _apply_theme(self):
        """Применяет текущую тему к интерфейсу приложения."""
        if self.current_theme == "dark":
            self._apply_dark_theme()
        else:
            self._apply_light_theme()
    
    def _apply_dark_theme(self):
        """Применяет темную тему к интерфейсу приложения."""
        if HAS_TTKTHEMES and ThemedStyle:
            # Используем ThemedStyle для более продвинутой темной темы
            style = ThemedStyle(self.root)
            # Пытаемся использовать тему, которая поддерживает темный режим
            try:
                style.set_theme("equilux")  # Темная тема из ttkthemes
            except:
                # Если тема недоступна, используем стандартные настройки
                style = ttk.Style()
                style.theme_use('clam')
        else:
            # Если ttkthemes недоступна, используем стандартные настройки
            style = ttk.Style()
            style.theme_use('clam')
        
        bg_color = "#2d2d2d"
        fg_color = "#ffffff"
        button_bg = "#4a4a4a"
        entry_bg = "#3d3d3d"
        entry_fg = "#ffffff"
        
        # Обновляем цвета для основного окна
        self.root.configure(bg=bg_color)
        
        # Настройка стилей для различных элементов
        if HAS_TTKTHEMES and ThemedStyle and isinstance(style, ThemedStyle):
            # Для ThemedStyle используем специфические темы
            pass
        else:
            # Настройка стилей для ttk.Style
            style.configure("TFrame", background=bg_color)
            style.configure("TLabel", background=bg_color, foreground=fg_color)
            style.configure("TButton", background=button_bg, foreground=fg_color)
            style.configure("TEntry", fieldbackground=entry_bg, foreground=entry_fg)
            style.configure("TCheckbutton", background=bg_color, foreground=fg_color)
            style.configure("TSpinbox", fieldbackground=entry_bg, foreground=entry_fg)
            style.configure("TProgressbar", background=button_bg)
            style.map("TButton", background=[('active', '#6a6a6a')])
        
        # Для LabelFrame нужно отдельное оформление
        if hasattr(self, 'root'):
            self._update_widget_colors(self.root, bg_color, fg_color)
    
    def _apply_light_theme(self):
        """Применяет светлую тему к интерфейсу приложения."""
        if HAS_TTKTHEMES and ThemedStyle:
            # Используем ThemedStyle для более продвинутой светлой темы
            style = ThemedStyle(self.root)
            # Пытаемся использовать светлую тему из ttkthemes
            try:
                style.set_theme("clearlooks")  # Светлая тема из ttkthemes
            except:
                # Если тема недоступна, используем стандартные настройки
                style = ttk.Style()
                style.theme_use('default')
        else:
            # Если ttkthemes недоступна, используем стандартные настройки
            style = ttk.Style()
            style.theme_use('default')
        
        # Используем стандартные светлые цвета
        bg_color = "#f0f0f0"
        fg_color = "#000000"
        
        # Обновляем цвета для основного окна
        self.root.configure(bg=bg_color)
        
        # Для LabelFrame нужно отдельное оформление
        if hasattr(self, 'root'):
            self._update_widget_colors(self.root, bg_color, fg_color)
    
    def _update_widget_colors(self, widget, bg_color, fg_color):
        """Рекурсивно обновляет цвета для всех виджетов."""
        # Устанавливаем цвет фона для виджета
        try:
            widget.configure(bg=bg_color)
        except tk.TclError:
            pass  # Некоторые виджеты не поддерживают изменение цвета фона
        
        # Для виджетов Entry и Text устанавливаем специальные цвета
        if isinstance(widget, tk.Entry):
            try:
                widget.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")
            except tk.TclError:
                pass
        elif isinstance(widget, tk.Text):
            try:
                widget.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")
            except tk.TclError:
                pass
        elif isinstance(widget, tk.Label):
            try:
                widget.configure(bg=bg_color, fg=fg_color)
            except tk.TclError:
                pass
        
        # Рекурсивно обновляем цвета для дочерних виджетов
        for child in widget.winfo_children():
            self._update_widget_colors(child, bg_color, fg_color)
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса."""
        # Основная рамка
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Конвертер изображений в JPG", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Раздел выбора папок
        input_frame = ttk.LabelFrame(main_frame, text="Входная папка", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(input_frame, text="Входная папка:").grid(row=0, column=0, sticky=tk.W)
        
        self.input_entry = ttk.Entry(input_frame, width=50)
        self.input_entry.grid(row=0, column=1, padx=(5, 5))
        
        input_browse_button = ttk.Button(input_frame, text="Обзор", command=self.browse_input)
        input_browse_button.grid(row=0, column=2)
        
        # Раздел выходной директории
        output_frame = ttk.LabelFrame(main_frame, text="Настройки вывода", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(output_frame, text="Выходная директория:").grid(row=0, column=0, sticky=tk.W)
        
        self.output_entry = ttk.Entry(output_frame, width=50)
        self.output_entry.grid(row=0, column=1, padx=(5, 5))
        
        browse_button = ttk.Button(output_frame, text="Обзор", command=self.browse_output)
        browse_button.grid(row=0, column=2)
        
        # Настройка качества
        ttk.Label(output_frame, text="Качество JPG (1-100):").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        self.quality_var = tk.StringVar(value=str(self.quality))
        quality_spinbox = ttk.Spinbox(output_frame, from_=1, to=100, textvariable=self.quality_var, width=10)
        quality_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 0))
        quality_spinbox.bind('<FocusOut>', self.on_quality_changed)
        quality_spinbox.bind('<KeyRelease>', self.on_quality_key_release)
        
        # Настройки разрешения
        resolution_frame = ttk.LabelFrame(output_frame, text="Настройки разрешения", padding="5")
        resolution_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Выпадающий список с пресетами разрешений
        ttk.Label(resolution_frame, text="Пресет разрешения:").grid(row=0, column=0, sticky=tk.W)
        self.resolution_preset_var = tk.StringVar()
        self.resolution_preset_var.set("Без изменения")  # Значение по умолчанию
        resolution_presets = [
            "Без изменения",
            "1920x1080 (Full HD)",
            "1280x720 (HD)",
            "3840x2160 (4K)",
            "2560x1440 (QHD)",
            "1366x768",
            "1024x768",
            "800x600"
        ]
        self.resolution_preset_combo = ttk.Combobox(
            resolution_frame,
            textvariable=self.resolution_preset_var,
            values=resolution_presets,
            state="readonly",
            width=20
        )
        self.resolution_preset_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 10))
        self.resolution_preset_combo.bind("<<ComboboxSelected>>", self.on_preset_selected)
        
        ttk.Label(resolution_frame, text="Ширина:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.width_var = tk.StringVar(value="0")
        width_spinbox = ttk.Spinbox(resolution_frame, from_=0, to=10000, textvariable=self.width_var, width=10)
        width_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(5, 10), pady=(10, 0))
        width_spinbox.bind('<FocusOut>', self.on_resolution_changed)
        width_spinbox.bind('<KeyRelease>', self.on_resolution_key_release)
        
        ttk.Label(resolution_frame, text="Высота:").grid(row=1, column=2, sticky=tk.W, pady=(10, 0))
        self.height_var = tk.StringVar(value="0")
        height_spinbox = ttk.Spinbox(resolution_frame, from_=0, to=1000, textvariable=self.height_var, width=10)
        height_spinbox.grid(row=1, column=3, sticky=tk.W, padx=(5, 0), pady=(10, 0))
        height_spinbox.bind('<FocusOut>', self.on_resolution_changed)
        height_spinbox.bind('<KeyRelease>', self.on_resolution_key_release)
        
        self.aspect_ratio_var = tk.BooleanVar(value=self.preserve_aspect_ratio)
        aspect_ratio_check = ttk.Checkbutton(resolution_frame, text="Сохранить соотношение сторон", variable=self.aspect_ratio_var)
        aspect_ratio_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        aspect_ratio_check.config(command=self.on_aspect_ratio_changed)
        
        # Кнопка преобразования
        self.convert_button = ttk.Button(main_frame, text="Преобразовать в JPG", command=self.start_conversion)
        self.convert_button.grid(row=3, column=0, columnspan=3, pady=(20, 0))
        
        # Индикатор прогресса
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Статусная строка
        self.status_var = tk.StringVar()
        self.status_var.set("Готов")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Добавляем переключатель темы
        theme_frame = ttk.Frame(main_frame)
        theme_frame.grid(row=6, column=0, columnspan=3, pady=(10, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(theme_frame, text="Тема:").grid(row=0, column=0, sticky=tk.W)
        
        self.theme_var = tk.StringVar(value=self.theme_preference)
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=["system", "light", "dark"],
            state="readonly",
            width=15
        )
        theme_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        theme_combo.bind("<<ComboboxSelected>>", self.on_theme_changed)
        
        # Настройка весов сетки
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(0, weight=1)
        output_frame.columnconfigure(1, weight=1)
    
    # Удаляем дублирующийся метод setup_ui
    
    def browse_input(self):
        """Поиск входной директории."""
        directory = filedialog.askdirectory(title="Выберите входную папку с изображениями")
        if directory:
            self.input_dir = directory
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, directory)
    
    def browse_output(self):
        """Поиск выходной директории."""
        directory = filedialog.askdirectory(title="Выберите выходную директорию")
        if directory:
            self.output_dir = directory
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, directory)
    
    def convert_files(self):
        """Выполняет фактическое преобразование в отдельном потоке."""
        if not self.input_dir or not os.path.isdir(self.input_dir):
            messagebox.showwarning("Нет входной папки", "Пожалуйста, выберите входную папку с изображениями.")
            return
        
        if not self.output_dir or not os.path.isdir(self.output_dir):
            messagebox.showwarning("Нет выходной директории", "Пожалуйста, выберите выходную директорию.")
            return
        
        try:
            self.quality = int(self.quality_var.get())
            if not 1 <= self.quality <= 100:
                raise ValueError("Качество должно быть между 1 и 100")
            
            # Сохраняем настройки качества
            self.save_settings()
        except ValueError:
            messagebox.showerror("Неверное качество", "Пожалуйста, введите допустимое значение качества (1-100).")
            return
        
        try:
            self.target_width = int(self.width_var.get())
            self.target_height = int(self.height_var.get())
            self.preserve_aspect_ratio = self.aspect_ratio_var.get()
            
            # Проверка, что по крайней мере одна размерность указана, если требуется изменение разрешения
            if (self.target_width > 0 or self.target_height > 0) and (self.target_width == 0 and self.target_height == 0):
                raise ValueError("Ширина и высота не могут быть нулевыми при желании изменения размера")
            
            # Сохраняем настройки разрешения
            self.save_settings()
        except ValueError as e:
            if "Ширина и высота не могут быть нулевыми" in str(e):
                messagebox.showerror("Неверное разрешение", str(e))
            else:
                messagebox.showerror("Неверное разрешение", "Пожалуйста, введите допустимые значения ширины и высоты.")
            return
        
        # Получаем список всех поддерживаемых файлов изображений из входной папки
        supported_extensions = ['.png', '.webp', '.bmp', '.gif']
        image_files = [f for f in os.listdir(self.input_dir)
                      if f.lower().endswith(tuple(supported_extensions))]
        
        if not image_files:
            messagebox.showwarning("Нет файлов изображений",
                                 f"В выбранной папке нет файлов с поддерживаемыми форматами ({', '.join(supported_extensions)}).")
            return

        self.convert_button.config(state='disabled')
        self.progress['value'] = 0
        step = 100 / len(image_files) if image_files else 1
        
        success_count = 0
        for i, file_name in enumerate(image_files):
            try:
                # Полный путь к входному файлу
                file_path = os.path.join(self.input_dir, file_name)
                
                # Открытие и преобразование изображения
                with Image.open(file_path) as img:
                    # Для GIF изображений берем только первый кадр
                    if img.format == 'GIF':
                        img.seek(0)  # Переходим к первому кадру
                    
                    # Преобразование RGBA в RGB при необходимости (JPG не поддерживает прозрачность)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Создание белого фона
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        if img.mode in ('RGBA', 'LA'):
                            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    
                    # Изменение размера изображения, если указаны настройки разрешения
                    if self.target_width > 0 or self.target_height > 0:
                        original_width, original_height = img.size
                        
                        if self.preserve_aspect_ratio:
                            # Расчет новых размеров с сохранением соотношения сторон
                            if self.target_width > 0 and self.target_height > 0:
                                # Использование размера, который приводит к меньшему изображению, чтобы уместить в оба ограничения
                                ratio_1 = self.target_width / original_width
                                ratio_2 = self.target_height / original_height
                                final_ratio = min(ratio_1, ratio_2)
                                
                                new_width = int(original_width * final_ratio)
                                new_height = int(original_height * final_ratio)
                            elif self.target_width > 0:
                                # Указана только ширина
                                ratio = self.target_width / original_width
                                new_width = self.target_width
                                new_height = int(original_height * ratio)
                            else:
                                # Указана только высота
                                ratio = self.target_height / original_height
                                new_width = int(original_width * ratio)
                                new_height = self.target_height
                        else:
                            # Использование точных размеров без сохранения соотношения сторон
                            new_width = self.target_width if self.target_width > 0 else original_width
                            new_height = self.target_height if self.target_height > 0 else original_height
                        
                        # Изменение размера изображения
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Генерация имени выходного файла
                    base_name = os.path.splitext(file_name)[0]
                    output_path = os.path.join(self.output_dir, f"{base_name}.jpg")
                    
                    # Сохранение в формате JPG
                    img.save(output_path, "JPEG", quality=self.quality, optimize=True)
                
                success_count += 1
                self.status_var.set(f"Преобразовано: {file_name}")
                
            except Exception as e:
                messagebox.showerror("Ошибка преобразования", f"Не удалось преобразовать {file_name}: {str(e)}")
            
            # Обновление прогресса
            self.progress['value'] = (i + 1) * step
            self.root.update_idletasks()
        
        self.convert_button.config(state='normal')
        self.status_var.set(f"Преобразование завершено. {success_count}/{len(image_files)} файлов успешно преобразовано.")
        messagebox.showinfo("Преобразование завершено", f"Преобразование завершено. {success_count}/{len(image_files)} файлов успешно преобразовано.")
    
    def start_conversion(self):
        """Запуск процесса преобразования в отдельном потоке."""
        conversion_thread = threading.Thread(target=self.convert_files)
        conversion_thread.daemon = True
        conversion_thread.start()
    
    def on_preset_selected(self, event=None):
        """Обработчик события выбора пресета разрешения."""
        preset = self.resolution_preset_var.get()
        self.resolution_preset = preset  # Сохраняем выбранное значение пресета
        
        # Определение разрешений для различных пресетов
        resolutions = {
            "Без изменения": (0, 0),
            "1920x1080 (Full HD)": (1920, 1080),
            "1280x720 (HD)": (1280, 720),
            "3840x2160 (4K)": (3840, 2160),
            "2560x1440 (QHD)": (2560, 1440),
            "1366x768": (1366, 768),
            "1024x768": (1024, 768),
            "800x600": (800, 600)
        }
        
        if preset in resolutions:
            width, height = resolutions[preset]
            self.width_var.set(str(width))
            self.height_var.set(str(height))
            # Обновляем соответствующие переменные
            self.target_width = width
            self.target_height = height
        
        # Сохраняем настройки при изменении
        self.save_settings()
    
    def load_settings(self):
        """Загружает настройки из файла config/settings.json"""
        config_path = "config/settings.json"
        
        # Инициализируем значения по умолчанию
        self.input_dir = ""
        self.output_dir = "./converted_images"
        self.quality = 95
        self.target_width = 0
        self.target_height = 0
        self.preserve_aspect_ratio = True
        self.resolution_preset = "Без изменения"
        # Загружаем настройки темы по умолчанию
        self.theme_preference = "system" # По умолчанию следуем системной теме
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    
                # Загружаем сохраненные настройки
                self.output_dir = settings.get("default_output_directory", self.output_dir)
                self.quality = settings.get("default_quality", self.quality)
                
                # Загружаем пользовательские настройки (если они были сохранены ранее)
                self.input_dir = settings.get("last_input_directory", self.input_dir)
                self.target_width = settings.get("last_target_width", self.target_width)
                self.target_height = settings.get("last_target_height", self.target_height)
                self.preserve_aspect_ratio = settings.get("last_preserve_aspect_ratio", self.preserve_aspect_ratio)
                self.resolution_preset = settings.get("last_resolution_preset", self.resolution_preset)
                
                # Загружаем настройки темы
                self.theme_preference = settings.get("theme_preference", "system")
                
                # Определяем текущую тему на основе настроек
                if self.theme_preference == "system":
                    self.current_theme = self.system_theme
                else:
                    self.current_theme = self.theme_preference
                
        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"Ошибка при загрузке настроек: {e}")
            # Используем значения по умолчанию, если произошла ошибка
    
    def save_settings(self):
        """Сохраняет настройки в файл config/settings.json"""
        config_path = "config/settings.json"
        
        # Загружаем существующие настройки
        settings = {}
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Если файл не существует или поврежден, начинаем с пустого словаря
            settings = {}
        
        # Обновляем настройки с текущими значениями
        settings.update({
            "default_output_directory": self.output_dir,
            "default_quality": self.quality,
            "last_input_directory": self.input_dir,
            "last_target_width": self.target_width,
            "last_target_height": self.target_height,
            "last_preserve_aspect_ratio": self.preserve_aspect_ratio,
            "last_resolution_preset": self.resolution_preset,
            "theme_preference": self.theme_preference
        })
        
        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Сохраняем настройки
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка при сохранении настроек: {e}")
    
    # Удаляем дублирующийся метод update_ui_with_settings
    
    
    def update_ui_with_settings(self):
        """Обновляет интерфейс с текущими настройками"""
        # Обновляем поля ввода
        if hasattr(self, 'input_entry'):
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.input_dir)
        
        if hasattr(self, 'output_entry'):
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, self.output_dir)
        
        if hasattr(self, 'quality_var'):
            self.quality_var.set(str(self.quality))
        
        if hasattr(self, 'width_var'):
            self.width_var.set(str(self.target_width))
        
        if hasattr(self, 'height_var'):
            self.height_var.set(str(self.target_height))
        
        if hasattr(self, 'aspect_ratio_var'):
            self.aspect_ratio_var.set(self.preserve_aspect_ratio)
        
        if hasattr(self, 'resolution_preset_var'):
            self.resolution_preset_var.set(self.resolution_preset)
        
        # Обновляем настройки темы в интерфейсе
        if hasattr(self, 'theme_var'):
            self.theme_var.set(self.theme_preference)
    
    def on_quality_changed(self, event=None):
        """Обработчик изменения качества"""
        try:
            quality = int(self.quality_var.get())
            if 1 <= quality <= 100:
                self.quality = quality
                self.save_settings()
        except ValueError:
            pass  # Игнорируем недопустимые значения
    
    def on_quality_key_release(self, event=None):
        """Обработчик отпускания клавиши в поле качества"""
        # Используем after для отложенного вызова, чтобы значение успело обновиться
        self.root.after(10, self.on_quality_changed)
    
    def on_resolution_changed(self, event=None):
        """Обработчик изменения разрешения"""
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            self.target_width = width
            self.target_height = height
            self.save_settings()
        except ValueError:
            pass  # Игнорируем недопустимые значения
    
    def on_resolution_key_release(self, event=None):
        """Обработчик отпускания клавиши в полях разрешения"""
        # Используем after для отложенного вызова, чтобы значение успело обновиться
        self.root.after(10, self.on_resolution_changed)
    
    def on_aspect_ratio_changed(self):
        """Обработчик изменения флага сохранения соотношения сторон"""
        self.preserve_aspect_ratio = self.aspect_ratio_var.get()
        self.save_settings()
    
    def on_theme_changed(self, event=None):
        """Обработчик изменения темы"""
        self.theme_preference = self.theme_var.get()
        
        # Определяем текущую тему на основе настроек
        if self.theme_preference == "system":
            self.current_theme = self.system_theme
        else:
            self.current_theme = self.theme_preference
        
        # Применяем новую тему
        self._apply_theme()
        
        # Сохраняем настройки
        self.save_settings()
    
    def run(self):
        """Запуск приложения."""
        self.root.mainloop()


if __name__ == "__main__":
    app = PNGtoJPGConverter()
    app.run()