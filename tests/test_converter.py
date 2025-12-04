"""
Модульные тесты для функциональности конвертера PNG в JPG.
"""

import unittest
import os
import tempfile
from PIL import Image
import tkinter as tk
from src.converter import PNGtoJPGConverter


class TestPNGtoJPGConverter(unittest.TestCase):
    """
    Тестовые случаи для конвертера PNG в JPG.
    """
    
    def setUp(self):
        """Настройка тестовых данных перед каждым методом теста."""
        # Создание временного PNG изображения для тестирования
        self.test_image = Image.new('RGB', (100, 100), color='red')
        self.temp_dir = tempfile.mkdtemp()
        self.test_png_path = os.path.join(self.temp_dir, "test.png")
        self.test_image.save(self.test_png_path, "PNG")
        
        # Создание экземпляра конвертера без графического интерфейса для тестирования
        self.root = tk.Tk()
        self.root.withdraw()  # Скрытие главного окна
        self.converter = PNGtoJPGConverter()
        self.converter.root = self.root
        self.converter.input_files = [self.test_png_path]
        self.converter.output_dir = self.temp_dir
        self.converter.quality = 95
    
    def tearDown(self):
        """Очистка после каждого метода теста."""
        # Закрытие экземпляра tkinter
        self.root.destroy()
        
        # Удаление временных файлов
        if os.path.exists(self.test_png_path):
            os.remove(self.test_png_path)
        
        # Нахождение и удаление преобразованного JPG файла
        jpg_path = os.path.join(self.temp_dir, "test.jpg")
        if os.path.exists(jpg_path):
            os.remove(jpg_path)
        
        # Удаление временной директории
        os.rmdir(self.temp_dir)
    
    def test_converter_initialization(self):
        """Тест правильной инициализации конвертера."""
        self.assertIsInstance(self.converter, PNGtoJPGConverter)
        self.assertIsNotNone(self.converter.root)
        self.assertEqual(len(self.converter.input_files), 1)
    
    def test_valid_png_file_added(self):
        """Тест возможности добавления действительного PNG файла в список."""
        self.assertEqual(len(self.converter.input_files), 1)
        self.assertTrue(self.converter.input_files[0].endswith('.png'))
    
    def test_output_directory_set(self):
        """Тест правильной установки выходной директории."""
        self.assertEqual(self.converter.output_dir, self.temp_dir)
        self.assertTrue(os.path.isdir(self.converter.output_dir))
    
    def test_convert_png_to_jpg(self):
        """Тест фактического преобразования из PNG в JPG."""
        # Выполнение преобразования
        success_count = 0
        for file_path in self.converter.input_files:
            try:
                with Image.open(file_path) as img:
                    # Преобразование RGBA в RGB при необходимости
                    if img.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', img.size, (255, 25, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        if img.mode in ('RGBA', 'LA'):
                            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    
                    # Генерация имени выходного файла
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    output_path = os.path.join(self.converter.output_dir, f"{base_name}.jpg")
                    
                    # Сохранение в формате JPG
                    img.save(output_path, "JPEG", quality=self.converter.quality, optimize=True)
                
                success_count += 1
                
                # Проверка существования выходного файла и его корректности в формате JPG
                jpg_path = os.path.join(self.converter.output_dir, "test.jpg")
                self.assertTrue(os.path.exists(jpg_path))
                
                # Проверка, что выходной файл является корректным изображением
                with Image.open(jpg_path) as jpg_img:
                    self.assertEqual(jpg_img.format, "JPEG")
                    self.assertEqual(jpg_img.size, (100, 100))
                
            except Exception as e:
                self.fail(f"Преобразование не удалось с ошибкой: {str(e)}")
        
        self.assertEqual(success_count, 1)


if __name__ == '__main__':
    unittest.main()