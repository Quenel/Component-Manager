import sqlite3
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy, QDialog, QLabel, QDialogButtonBox, QMessageBox, QCheckBox, QFileDialog
from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import sys
import os
import shutil
import subprocess
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QTextEdit



class TakePictureDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Take Picture")
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout(self)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(640, 480)
        layout.addWidget(self.image_label)

        self.capture_button = QPushButton("Take Picture")
        self.capture_button.clicked.connect(self.capture_image)
        layout.addWidget(self.capture_button)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.image = None

    def capture_image(self):
        ret, frame = self.camera.read()
        if ret:
            self.image = frame

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def get_image(self):
        return self.image