<div align="center">

# 🖼️ Image Converter Pro

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-41cd52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/llleovianna/audio-converter?style=for-the-badge&color=gold)](https://github.com/llleovianna/audio-converter/stargazers)
[![Issues](https://img.shields.io/github/issues/llleovianna/audio-converter?style=for-the-badge&color=red)](https://github.com/llleovianna/audio-converter/issues)

<p align="center">
  <img src="https://raw.githubusercontent.com/llleovianna/audio-converter/main/assets/demo.gif" alt="Demo" width="700"/>
</p>

### 🚀 A modern, feature-rich image converter with a sleek dark interface

**Convert • Optimize • Batch Process • Rename • Find Duplicates**

[📥 Download](#-installation) • [✨ Features](#-features) • [📖 Usage](#-usage) • [🤝 Contributing](#-contributing)

---

</div>

## 🌟 Why Image Converter Pro?

<table>
<tr>
<td width="50%">

### ⚡ Lightning Fast
Multi-threaded conversion using up to 16 parallel workers for maximum performance.

### 🎨 Modern UI
Beautiful dark theme interface built with PyQt5, designed for power users.

### 📦 Multi-Format Support
Convert between PNG, JPEG, WebP, BMP, GIF, TIFF, and ICO formats.

</td>
<td width="50%">

### 🔄 Batch Operations
Process entire folders recursively with smart file management.

### 💾 Space Optimizer
Reduce image sizes by up to 90% with WebP conversion while maintaining quality.

### 🛠️ Advanced Tools
Batch rename, duplicate finder, image info viewer, and more!

</td>
</tr>
</table>

---

## ✨ Features

### 🔄 Format Conversion
- **Input Formats**: PNG, JPEG, WebP, BMP, GIF, TIFF, ICO
- **Output Formats**: WebP, PNG, JPEG, BMP, GIF, TIFF, ICO
- Quality control slider (1-100%)
- Automatic optimization for web delivery

### 📁 Directory Processing
- Recursive folder scanning
- Preserve directory structure in output
- Custom output directory option
- Automatic file suffix addition

### 📐 Image Resizing
- Custom width/height dimensions
- Maintain aspect ratio option
- High-quality Lanczos resampling

### 🛠️ Batch Tools
| Tool | Description |
|------|-------------|
| **✏️ Batch Rename** | Rename files using patterns with placeholders |
| **🔍 Duplicate Finder** | Find duplicate images using MD5 hash comparison |
| **ℹ️ Image Info** | View detailed image metadata and properties |

### ⚙️ Advanced Options
- Delete original files after conversion
- Preserve metadata (EXIF data)
- Custom filename patterns
- Multi-threaded processing (1-16 workers)
- Conversion history tracking

---

## 📥 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/llleovianna/audio-converter.git

# Navigate to the directory
cd audio-converter

# Install dependencies
pip install -r requirements.txt

# Run the application
python image_converter.py
```

### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python image_converter.py
```

---

## 📖 Usage

### Basic Conversion

1. **Launch the application**
   ```bash
   python image_converter.py
   ```

2. **Select source directory**
   - Click "📂 Browse" to choose a folder containing images

3. **Configure settings**
   - Choose input format filter (or "All Images")
   - Select output format (WebP recommended for web)
   - Adjust quality slider (80% recommended)

4. **Start conversion**
   - Click "🚀 Start Conversion"
   - Monitor progress in real-time

### Batch Rename

Use placeholders in the rename pattern:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{name}` | Original filename | `photo` |
| `{date}` | Current date | `20260115` |
| `{time}` | Current time | `143052` |
| `{counter}` | Sequential number | `0001` |

**Example Pattern**: `{name}_{date}_{counter}` → `photo_20260115_0001.jpg`

---

## 🎨 Screenshots

<div align="center">

### Main Interface
| Dark Theme | Conversion Progress |
|------------|---------------------|
| ![Main](https://via.placeholder.com/400x300/0d1117/58a6ff?text=Main+Interface) | ![Progress](https://via.placeholder.com/400x300/0d1117/3fb950?text=Progress+View) |

### Batch Tools
| Rename Tool | Duplicate Finder |
|-------------|------------------|
| ![Rename](https://via.placeholder.com/400x300/0d1117/d29922?text=Batch+Rename) | ![Duplicates](https://via.placeholder.com/400x300/0d1117/f85149?text=Find+Duplicates) |

</div>

---

## 📊 Performance

<div align="center">

| Metric | Value |
|--------|-------|
| **Average Compression** | 60-80% size reduction |
| **Processing Speed** | ~50 images/second* |
| **Memory Usage** | < 200MB |
| **Max Workers** | 16 threads |

*Depends on image size and system specifications*

</div>

---

## 🗂️ Project Structure

```
image-converter-pro/
├── 📄 image_converter.py    # Main application
├── 📄 requirements.txt      # Python dependencies
├── 📄 README.md            # Documentation
├── 📄 LICENSE              # MIT License
├── 📄 .gitignore           # Git ignore rules
└── 📁 assets/              # Images and icons (future)
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Ideas for Contribution

- [ ] Add drag & drop support
- [ ] Implement image preview
- [ ] Add watermark functionality
- [ ] Create portable executable (PyInstaller)
- [ ] Add command-line interface
- [ ] Support for RAW image formats
- [ ] Cloud storage integration
- [ ] Localization (i18n)

---

## 📋 Changelog

### v2.0.0 (2026-01-15)
- 🎨 Complete UI redesign with PyQt5
- 🌙 Modern dark theme
- ✨ Multi-format support (PNG, JPEG, WebP, BMP, GIF, TIFF, ICO)
- 🔄 Batch rename functionality
- 🔍 Duplicate finder tool
- 📐 Image resizing options
- ⚡ Multi-threaded processing
- 📊 Conversion history tracking

### v1.0.0 (Initial)
- Basic PNG/JPG to WebP conversion
- Simple Tkinter interface

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Leonardo Vianna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 💖 Support

If you find this project useful, please consider:

- ⭐ **Starring** this repository
- 🐛 **Reporting** bugs and issues
- 💡 **Suggesting** new features
- 🔀 **Contributing** code improvements

---

<div align="center">

### Made with ❤️ by [Leonardo Vianna](https://github.com/llleovianna)

[![GitHub](https://img.shields.io/badge/GitHub-llleovianna-181717?style=flat-square&logo=github)](https://github.com/llleovianna)

**⭐ Star this repo if you find it useful! ⭐**

</div>

### Otimizações
- `optimize=True`: Busca a melhor estratégia de compressão
- `quality`: Controla o balanço entre tamanho e qualidade visual
- Suporte a canal Alpha (transparência)
- Processamento assíncrono para interface responsiva

### Estrutura do Código

```python
ConversorWebP
├── criar_interface()        # Monta a UI com TKinter
├── escolher_diretorio()     # Diálogo de seleção de pasta
├── iniciar_conversao()      # Gerencia thread de conversão
└── converter_imagens()      # Lógica principal de conversão
```

## 💡 Dicas

- **Para fotos JPEG**: Use qualidade 75-85
- **Para PNG com transparência**: Use qualidade 80-90
- **Para gráficos/ícones**: Use qualidade 85-95
- Teste diferentes configurações em uma amostra antes de processar tudo

## ⚠️ Notas Importantes

- As imagens originais são mantidas intactas
- Verifique o espaço em disco antes de processar muitas imagens
- A conversão pode levar tempo dependendo da quantidade de arquivos
- Interromper o processo pode deixar conversões incompletas

## 📄 Licença

Código livre para uso pessoal e comercial.
