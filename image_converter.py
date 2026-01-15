"""
🖼️ Image Converter Pro - Advanced Image Format Converter
A modern, feature-rich image converter with a sleek PyQt5 interface.
Supports multiple formats, batch processing, and various optimization options.

Author: Leonardo Vianna
Repository: https://github.com/llleovianna/audio-converter
License: MIT
"""

import os
import sys
import json
import hashlib
import threading
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QSlider, QProgressBar,
    QTextEdit, QFileDialog, QCheckBox, QGroupBox, QTabWidget,
    QSpinBox, QFrame, QSplitter, QMessageBox, QListWidget,
    QListWidgetItem, QGridLayout, QScrollArea, QSizePolicy,
    QStatusBar, QMenu, QAction, QToolBar, QDialog, QDialogButtonBox,
    QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QSize, QTimer, QPropertyAnimation,
    QEasingCurve, QSequentialAnimationGroup, pyqtProperty
)
from PyQt5.QtGui import (
    QFont, QIcon, QPalette, QColor, QPixmap, QLinearGradient,
    QBrush, QPainter, QPen, QFontDatabase
)

try:
    from PIL import Image, ImageFilter, ImageEnhance, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ Pillow not installed. Run: pip install Pillow")


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & CONFIGURATIONS
# ═══════════════════════════════════════════════════════════════════════════════

APP_NAME = "Image Converter Pro"
APP_VERSION = "2.0.0"
GITHUB_URL = "https://github.com/llleovianna/audio-converter"

# Supported formats configuration
INPUT_FORMATS = {
    'PNG': ['.png'],
    'JPEG': ['.jpg', '.jpeg'],
    'WebP': ['.webp'],
    'BMP': ['.bmp'],
    'GIF': ['.gif'],
    'TIFF': ['.tiff', '.tif'],
    'ICO': ['.ico'],
    'All Images': ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif', '.tiff', '.tif']
}

OUTPUT_FORMATS = {
    'WebP': {'ext': '.webp', 'quality': True, 'optimize': True},
    'PNG': {'ext': '.png', 'quality': False, 'optimize': True},
    'JPEG': {'ext': '.jpg', 'quality': True, 'optimize': True},
    'BMP': {'ext': '.bmp', 'quality': False, 'optimize': False},
    'GIF': {'ext': '.gif', 'quality': False, 'optimize': True},
    'TIFF': {'ext': '.tiff', 'quality': True, 'optimize': False},
    'ICO': {'ext': '.ico', 'quality': False, 'optimize': False},
}

