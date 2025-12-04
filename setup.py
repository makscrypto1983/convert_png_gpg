"""
Setup script for PNG to JPG Converter application.
"""

from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]


setup(
    name="png-to-jpg-converter",
    version="1.0.0",
    author="Developer",
    author_email="developer@example.com",
    description="A simple GUI application to convert PNG images to JPG format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/png-to-jpg-converter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "png-to-jpg=main:main",
        ],
    },
)