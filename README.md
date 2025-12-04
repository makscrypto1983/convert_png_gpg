# PNG to JPG Converter

A simple GUI application to batch convert images to JPG format with customizable quality settings and resolution options. The application supports multiple input formats and provides an intuitive interface for converting images.

## Features

- Graphical user interface for easy image conversion
- Batch conversion of multiple images from a selected directory
- Adjustable quality settings for output images (1-100)
- Resolution customization with width and height controls
- Option to preserve aspect ratio during resizing
- Multiple resolution presets (Full HD, HD, 4K, QHD, etc.)
- Dark/light theme support with system theme detection
- Configurable output directory
- Progress bar to track conversion status
- Support for transparency handling (images with alpha channels)
- Support for multiple input formats: PNG, WEBP, BMP, and GIF

## System Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- Pillow for image processing
- ttkthemes for advanced theming (optional)

## Installation

  1. Clone this repository or download the source code
  2. Install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```
  3. Run the application:
     ```bash
     python main.py
     ```

## Usage Instructions

 1. Launch the application by running `python main.py`
  2. Select an input directory containing images using the "Обзор" button in the "Входная папка" section
  3. Set the output directory where converted images will be saved using the "Обзор" button in the "Настройки вывода" section
  4. Adjust quality settings (1-100) as needed - higher values mean better quality but larger file size
  5. Optionally select a resolution preset or set custom width and height for the output images
  6. Use the "Сохранить соотношение сторон" checkbox to maintain the original proportions when resizing
  7. Select the theme (system, light, or dark) from the theme dropdown
  8. Click "Преобразовать в JPG" to start the conversion process
  9. Monitor the progress bar and status messages during conversion
  10. Find your converted JPG images in the specified output directory

## Example Usage

  1. **Basic conversion**: Select a directory with PNG, WEBP, BMP, or GIF files, select output directory, click "Преобразовать в JPG"
  2. **Quality adjustment**: Set quality to 85 for smaller file size with good quality
  3. **Resolution change**: Select "1920x1080 (Full HD)" preset to resize all images to Full HD resolution
  4. **Batch conversion**: Convert all supported images in a selected directory at once
  5. **Format conversion**: Convert images from any supported format (PNG, WEBP, BMP, GIF) to JPG

## Interface Description

The application features a clean and intuitive interface with the following components:
- Input directory selection panel
- Output directory selection with browse button
- Quality control spinbox (1-100)
- Resolution presets dropdown (Full HD, HD, 4K, etc.)
- Resolution controls (width, height, aspect ratio preservation)
- Theme selection (system, light, dark)
- Progress bar showing conversion status
- Status bar with real-time updates
- Convert button to initiate the conversion process

## Configuration

The application can be configured using the `config/settings.json` file. You can modify default settings such as:
- Default output directory
- Default image quality
- Last used input directory
- Last used resolution settings
- Theme preference (system, light, dark)
- Preserve aspect ratio setting

## Supported Input Formats

The application supports conversion from the following image formats to JPG:
- PNG (Portable Network Graphics)
- WEBP (Web Picture format)
- BMP (Bitmap image file)
- GIF (Graphics Interchange Format) - Note: Only the first frame of animated GIFs will be converted

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact Information

For questions, suggestions, or support regarding this project, please contact:
- Project Repository: https://github.com/your-username/png-to-jpg-converter
- Email: pngjpg-converter@example.com
- Issues: Please report any issues or feature requests through the GitHub Issues section

We welcome feedback and contributions to improve this PNG to JPG converter application.