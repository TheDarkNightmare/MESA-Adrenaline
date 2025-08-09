import os
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTabWidget,
    QWidget,
    QPushButton,
    QProgressBar,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from qt_material import apply_stylesheet
import subprocess
from datetime import datetime
import sys
sys.path.append('./src')

# Main application file

from src.definitions import (
    get_smart_access_memory_status,
    get_amdgpu_ppfeaturemask_status,
    get_gpu_name,
    get_gpu_temperature,
    get_gpu_fan_speed,
    get_cpu_name,
    get_cpu_temperature,
    get_cpu_mhz,
    get_memory_usage
)
class AdrenalineStyleApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Settings
        self.setWindowTitle("AMD Adrenaline Linux")
        self.setGeometry(100, 100, 1200, 800)

        # Ensure font is installed and used correctly
        self.font_family = "Roboto"
        if self.font_family not in QFontDatabase().families():
            print(f"Warning: Font '{self.font_family}' not found, falling back to default.")
            self.font_family = "Arial"  # Fallback font

        # Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Add tabs
        self.add_tab("Home", self.home_tab())
        self.add_tab("Performance", self.performance_tab())
        self.add_tab("Settings", self.settings_tab())

    def add_tab(self, title, content_widget):
        self.tabs.addTab(content_widget, title)

    @staticmethod
    def download_icon(url, local_filename):
        """Download the icon from the specified URL or use the local file if already present."""
        if not os.path.exists(local_filename):
            try:
                print(f"Downloading icon from {url}...")
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(local_filename, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    print(f"Icon downloaded successfully to {local_filename}")
                else:
                    print(f"Failed to download icon. HTTP Status Code: {response.status_code}")
                    return None
            except Exception as e:
                print(f"Error downloading icon: {e}")
                return None  # If download fails, return None
        return local_filename

    def get_mesa_version(self):
        try:
            result = subprocess.run(["glxinfo"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "OpenGL version string" in line:
                    return line.split(": ")[1]
        except FileNotFoundError:
            return "Mesa not found"
        return "Unknown"

    def get_kernel_version(self):
        try:
            result = subprocess.run(["uname", "-r"], capture_output=True, text=True)
            return result.stdout.strip()
        except FileNotFoundError:
            return "Unknown"

    def home_tab(self):
        widget = QWidget()
        main_layout = QVBoxLayout()

        title = QLabel("Welcome to the AMD Adrenaline for Linux.\nThis tool is currently in alfa state.")
        title.setFont(QFont(self.font_family, 16))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setAlignment(Qt.AlignTop)  # Align everything to the top

        # Blocks Layout
        block_layout = QVBoxLayout()
        block_layout.setSpacing(10)

        # Row 1 Layout
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(10)

        # Block 1: AMD Software Information
        current_time = datetime.now().strftime("%Y-%m-%d")
        block1 = QWidget()
        block1_layout = QVBoxLayout(block1)
        block1_label = QLabel(self.format_text(
            "  &nbsp;&nbsp; <b>AMD Adrenaline LINUX (alfa)</b>",
            f"Version: 0.1.003-alfa",
            f"Updated: {current_time}"
        ))
        block1_label.setFont(QFont(self.font_family, 12))
        block1_label.setAlignment(Qt.AlignTop)
        block1_layout.addWidget(block1_label)
        block1.setFixedSize(600, 150)  # Adjust block size

        # Block 2: System Information
        kernel_version = self.get_kernel_version()
        mesa_version = self.get_mesa_version()
        block2 = QWidget()
        block2_layout = QVBoxLayout(block2)
        block2_label = QLabel(self.format_text(
            "  &nbsp;&nbsp; <b>System Information</b>",
            f"<br>Kernel: {kernel_version}",
            f"Mesa Version: {mesa_version}"
        ))
        block2_label.setFont(QFont(self.font_family, 12))
        block2_label.setAlignment(Qt.AlignTop)
        block2_layout.addWidget(block2_label)
        block2.setFixedSize(600, 150)  # Adjust block size

        # Add blocks to row 1
        row1_layout.addWidget(block1)
        row1_layout.addWidget(block2)

        # Row 2 Layout
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(10)

        # Block 3: Smart Access Memory
        sam_status = get_smart_access_memory_status()
        sam_color = "green" if sam_status else "red"
        block3 = QWidget()
        block3_layout = QVBoxLayout(block3)

        block3_label = QLabel(self.format_text(
            " &nbsp;&nbsp; <b>Smart Access Memory</b>",
            f"<br>Status: <span style='color: {sam_color};'>{'Enabled' if sam_status else 'Disabled'}</span>",
            "<br>AMD Smart Access Memory™ technology unlocks higher performance <br> across select titles by providing AMD Ryzen™ processors with immediate,<br> full access to AMD Radeon™ graphics memory for faster data transfers between the two."
        ))
        block3_label.setFont(QFont(self.font_family, 12))
        block3_label.setAlignment(Qt.AlignTop)
        block3_layout.addWidget(block3_label)

        block3.setFixedSize(600, 200)  # Adjust block size to fit the text

        # Block 4: AMDGPU Performance Override
        override_status = get_amdgpu_ppfeaturemask_status()
        override_label = "Enabled" if override_status else "Disabled"
        override_color = "green" if override_status else "red"
        config_label = "AMD Performance Override" if override_status else "Stock"
        config_color = "orange" if override_status else "blue"

        block4 = QWidget()
        block4_layout = QVBoxLayout(block4)
        block4_label = QLabel(self.format_text(
            "󰆷  &nbsp;&nbsp; <b>System Performance Override</b>",
            f"<br>Status: <span style='color: {override_color};'>{override_label}</span>",
            f"Configuration: <span style='color: {config_color};'>{config_label}</span>",
            "<br>It is required to unlock access clocks and voltages in sysfs by appending the Kernel parameter"
        ))
        block4_label.setFont(QFont(self.font_family, 12))
        block4_label.setAlignment(Qt.AlignTop)
        block4_layout.addWidget(block4_label)
        block4.setFixedSize(600, 200)  # Adjust block size

        # Add block to row 2
        row2_layout.addWidget(block3)
        row2_layout.addWidget(block4)

        # Add rows to the main block layout
        block_layout.addLayout(row1_layout)
        block_layout.addLayout(row2_layout)

        # Add layout to top of the window
        main_layout.addLayout(block_layout)

        widget.setLayout(main_layout)
        return widget

    def format_text(self, *lines):
        """Combine lines into formatted HTML."""
        return "<br>".join(lines)



    def performance_tab(self):
        widget = QWidget()
        main_layout = QVBoxLayout()

        title = QLabel("Performance Monitoring")
        title.setFont(QFont(self.font_family, 13))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setAlignment(Qt.AlignTop)  # Align everything to the top

        # Blocks Layout
        block_layout = QVBoxLayout()
        block_layout.setSpacing(10)

        # Row 1 Layout
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(10)

        # Block 1: GPU Information
        gpu_name = get_gpu_name()
        gpu_temp = get_gpu_temperature()
        gpu_fan_speed = get_gpu_fan_speed()

        # Block 1: GPU Information
        block1 = QWidget()
        block1_layout = QVBoxLayout(block1)
        self.gpu_label = QLabel(self.format_text(
            " &nbsp;&nbsp; <b>GPU</b>",
            f"<br><b>Model:</b> {gpu_name}",
            f"<br><b>Temperature:</b> {gpu_temp}",
            f"<br><b>Fan Speed:</b> {gpu_fan_speed}"
            ))
        self.gpu_label.setFont(QFont(self.font_family, 11))
        self.gpu_label.setAlignment(Qt.AlignTop)
        block1_layout.addWidget(self.gpu_label)
        block1.setFixedSize(600, 200)  # Adjust block size

        cpu_name = get_cpu_name()
        cpu_temp = get_cpu_temperature()
        cpu_mhz = get_cpu_mhz()

        # Block 2: CPU Information
        block2 = QWidget()
        block2_layout = QVBoxLayout(block2)
        block2_label = QLabel(self.format_text(
            " &nbsp;&nbsp; <b>CPU</b>",
            f"<br><b>Model:</b> {cpu_name}",
            f"<br><b>Temperature:</b> {cpu_temp}",
            f"<br><b>Frequency:</b> {cpu_mhz}"
        ))
        block2_label.setFont(QFont(self.font_family, 11))
        block2_label.setAlignment(Qt.AlignTop)
        block2_layout.addWidget(block2_label)
        block2.setFixedSize(600, 200)  # Adjust block size

        # Add blocks to row 1
        row1_layout.addWidget(block1)
        row1_layout.addWidget(block2)

        # Row 2 Layout
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(10)

        used_ram, total_ram = get_memory_usage()
        # Block 3: RAM Information
        block3 = QWidget()
        block3_layout = QVBoxLayout(block3)
        block3_layout.setContentsMargins(10, 10, 10, 10)  # Adjust padding

        # RAM Information Title
        block3_title = QLabel(" &nbsp;&nbsp;<b>RAM Information</b>")
        block3_title.setFont(QFont(self.font_family, 12))
        block3_title.setAlignment(Qt.AlignLeft)
        block3_layout.addWidget(block3_title)

        # RAM Usage Bar
        ram_usage_bar = QProgressBar()
        ram_usage_bar.setMaximum(total_ram)
        ram_usage_bar.setValue(used_ram)
        ram_usage_bar.setTextVisible(True)
        ram_usage_bar.setFormat(f"{used_ram}MB / {total_ram}MB")  # Display usage on the bar
        # Adjust bar length
        ram_usage_bar.setFixedWidth(500)  # Set the desired width (e.g., 500 pixels)
        ram_usage_bar.setFixedHeight(25)  # Optional: adjust bar height

        block3_layout.addWidget(ram_usage_bar)

        # Set the overall block styling
        block3.setFixedSize(590, 150)  # Adjust block size to fit content




        # Block 4: Settings Information
        block4 = QWidget()
        block4_layout = QVBoxLayout(block4)
        block4_label = QLabel(self.format_text(
            "<b>Settings</b>",
            "<br>Status: Placeholder",
            "<br>Details: Placeholder"
        ))
        block4_label.setFont(QFont(self.font_family, 12))
        block4_label.setAlignment(Qt.AlignTop)
        block4_layout.addWidget(block4_label)
        block4.setFixedSize(600, 150)  # Adjust block size

        # Add blocks to row 2
        row2_layout.addWidget(block3)
        row2_layout.addWidget(block4)

        # Add rows to the main block layout
        block_layout.addLayout(row1_layout)
        block_layout.addLayout(row2_layout)

        # Add layout to the main tab
        main_layout.addLayout(block_layout)

        widget.setLayout(main_layout)

                # Set up a timer to update GPU information dynamically
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gpu_info)
        self.timer.start(3000)  # Update every 3 seconds

        return widget

    def update_gpu_info(self):
        """Update the GPU information dynamically."""
        self.gpu_label.setText(self.format_text(
            " &nbsp;&nbsp; <b>GPU</b>",
            f"<br><b>Model:</b> {get_gpu_name()}",
            f"<br><b>Temperature:</b> {get_gpu_temperature()}",
            f"<br><b>Fan Speed:</b> {get_gpu_fan_speed()}"
        ))

    def settings_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Settings")
        title.setFont(QFont(self.font_family, 16))
        title.setAlignment(Qt.AlignCenter)

        # Add a Toggle SAM button
        button = QPushButton("Toggle SAM")

        layout.addWidget(title)
        layout.addWidget(button)
        widget.setLayout(layout)
        return widget


if __name__ == "__main__":
    if sys.platform.startswith("linux"):
        os.environ["QT_QPA_PLATFORM"] = "wayland"
        os.environ["QT_QPA_PLATFORMTHEME"] = "qt5ct"

    app = QApplication([])
    apply_stylesheet(app, theme="dark_red.xml")

    icon_url = "https://raw.githubusercontent.com/TheDarkNightmare/PulseTool/main/icon.png"
    icon_local_path = "./icon.png"

    # Download the icon from the URL
    icon_path = AdrenalineStyleApp.download_icon(icon_url, icon_local_path)

    # Set the application icon if the download was successful
    if icon_path:
        app.setWindowIcon(QIcon(icon_path))
    else:
        print("Failed to set the icon.")

    # Ensure the font is installed
    font_family = "Roboto"  # Font name to apply globally
    if font_family in QFontDatabase().families():
        app.setFont(QFont(font_family))  # Set the global application font
        print(f"Using font: {font_family}")
    else:
        print(f"Warning: Font '{font_family}' not found. Falling back to default.")

    # Create the main window
    window = AdrenalineStyleApp()

    window.show()

    app.exec_()
