#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функциональности сохранения и восстановления настроек.
"""

import json
import os
from src.converter import PNGtoJPGConverter

def test_settings_functionality():
    """Тестирует функциональность сохранения и восстановления настроек."""
    print("Тестируем функциональность сохранения и восстановления настроек...")
    
    # Создаем экземпляр конвертера
    converter = PNGtoJPGConverter()
    
    # Проверяем начальные значения
    print(f"Начальные значения:")
    print(f"  input_dir: {converter.input_dir}")
    print(f"  output_dir: {converter.output_dir}")
    print(f"  quality: {converter.quality}")
    print(f"  target_width: {converter.target_width}")
    print(f"  target_height: {converter.target_height}")
    print(f"  preserve_aspect_ratio: {converter.preserve_aspect_ratio}")
    print(f"  resolution_preset: {converter.resolution_preset}")
    
    # Изменяем значения
    converter.input_dir = "/test/input"
    converter.output_dir = "/test/output"
    converter.quality = 85
    converter.target_width = 1920
    converter.target_height = 1080
    converter.preserve_aspect_ratio = False
    converter.resolution_preset = "1920x1080 (Full HD)"
    
    print(f"\nПосле изменения значений:")
    print(f"  input_dir: {converter.input_dir}")
    print(f"  output_dir: {converter.output_dir}")
    print(f"  quality: {converter.quality}")
    print(f"  target_width: {converter.target_width}")
    print(f"  target_height: {converter.target_height}")
    print(f"  preserve_aspect_ratio: {converter.preserve_aspect_ratio}")
    print(f"  resolution_preset: {converter.resolution_preset}")
    
    # Сохраняем настройки
    converter.save_settings()
    print(f"\nНастройки сохранены в config/settings.json")
    
    # Проверяем содержимое файла настроек
    with open("config/settings.json", 'r', encoding='utf-8') as f:
        settings = json.load(f)
    
    print(f"\nСодержимое файла настроек:")
    for key, value in settings.items():
        print(f" {key}: {value}")
    
    # Создаем новый экземпляр конвертера для проверки загрузки настроек
    print(f"\nСоздаем новый экземпляр конвертера для проверки загрузки настроек...")
    converter2 = PNGtoJPGConverter()
    
    print(f"\nЗагруженные значения:")
    print(f"  input_dir: {converter2.input_dir}")
    print(f"  output_dir: {converter2.output_dir}")
    print(f"  quality: {converter2.quality}")
    print(f" target_width: {converter2.target_width}")
    print(f" target_height: {converter2.target_height}")
    print(f" preserve_aspect_ratio: {converter2.preserve_aspect_ratio}")
    print(f"  resolution_preset: {converter2.resolution_preset}")
    
    # Проверяем, совпадают ли значения
    success = (
        converter.input_dir == converter2.input_dir and
        converter.output_dir == converter2.output_dir and
        converter.quality == converter2.quality and
        converter.target_width == converter2.target_width and
        converter.target_height == converter2.target_height and
        converter.preserve_aspect_ratio == converter2.preserve_aspect_ratio and
        converter.resolution_preset == converter2.resolution_preset
    )
    
    print(f"\nТест {'успешно пройден' if success else 'провален'}!")
    
    # Удаляем временные изменения из файла настроек
    # Восстановим первоначальные значения
    original_settings = {
        "default_output_directory": "./converted_images",
        "default_quality": 95,
        "create_subfolder_with_date": True,
        "overwrite_existing_files": False,
        "supported_input_formats": [".png"],
        "default_naming_pattern": "{filename}_converted.jpg",
        "max_threads": 4
    }
    
    # Добавляем последние сохраненные настройки, если они были
    if "last_input_directory" in settings:
        original_settings["last_input_directory"] = ""
    if "last_target_width" in settings:
        original_settings["last_target_width"] = 0
    if "last_target_height" in settings:
        original_settings["last_target_height"] = 0
    if "last_preserve_aspect_ratio" in settings:
        original_settings["last_preserve_aspect_ratio"] = True
    if "last_resolution_preset" in settings:
        original_settings["last_resolution_preset"] = "Без изменения"
    
    with open("config/settings.json", 'w', encoding='utf-8') as f:
        json.dump(original_settings, f, indent=2, ensure_ascii=False)
    
    print("Файл настроек восстановлен до первоначального состояния.")
    
    return success

if __name__ == "__main__":
    test_settings_functionality()