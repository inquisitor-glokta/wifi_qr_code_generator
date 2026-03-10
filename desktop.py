import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                           QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QFileDialog)
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import Qt
import qrcode
from PIL import Image

class WiFiQRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFi QR Code Generator - All Standards")
        
        # Load icon
        icon_path = "ico.ico"
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            self.setWindowIcon(icon)
        
        self.setGeometry(100, 100, 500, 700)

        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Title
        title = QLabel("📶 WiFi QR Code Generator")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin: 10px;")
        layout.addWidget(title)

        # SSID input
        self.ssid_edit = QLineEdit()
        self.ssid_edit.setPlaceholderText("Network Name (SSID)")
        self.ssid_edit.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.ssid_edit)

        # Password input
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_edit.setPlaceholderText("Password (leave empty for open networks)")
        self.pass_edit.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.pass_edit)

        # Security type with modern standards + security indicators
        security_layout = QWidget()
        security_layout_layout = QVBoxLayout(security_layout)
        
        security_label = QLabel("🔒 Security Type:")
        security_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        security_layout_layout.addWidget(security_label)
        
        self.security_combo = QComboBox()
        self.security_combo.addItems([
            "WPA3 (Latest) - Highest security, SAE protection",
            "WPA2 (Standard) - AES encryption, still secure", 
            "WPA (Obsolete) - TKIP, avoid if possible",
            "WEP (Broken) - Cracked in minutes, DO NOT USE",
            "nopass (Open) - No encryption"
        ])
        self.security_combo.setStyleSheet("padding: 8px; font-size: 13px;")
        security_layout_layout.addWidget(self.security_combo)
        layout.addWidget(security_layout)

        # Hidden network checkbox
        self.hidden_cb = QCheckBox("🌐 Hidden Network")
        self.hidden_cb.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.hidden_cb)

        # Buttons
        btn_layout = QWidget()
        btn_layout_layout = QVBoxLayout(btn_layout)
        
        self.generate_btn = QPushButton("✅ Generate QR Code")
        self.generate_btn.clicked.connect(self.generate_qr)
        self.generate_btn.setStyleSheet("""
            QPushButton { 
                background-color: #27ae60; 
                color: white; 
                padding: 12px; 
                font-size: 14px; 
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #2ecc71; }
            QPushButton:pressed { background-color: #229954; }
        """)
        btn_layout_layout.addWidget(self.generate_btn)

        self.save_btn = QPushButton("💾 Save as PNG")
        self.save_btn.clicked.connect(self.save_qr)
        self.save_btn.setStyleSheet("""
            QPushButton { 
                background-color: #3498db; 
                color: white; 
                padding: 12px; 
                font-size: 14px; 
                font-weight: bold;
                border-radius: 8px;
                margin-top: 5px;
            }
            QPushButton:hover { background-color: #5dade2; }
            QPushButton:pressed { background-color: #2980b9; }
        """)
        btn_layout_layout.addWidget(self.save_btn)
        
        layout.addWidget(btn_layout)

        # QR display
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setMinimumSize(350, 350)
        self.qr_label.setStyleSheet("""
            border: 3px solid #3498db; 
            background: white; 
            border-radius: 12px;
        """)
        layout.addWidget(self.qr_label)

        # Footer
        footer = QLabel("Software created by Šamec Uglješa © 2026")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #95a5a6; font-size: 11px; padding: 10px; border-top: 1px solid #ecf0f1;")
        layout.addWidget(footer)

        self.setCentralWidget(widget)

    def get_security_type(self):
        """Convert UI text to QR code standard format"""
        text = self.security_combo.currentText().lower()
        if "wpa3" in text:
            return "WPA3"
        elif "wpa2" in text:
            return "WPA2"
        elif "wpa" in text:
            return "WPA"
        elif "wep" in text:
            return "WEP"
        else:  # nopass/open
            return "nopass"

    def generate_qr(self):
        ssid = self.ssid_edit.text().strip()
        password = self.pass_edit.text()
        security = self.get_security_type()
        hidden = "true" if self.hidden_cb.isChecked() else "false"

        if not ssid:
            self.qr_label.setText("⚠️ Please enter Network Name (SSID)")
            return

        # WiFi QR format standard - supports all protocols
        data = f"WIFI:S:{ssid};T:{security};P:{password};H:{hidden};;"
        
        try:
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=8, border=4)
            qr.add_data(data)
            qr.make(fit=True)
            
            pil_img = qr.make_image(fill_color="black", back_color="white")
            pil_img = pil_img.convert('RGB')
            
            # Convert to QPixmap
            width, height = pil_img.size
            data_bytes = pil_img.tobytes("raw", "RGBX")
            qimage = QImage(data_bytes, width, height, width * 4, QImage.Format.Format_RGB32)
            pixmap = QPixmap.fromImage(qimage)
            scaled = pixmap.scaled(320, 320, Qt.AspectRatioMode.KeepAspectRatio, 
                                 Qt.TransformationMode.SmoothTransformation)
            
            self.qr_label.setPixmap(scaled)
            self.qr_label.setText("")  # Clear any previous text
            
            print(f"QR Data: {data}")
            
        except Exception as e:
            self.qr_label.setText(f"❌ Error: {str(e)}")

    def save_qr(self):
        pixmap = self.qr_label.pixmap()
        if pixmap:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save QR Code", f"{self.ssid_edit.text() or 'wifi'}_qr.png", "PNG Files (*.png)"
            )
            if filename:
                pixmap.save(filename, "PNG")
        else:
            self.qr_label.setText("⚠️ Generate QR first!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application icon for taskbar (Windows)
    icon_path = "ico.ico"
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = WiFiQRApp()
    window.show()
    sys.exit(app.exec())
