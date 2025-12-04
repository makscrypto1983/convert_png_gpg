"""  """#!/usr/bin/env python3
"""
Главная точка входа для приложения PNG to JPG Converter.

Это графическое приложение позволяет пользователям преобразовывать
PNG изображения в формат JPG с настраиваемыми параметрами качества.
"""

import sys
import os
from src.converter import PNGtoJPGConverter

def main():
    """Основная функция для запуска приложения конвертера PNG в JPG."""
    app = PNGtoJPGConverter()
    app.run()

if __name__ == "__main__":
    main()