# Modern Dark Theme Stylesheet
DARK_THEME = """
QMainWindow {
    background-color: #0d1117;
}

QWidget {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

QGroupBox {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    margin-top: 12px;
    padding: 15px;
    font-weight: bold;
    font-size: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 5px 15px;
    background-color: #21262d;
    border-radius: 8px;
    color: #58a6ff;
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #238636, stop:1 #2ea043);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: bold;
    font-size: 14px;
    min-width: 120px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #2ea043, stop:1 #3fb950);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #196c2e, stop:1 #238636);
}

QPushButton:disabled {
    background: #21262d;
    color: #484f58;
}

QPushButton#dangerBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #da3633, stop:1 #f85149);
}

QPushButton#dangerBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #f85149, stop:1 #ff7b72);
}

QPushButton#secondaryBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #6e7681, stop:1 #8b949e);
}

QPushButton#secondaryBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #8b949e, stop:1 #c9d1d9);
}

QPushButton#accentBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #1f6feb, stop:1 #388bfd);
}

QPushButton#accentBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #388bfd, stop:1 #58a6ff);
}

QLineEdit, QSpinBox, QComboBox {
    background-color: #0d1117;
    border: 2px solid #30363d;
    border-radius: 8px;
    padding: 10px 15px;
    color: #c9d1d9;
    font-size: 13px;
    selection-background-color: #1f6feb;
}

QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border-color: #58a6ff;
    background-color: #161b22;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 8px solid #58a6ff;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #161b22;
    border: 2px solid #30363d;
    border-radius: 8px;
    selection-background-color: #1f6feb;
    padding: 5px;
}

QSlider::groove:horizontal {
    background: #21262d;
    height: 8px;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #58a6ff, stop:1 #1f6feb);
    width: 20px;
    height: 20px;
    margin: -6px 0;
    border-radius: 10px;
}

QSlider::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #79c0ff, stop:1 #58a6ff);
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #1f6feb, stop:1 #58a6ff);
    border-radius: 4px;
}

QProgressBar {
    background-color: #21262d;
    border: none;
    border-radius: 10px;
    height: 20px;
    text-align: center;
    font-weight: bold;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #238636, stop:0.5 #3fb950, stop:1 #238636);
    border-radius: 10px;
}

QTextEdit {
    background-color: #0d1117;
    border: 2px solid #30363d;
    border-radius: 12px;
    padding: 15px;
    font-family: 'Cascadia Code', 'Consolas', monospace;
    font-size: 12px;
    color: #c9d1d9;
}

QTabWidget::pane {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 10px;
}

QTabBar::tab {
    background-color: #21262d;
    color: #8b949e;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    font-weight: bold;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                stop:0 #1f6feb, stop:1 #161b22);
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background-color: #30363d;
    color: #c9d1d9;
}

QCheckBox {
    spacing: 10px;
    font-size: 13px;
}

QCheckBox::indicator {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid #30363d;
    background-color: #0d1117;
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #238636, stop:1 #3fb950);
    border-color: #3fb950;
}

QCheckBox::indicator:hover {
    border-color: #58a6ff;
}

QScrollBar:vertical {
    background-color: #0d1117;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #30363d;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #484f58;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QStatusBar {
    background-color: #161b22;
    border-top: 1px solid #30363d;
    padding: 5px;
    font-size: 12px;
}

QLabel#titleLabel {
    font-size: 28px;
    font-weight: bold;
    color: #58a6ff;
}

QLabel#subtitleLabel {
    font-size: 14px;
    color: #8b949e;
}

QLabel#statsLabel {
    background-color: #21262d;
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 13px;
}

QFrame#separator {
    background-color: #30363d;
    max-height: 1px;
}

QListWidget {
    background-color: #0d1117;
    border: 2px solid #30363d;
    border-radius: 12px;
    padding: 10px;
}

QListWidget::item {
    background-color: #161b22;
    border-radius: 6px;
    padding: 8px;
    margin: 3px 0;
}

QListWidget::item:selected {
    background-color: #1f6feb;
}

QListWidget::item:hover:!selected {
    background-color: #21262d;
}

QTableWidget {
    background-color: #0d1117;
    border: 2px solid #30363d;
    border-radius: 12px;
    gridline-color: #21262d;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #1f6feb;
}

QHeaderView::section {
    background-color: #161b22;
    color: #58a6ff;
    padding: 10px;
    border: none;
    font-weight: bold;
}

QToolTip {
    background-color: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 8px;
}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ConversionResult:
    """Stores the result of a single image conversion."""
    source_path: Path
    output_path: Optional[Path]
    success: bool
    original_size: int
    new_size: int
    error_message: str = ""
    
    @property
    def size_saved(self) -> int:
        return max(0, self.original_size - self.new_size)
    
    @property
    def compression_ratio(self) -> float:
        if self.original_size == 0:
            return 0.0
        return (self.size_saved / self.original_size) * 100


@dataclass
class ConversionSettings:
    """Stores all conversion settings."""
    input_format: str = "All Images"
    output_format: str = "WebP"
    quality: int = 80
    recursive: bool = True
    delete_original: bool = False
    preserve_metadata: bool = True
    resize_enabled: bool = False
    resize_width: int = 0
    resize_height: int = 0
    maintain_aspect_ratio: bool = True
    apply_optimization: bool = True
    rename_pattern: str = ""
    add_suffix: str = ""
    output_directory: str = ""
    max_workers: int = 4


# ═══════════════════════════════════════════════════════════════════════════════
# WORKER THREAD
# ═══════════════════════════════════════════════════════════════════════════════

class ConversionWorker(QThread):
    """Worker thread for image conversion."""
    
    progress = pyqtSignal(int, int)  # current, total
    log_message = pyqtSignal(str, str)  # message, type (info/success/error/warning)
    conversion_complete = pyqtSignal(list)  # list of ConversionResult
    file_converted = pyqtSignal(object)  # ConversionResult
    
    def __init__(self, directory: str, settings: ConversionSettings):
        super().__init__()
        self.directory = Path(directory)
        self.settings = settings
        self._is_cancelled = False
    
    def cancel(self):
        """Cancel the conversion process."""
        self._is_cancelled = True
    
    def get_input_extensions(self) -> List[str]:
        """Get list of input file extensions based on settings."""
        return INPUT_FORMATS.get(self.settings.input_format, INPUT_FORMATS['All Images'])
    
    def find_images(self) -> List[Path]:
        """Find all images in directory matching input format."""
        extensions = self.get_input_extensions()
        images = []
        
        if self.settings.recursive:
            for ext in extensions:
                images.extend(self.directory.rglob(f'*{ext}'))
                images.extend(self.directory.rglob(f'*{ext.upper()}'))
        else:
            for ext in extensions:
                images.extend(self.directory.glob(f'*{ext}'))
                images.extend(self.directory.glob(f'*{ext.upper()}'))
        
        # Remove duplicates and sort
        images = list(set(images))
        images.sort()
        return images
    
    def generate_output_path(self, source: Path) -> Path:
        """Generate output path for converted image."""
        output_ext = OUTPUT_FORMATS[self.settings.output_format]['ext']
        
        # Determine base name
        stem = source.stem
        
        # Apply rename pattern if set
        if self.settings.rename_pattern:
            pattern = self.settings.rename_pattern
            pattern = pattern.replace('{name}', stem)
            pattern = pattern.replace('{date}', datetime.now().strftime('%Y%m%d'))
            pattern = pattern.replace('{time}', datetime.now().strftime('%H%M%S'))
            stem = pattern
        
        # Add suffix if set
        if self.settings.add_suffix:
            stem = f"{stem}{self.settings.add_suffix}"
        
        # Determine output directory
        if self.settings.output_directory:
            output_dir = Path(self.settings.output_directory)
            # Preserve relative path structure
            relative = source.parent.relative_to(self.directory)
            output_dir = output_dir / relative
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = source.parent
        
        return output_dir / f"{stem}{output_ext}"
    
    def convert_single_image(self, source: Path) -> ConversionResult:
        """Convert a single image."""
        original_size = source.stat().st_size
        output_path = self.generate_output_path(source)
        
        try:
            with Image.open(source) as img:
                # Convert RGBA to RGB for formats that don't support transparency
                output_format = self.settings.output_format
                if img.mode == 'RGBA' and output_format in ['JPEG', 'BMP']:
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                elif img.mode == 'P' and output_format in ['JPEG']:
                    img = img.convert('RGB')
                
                # Resize if enabled
                if self.settings.resize_enabled:
                    new_size = self.calculate_resize(img.size)
                    if new_size != img.size:
                        img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Prepare save arguments
                save_kwargs = {}
                format_config = OUTPUT_FORMATS[output_format]
                
                if format_config['quality'] and output_format != 'PNG':
                    save_kwargs['quality'] = self.settings.quality
                
                if format_config['optimize'] and self.settings.apply_optimization:
                    save_kwargs['optimize'] = True
                
                # WebP specific options
                if output_format == 'WebP':
                    save_kwargs['method'] = 6  # Best compression
                
                # PNG specific options
                if output_format == 'PNG':
                    save_kwargs['compress_level'] = 9
                
                # Save the image
                img.save(output_path, format_config['ext'][1:].upper(), **save_kwargs)
            
            new_size = output_path.stat().st_size
            
            # Delete original if requested
            if self.settings.delete_original and source != output_path:
                source.unlink()
            
            return ConversionResult(
                source_path=source,
                output_path=output_path,
                success=True,
                original_size=original_size,
                new_size=new_size
            )
            
        except Exception as e:
            return ConversionResult(
                source_path=source,
                output_path=None,
                success=False,
                original_size=original_size,
                new_size=0,
                error_message=str(e)
            )
    
    def calculate_resize(self, original_size: Tuple[int, int]) -> Tuple[int, int]:
        """Calculate new size maintaining aspect ratio if needed."""
        width, height = original_size
        new_width = self.settings.resize_width or width
        new_height = self.settings.resize_height or height
        
        if self.settings.maintain_aspect_ratio:
            if self.settings.resize_width and not self.settings.resize_height:
                ratio = new_width / width
                new_height = int(height * ratio)
            elif self.settings.resize_height and not self.settings.resize_width:
                ratio = new_height / height
                new_width = int(width * ratio)
            elif self.settings.resize_width and self.settings.resize_height:
                ratio = min(new_width / width, new_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
        
        return (new_width, new_height)
    
    def run(self):
        """Execute the conversion process."""
        results = []
        
        self.log_message.emit(f"🔍 Scanning directory: {self.directory}", "info")
        images = self.find_images()
        
        if not images:
            self.log_message.emit("⚠️ No images found matching the selected format.", "warning")
            self.conversion_complete.emit(results)
            return
        
        total = len(images)
        self.log_message.emit(f"📁 Found {total} images to convert", "info")
        self.log_message.emit(f"🎯 Output format: {self.settings.output_format} | Quality: {self.settings.quality}%", "info")
        self.log_message.emit("─" * 60, "info")
        
        with ThreadPoolExecutor(max_workers=self.settings.max_workers) as executor:
            futures = {executor.submit(self.convert_single_image, img): img for img in images}
            
            for i, future in enumerate(as_completed(futures)):
                if self._is_cancelled:
                    self.log_message.emit("🛑 Conversion cancelled by user", "warning")
                    break
                
                result = future.result()
                results.append(result)
                
                if result.success:
                    self.log_message.emit(
                        f"✅ {result.source_path.name} → {result.output_path.name} "
                        f"({result.new_size/1024:.1f}KB, -{result.compression_ratio:.1f}%)",
                        "success"
                    )
                else:
                    self.log_message.emit(
                        f"❌ {result.source_path.name}: {result.error_message}",
                        "error"
                    )
                
                self.file_converted.emit(result)
                self.progress.emit(i + 1, total)
        
        self.conversion_complete.emit(results)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION WINDOW
# ═══════════════════════════════════════════════════════════════════════════════

class ImageConverterPro(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.settings = ConversionSettings()
        self.worker = None
        self.conversion_history = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1000, 800)
        self.setStyleSheet(DARK_THEME)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        self.create_header(main_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_conversion_tab()
        self.create_batch_operations_tab()
        self.create_settings_tab()
        self.create_history_tab()
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(f"Ready | {APP_NAME} v{APP_VERSION}")
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Center the window on screen."""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def create_header(self, layout):
        """Create the application header."""
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 10)
        
        # Title
        title = QLabel(f"🖼️ {APP_NAME}")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Convert, optimize, and manage your images with ease")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        # Separator
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.HLine)
        header_layout.addWidget(separator)
        
        layout.addWidget(header_frame)
    
    def create_conversion_tab(self):
        """Create the main conversion tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Directory selection group
        dir_group = QGroupBox("📁 Source Directory")
        dir_layout = QHBoxLayout(dir_group)
        
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Select a folder containing images...")
        dir_layout.addWidget(self.dir_input)
        
        browse_btn = QPushButton("📂 Browse")
        browse_btn.setObjectName("secondaryBtn")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(browse_btn)
        
        layout.addWidget(dir_group)
        
        # Format selection group
        format_group = QGroupBox("🔄 Format Settings")
        format_layout = QGridLayout(format_group)
        
        # Input format
        format_layout.addWidget(QLabel("Input Format:"), 0, 0)
        self.input_format_combo = QComboBox()
        self.input_format_combo.addItems(INPUT_FORMATS.keys())
        self.input_format_combo.setCurrentText("All Images")
        format_layout.addWidget(self.input_format_combo, 0, 1)
        
        # Output format
        format_layout.addWidget(QLabel("Output Format:"), 0, 2)
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(OUTPUT_FORMATS.keys())
        self.output_format_combo.setCurrentText("WebP")
        self.output_format_combo.currentTextChanged.connect(self.on_output_format_changed)
        format_layout.addWidget(self.output_format_combo, 0, 3)
        
        # Quality slider
        format_layout.addWidget(QLabel("Quality:"), 1, 0)
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(80)
        self.quality_slider.valueChanged.connect(self.on_quality_changed)
        format_layout.addWidget(self.quality_slider, 1, 1, 1, 2)
        
        self.quality_label = QLabel("80%")
        self.quality_label.setMinimumWidth(50)
        format_layout.addWidget(self.quality_label, 1, 3)
        
        layout.addWidget(format_group)
        
        # Options group
        options_group = QGroupBox("⚙️ Options")
        options_layout = QGridLayout(options_group)
        
        self.recursive_check = QCheckBox("🔄 Process subfolders recursively")
        self.recursive_check.setChecked(True)
        options_layout.addWidget(self.recursive_check, 0, 0)
        
        self.delete_original_check = QCheckBox("🗑️ Delete original files after conversion")
        options_layout.addWidget(self.delete_original_check, 0, 1)
        
        self.optimize_check = QCheckBox("⚡ Apply optimization")
        self.optimize_check.setChecked(True)
        options_layout.addWidget(self.optimize_check, 1, 0)
        
        self.preserve_metadata_check = QCheckBox("📋 Preserve metadata")
        self.preserve_metadata_check.setChecked(True)
        options_layout.addWidget(self.preserve_metadata_check, 1, 1)
        
        layout.addWidget(options_group)
        
        # Resize options
        resize_group = QGroupBox("📐 Resize Options")
        resize_layout = QGridLayout(resize_group)
        
        self.resize_check = QCheckBox("Enable resizing")
        self.resize_check.toggled.connect(self.on_resize_toggled)
        resize_layout.addWidget(self.resize_check, 0, 0, 1, 4)
        
        resize_layout.addWidget(QLabel("Width:"), 1, 0)
        self.width_spin = QSpinBox()
        self.width_spin.setRange(0, 10000)
        self.width_spin.setEnabled(False)
        self.width_spin.setSpecialValueText("Auto")
        resize_layout.addWidget(self.width_spin, 1, 1)
        
        resize_layout.addWidget(QLabel("Height:"), 1, 2)
        self.height_spin = QSpinBox()
        self.height_spin.setRange(0, 10000)
        self.height_spin.setEnabled(False)
        self.height_spin.setSpecialValueText("Auto")
        resize_layout.addWidget(self.height_spin, 1, 3)
        
        self.aspect_ratio_check = QCheckBox("Maintain aspect ratio")
        self.aspect_ratio_check.setChecked(True)
        self.aspect_ratio_check.setEnabled(False)
        resize_layout.addWidget(self.aspect_ratio_check, 2, 0, 1, 4)
        
        layout.addWidget(resize_group)
        
        # Progress section
        progress_group = QGroupBox("📊 Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        # Stats labels
        stats_layout = QHBoxLayout()
        self.files_label = QLabel("Files: 0/0")
        self.files_label.setObjectName("statsLabel")
        stats_layout.addWidget(self.files_label)
        
        self.saved_label = QLabel("Space Saved: 0 MB")
        self.saved_label.setObjectName("statsLabel")
        stats_layout.addWidget(self.saved_label)
        
        self.time_label = QLabel("Time: 0s")
        self.time_label.setObjectName("statsLabel")
        stats_layout.addWidget(self.time_label)
        
        progress_layout.addLayout(stats_layout)
        layout.addWidget(progress_group)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        self.convert_btn = QPushButton("🚀 Start Conversion")
        self.convert_btn.clicked.connect(self.start_conversion)
        btn_layout.addWidget(self.convert_btn)
        
        self.cancel_btn = QPushButton("🛑 Cancel")
        self.cancel_btn.setObjectName("dangerBtn")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_conversion)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
        
        # Log area
        log_group = QGroupBox("📝 Conversion Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMinimumHeight(150)
        log_layout.addWidget(self.log_area)
        
        clear_log_btn = QPushButton("🧹 Clear Log")
        clear_log_btn.setObjectName("secondaryBtn")
        clear_log_btn.clicked.connect(lambda: self.log_area.clear())
        log_layout.addWidget(clear_log_btn)
        
        layout.addWidget(log_group)
        
        self.tabs.addTab(tab, "🔄 Convert")
    
    def create_batch_operations_tab(self):
        """Create the batch operations tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Batch rename group
        rename_group = QGroupBox("✏️ Batch Rename")
        rename_layout = QGridLayout(rename_group)
        
        rename_layout.addWidget(QLabel("Directory:"), 0, 0)
        self.rename_dir_input = QLineEdit()
        self.rename_dir_input.setPlaceholderText("Select folder...")
        rename_layout.addWidget(self.rename_dir_input, 0, 1)
        
        rename_browse_btn = QPushButton("📂 Browse")
        rename_browse_btn.setObjectName("secondaryBtn")
        rename_browse_btn.clicked.connect(self.browse_rename_directory)
        rename_layout.addWidget(rename_browse_btn, 0, 2)
        
        rename_layout.addWidget(QLabel("Pattern:"), 1, 0)
        self.rename_pattern_input = QLineEdit()
        self.rename_pattern_input.setPlaceholderText("{name}_{date}_{counter}")
        self.rename_pattern_input.setToolTip(
            "Available placeholders:\n"
            "{name} - Original filename\n"
            "{date} - Current date (YYYYMMDD)\n"
            "{time} - Current time (HHMMSS)\n"
            "{counter} - Sequential number"
        )
        rename_layout.addWidget(self.rename_pattern_input, 1, 1, 1, 2)
        
        rename_btn = QPushButton("✏️ Rename Files")
        rename_btn.setObjectName("accentBtn")
        rename_btn.clicked.connect(self.batch_rename)
        rename_layout.addWidget(rename_btn, 2, 0, 1, 3)
        
        layout.addWidget(rename_group)
        
        # Duplicate finder group
        duplicate_group = QGroupBox("🔍 Find Duplicates")
        duplicate_layout = QVBoxLayout(duplicate_group)
        
        dup_dir_layout = QHBoxLayout()
        self.dup_dir_input = QLineEdit()
        self.dup_dir_input.setPlaceholderText("Select folder to scan...")
        dup_dir_layout.addWidget(self.dup_dir_input)
        
        dup_browse_btn = QPushButton("📂 Browse")
        dup_browse_btn.setObjectName("secondaryBtn")
        dup_browse_btn.clicked.connect(self.browse_duplicate_directory)
        dup_dir_layout.addWidget(dup_browse_btn)
        duplicate_layout.addLayout(dup_dir_layout)
        
        find_dup_btn = QPushButton("🔍 Find Duplicates")
        find_dup_btn.setObjectName("accentBtn")
        find_dup_btn.clicked.connect(self.find_duplicates)
        duplicate_layout.addWidget(find_dup_btn)
        
        self.duplicate_list = QListWidget()
        duplicate_layout.addWidget(self.duplicate_list)
        
        layout.addWidget(duplicate_group)
        
        # Image info group
        info_group = QGroupBox("ℹ️ Image Information")
        info_layout = QVBoxLayout(info_group)
        
        info_dir_layout = QHBoxLayout()
        self.info_file_input = QLineEdit()
        self.info_file_input.setPlaceholderText("Select an image...")
        info_dir_layout.addWidget(self.info_file_input)
        
        info_browse_btn = QPushButton("📂 Browse")
        info_browse_btn.setObjectName("secondaryBtn")
        info_browse_btn.clicked.connect(self.browse_info_file)
        info_dir_layout.addWidget(info_browse_btn)
        info_layout.addLayout(info_dir_layout)
        
        self.info_table = QTableWidget()
        self.info_table.setColumnCount(2)
        self.info_table.setHorizontalHeaderLabels(["Property", "Value"])
        self.info_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        info_layout.addWidget(self.info_table)
        
        layout.addWidget(info_group)
        
        layout.addStretch()
        self.tabs.addTab(tab, "🛠️ Batch Tools")
    
    def create_settings_tab(self):
        """Create the settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # Output settings
        output_group = QGroupBox("📤 Output Settings")
        output_layout = QGridLayout(output_group)
        
        output_layout.addWidget(QLabel("Output Directory:"), 0, 0)
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setPlaceholderText("Same as source (leave empty)")
        output_layout.addWidget(self.output_dir_input, 0, 1)
        
        output_browse_btn = QPushButton("📂 Browse")
        output_browse_btn.setObjectName("secondaryBtn")
        output_browse_btn.clicked.connect(self.browse_output_directory)
        output_layout.addWidget(output_browse_btn, 0, 2)
        
        output_layout.addWidget(QLabel("Filename Suffix:"), 1, 0)
        self.suffix_input = QLineEdit()
        self.suffix_input.setPlaceholderText("_converted")
        output_layout.addWidget(self.suffix_input, 1, 1, 1, 2)
        
        layout.addWidget(output_group)
        
        # Performance settings
        perf_group = QGroupBox("⚡ Performance")
        perf_layout = QGridLayout(perf_group)
        
        perf_layout.addWidget(QLabel("Max Workers (threads):"), 0, 0)
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 16)
        self.workers_spin.setValue(4)
        self.workers_spin.setToolTip("Number of parallel conversion threads")
        perf_layout.addWidget(self.workers_spin, 0, 1)
        
        layout.addWidget(perf_group)
        
        # About section
        about_group = QGroupBox("ℹ️ About")
        about_layout = QVBoxLayout(about_group)
        
        about_text = QLabel(
            f"<h3>{APP_NAME}</h3>"
            f"<p>Version: {APP_VERSION}</p>"
            f"<p>A modern, feature-rich image converter with support for multiple formats.</p>"
            f"<p><a href='{GITHUB_URL}' style='color: #58a6ff;'>GitHub Repository</a></p>"
            f"<p>Made with ❤️ by Leonardo Vianna</p>"
        )
        about_text.setOpenExternalLinks(True)
        about_text.setWordWrap(True)
        about_layout.addWidget(about_text)
        
        layout.addWidget(about_group)
        
        layout.addStretch()
        self.tabs.addTab(tab, "⚙️ Settings")
    
    def create_history_tab(self):
        """Create the conversion history tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            "Date/Time", "Files", "Format", "Space Saved", "Status"
        ])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.history_table)
        
        # Clear history button
        clear_btn = QPushButton("🧹 Clear History")
        clear_btn.setObjectName("secondaryBtn")
        clear_btn.clicked.connect(self.clear_history)
        layout.addWidget(clear_btn)
        
        self.tabs.addTab(tab, "📜 History")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EVENT HANDLERS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def browse_directory(self):
        """Open directory browser dialog."""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Image Directory", "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if directory:
            self.dir_input.setText(directory)
            self.log_message(f"📁 Selected directory: {directory}", "info")
    
    def browse_rename_directory(self):
        """Browse for rename directory."""
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.rename_dir_input.setText(directory)
    
    def browse_duplicate_directory(self):
        """Browse for duplicate finder directory."""
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.dup_dir_input.setText(directory)
    
    def browse_info_file(self):
        """Browse for image info file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image",
            "", "Images (*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tiff)"
        )
        if file_path:
            self.info_file_input.setText(file_path)
            self.show_image_info(file_path)
    
    def browse_output_directory(self):
        """Browse for output directory."""
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_dir_input.setText(directory)
    
    def on_quality_changed(self, value):
        """Handle quality slider change."""
        self.quality_label.setText(f"{value}%")
    
    def on_output_format_changed(self, format_name):
        """Handle output format change."""
        config = OUTPUT_FORMATS.get(format_name, {})
        self.quality_slider.setEnabled(config.get('quality', False))
        if not config.get('quality', False):
            self.quality_label.setText("N/A")
    
    def on_resize_toggled(self, checked):
        """Handle resize checkbox toggle."""
        self.width_spin.setEnabled(checked)
        self.height_spin.setEnabled(checked)
        self.aspect_ratio_check.setEnabled(checked)
    
    def log_message(self, message: str, msg_type: str = "info"):
        """Add message to log area with color coding."""
        colors = {
            "info": "#58a6ff",
            "success": "#3fb950",
            "error": "#f85149",
            "warning": "#d29922"
        }
        color = colors.get(msg_type, "#c9d1d9")
        self.log_area.append(f'<span style="color: {color};">{message}</span>')
        
        # Auto-scroll to bottom
        scrollbar = self.log_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def start_conversion(self):
        """Start the conversion process."""
        directory = self.dir_input.text()
        if not directory or not os.path.isdir(directory):
            QMessageBox.warning(self, "Warning", "Please select a valid directory.")
            return
        
        # Update settings
        self.settings.input_format = self.input_format_combo.currentText()
        self.settings.output_format = self.output_format_combo.currentText()
        self.settings.quality = self.quality_slider.value()
        self.settings.recursive = self.recursive_check.isChecked()
        self.settings.delete_original = self.delete_original_check.isChecked()
        self.settings.apply_optimization = self.optimize_check.isChecked()
        self.settings.preserve_metadata = self.preserve_metadata_check.isChecked()
        self.settings.resize_enabled = self.resize_check.isChecked()
        self.settings.resize_width = self.width_spin.value()
        self.settings.resize_height = self.height_spin.value()
        self.settings.maintain_aspect_ratio = self.aspect_ratio_check.isChecked()
        self.settings.output_directory = self.output_dir_input.text()
        self.settings.add_suffix = self.suffix_input.text()
        self.settings.max_workers = self.workers_spin.value()
        
        # Clear log and reset progress
        self.log_area.clear()
        self.progress_bar.setValue(0)
        self.total_saved = 0
        self.start_time = datetime.now()
        
        # Update UI state
        self.convert_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.statusBar.showMessage("Converting...")
        
        # Create and start worker
        self.worker = ConversionWorker(directory, self.settings)
        self.worker.progress.connect(self.on_progress)
        self.worker.log_message.connect(self.log_message)
        self.worker.conversion_complete.connect(self.on_conversion_complete)
        self.worker.file_converted.connect(self.on_file_converted)
        self.worker.start()
    
    def cancel_conversion(self):
        """Cancel the conversion process."""
        if self.worker:
            self.worker.cancel()
            self.log_message("🛑 Cancelling conversion...", "warning")
    
    def on_progress(self, current: int, total: int):
        """Handle progress update."""
        percentage = int((current / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(percentage)
        self.files_label.setText(f"Files: {current}/{total}")
        
        # Update time
        elapsed = (datetime.now() - self.start_time).total_seconds()
        self.time_label.setText(f"Time: {elapsed:.1f}s")
    
    def on_file_converted(self, result: ConversionResult):
        """Handle single file conversion completion."""
        if result.success:
            self.total_saved += result.size_saved
            self.saved_label.setText(f"Space Saved: {self.total_saved / 1024 / 1024:.2f} MB")
    
    def on_conversion_complete(self, results: List[ConversionResult]):
        """Handle conversion completion."""
        # Update UI state
        self.convert_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        
        # Calculate stats
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        total_saved = sum(r.size_saved for r in results if r.success)
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        # Log summary
        self.log_message("─" * 60, "info")
        self.log_message("🏁 Conversion Complete!", "success")
        self.log_message(f"✅ {successful} files converted successfully", "success")
        if failed > 0:
            self.log_message(f"❌ {failed} files failed", "error")
        self.log_message(f"💾 Total space saved: {total_saved / 1024 / 1024:.2f} MB", "info")
        self.log_message(f"⏱️ Total time: {elapsed:.2f} seconds", "info")
        
        self.statusBar.showMessage(f"Conversion complete: {successful} files processed")
        
        # Add to history
        self.add_to_history(results)
    
    def add_to_history(self, results: List[ConversionResult]):
        """Add conversion session to history."""
        successful = sum(1 for r in results if r.success)
        total_saved = sum(r.size_saved for r in results if r.success)
        
        row = self.history_table.rowCount()
        self.history_table.insertRow(row)
        
        self.history_table.setItem(row, 0, QTableWidgetItem(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.history_table.setItem(row, 1, QTableWidgetItem(
            f"{successful}/{len(results)}"
        ))
        self.history_table.setItem(row, 2, QTableWidgetItem(
            f"{self.settings.input_format} → {self.settings.output_format}"
        ))
        self.history_table.setItem(row, 3, QTableWidgetItem(
            f"{total_saved / 1024 / 1024:.2f} MB"
        ))
        self.history_table.setItem(row, 4, QTableWidgetItem(
            "✅ Success" if successful == len(results) else "⚠️ Partial"
        ))
    
    def clear_history(self):
        """Clear conversion history."""
        self.history_table.setRowCount(0)
    
    def batch_rename(self):
        """Perform batch rename operation."""
        directory = self.rename_dir_input.text()
        pattern = self.rename_pattern_input.text()
        
        if not directory or not os.path.isdir(directory):
            QMessageBox.warning(self, "Warning", "Please select a valid directory.")
            return
        
        if not pattern:
            QMessageBox.warning(self, "Warning", "Please enter a rename pattern.")
            return
        
        try:
            path = Path(directory)
            extensions = ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif', '.tiff']
            files = [f for f in path.iterdir() if f.suffix.lower() in extensions]
            
            counter = 1
            for file in sorted(files):
                new_name = pattern
                new_name = new_name.replace('{name}', file.stem)
                new_name = new_name.replace('{date}', datetime.now().strftime('%Y%m%d'))
                new_name = new_name.replace('{time}', datetime.now().strftime('%H%M%S'))
                new_name = new_name.replace('{counter}', str(counter).zfill(4))
                
                new_path = file.parent / f"{new_name}{file.suffix}"
                file.rename(new_path)
                counter += 1
            
            QMessageBox.information(
                self, "Success",
                f"Successfully renamed {counter - 1} files."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Rename failed: {str(e)}")
    
    def find_duplicates(self):
        """Find duplicate images in directory."""
        directory = self.dup_dir_input.text()
        
        if not directory or not os.path.isdir(directory):
            QMessageBox.warning(self, "Warning", "Please select a valid directory.")
            return
        
        self.duplicate_list.clear()
        hash_dict: Dict[str, List[Path]] = {}
        
        try:
            path = Path(directory)
            extensions = ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif', '.tiff']
            
            for file in path.rglob('*'):
                if file.suffix.lower() in extensions:
                    file_hash = self.get_file_hash(file)
                    if file_hash in hash_dict:
                        hash_dict[file_hash].append(file)
                    else:
                        hash_dict[file_hash] = [file]
            
            duplicates_found = 0
            for files in hash_dict.values():
                if len(files) > 1:
                    duplicates_found += 1
                    self.duplicate_list.addItem(f"─── Duplicate Group {duplicates_found} ───")
                    for f in files:
                        item = QListWidgetItem(f"  📄 {f.name}")
                        item.setToolTip(str(f))
                        self.duplicate_list.addItem(item)
            
            if duplicates_found == 0:
                self.duplicate_list.addItem("✅ No duplicates found!")
            else:
                self.duplicate_list.insertItem(
                    0, f"Found {duplicates_found} groups of duplicate files"
                )
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Search failed: {str(e)}")
    
    def get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file."""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            # Read in chunks for large files
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def show_image_info(self, file_path: str):
        """Display image information."""
        try:
            self.info_table.setRowCount(0)
            path = Path(file_path)
            
            with Image.open(path) as img:
                info = [
                    ("Filename", path.name),
                    ("Format", img.format or "Unknown"),
                    ("Mode", img.mode),
                    ("Size", f"{img.width} × {img.height} pixels"),
                    ("File Size", f"{path.stat().st_size / 1024:.2f} KB"),
                    ("Megapixels", f"{(img.width * img.height) / 1_000_000:.2f} MP"),
                ]
                
                # Add EXIF data if available
                if hasattr(img, '_getexif') and img._getexif():
                    exif = img._getexif()
                    if exif:
                        info.append(("EXIF Data", "Available"))
                
                for prop, value in info:
                    row = self.info_table.rowCount()
                    self.info_table.insertRow(row)
                    self.info_table.setItem(row, 0, QTableWidgetItem(prop))
                    self.info_table.setItem(row, 1, QTableWidgetItem(str(value)))
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not read image: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point."""
    if not PIL_AVAILABLE:
        print("Error: Pillow library is required. Install with: pip install Pillow")
        sys.exit(1)
    
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    # Set application icon (if available)
    # app.setWindowIcon(QIcon('icon.png'))
    
    window = ImageConverterPro()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
