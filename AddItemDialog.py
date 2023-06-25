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



class AddItemDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Item")
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout(self)

        self.name_input = QLineEdit()
        self.model_input = QLineEdit()
        self.qty_input = QLineEdit()
        self.storage_input = QLineEdit()
        self.price_per_unit_input = QLineEdit()
        self.description_input = QTextEdit()
        self.project_input = QLineEdit()
        self.purchase_input = QLineEdit()
        self.ordered_checkbox = QCheckBox("Part has been ordered")
        self.used_part_checkbox = QCheckBox("Part is used")
        self.image_button = QPushButton("Add Image")
        self.image_button.clicked.connect(self.add_image)
        self.datasheet_button = QPushButton("Add Datasheet")
        self.datasheet_button.clicked.connect(self.add_datasheet)


        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Model:"))
        layout.addWidget(self.model_input)

        layout.addWidget(QLabel("Quantity:"))
        layout.addWidget(self.qty_input)

        layout.addWidget(QLabel("Storage Location:"))
        layout.addWidget(self.storage_input)

        layout.addWidget(QLabel("Purchase Place:"))
        self.purchase_input = QLineEdit()
        self.purchase_input.setText("AliExpress")
        layout.addWidget(self.purchase_input)

        layout.addWidget(QLabel("Price per Unit:"))
        layout.addWidget(self.price_per_unit_input)

        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)

        layout.addWidget(QLabel("Project:"))
        layout.addWidget(self.project_input)

        layout.addWidget(self.ordered_checkbox)
        layout.addWidget(self.used_part_checkbox)
        layout.addWidget(self.image_button)
        layout.addWidget(self.datasheet_button)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_item_data(self):
        name = self.name_input.text()
        model = self.model_input.text()
        qty = self.qty_input.text()
        storage_location = self.storage_input.text()
        price_per_unit = self.price_per_unit_input.text()
        description = self.description_input.toPlainText()
        project = self.project_input.text()
        ordered = int(self.ordered_checkbox.isChecked())
        purchase_price_input = self.purchase_input.text()
        used_part = int(self.used_part_checkbox.isChecked())
        place_of_purchase = self.purchase_input.text()

        return name, model, qty, storage_location, price_per_unit, description, project, ordered, purchase_price_input, used_part, place_of_purchase
    
    

    def add_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            try:
                self.image = QPixmap(file_path)
                self.image_button.setText("Image Added")
                self.image_button.setEnabled(False)
            except Exception:
                QMessageBox.warning(self, "Error", "Failed to add the image.")
        else:
            QMessageBox.warning(self, "Error", "No image selected.")

    def add_datasheet(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Datasheet", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            folder_path = "datasheets"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            datasheet_file = os.path.basename(file_path)
            target_path = os.path.join(folder_path, datasheet_file)
            try:
                shutil.copy(file_path, target_path)
                self.datasheet_button.setText("Datasheet Added")
                self.datasheet_button.setEnabled(False)
                self.datasheet = target_path
            except OSError:
                QMessageBox.warning(self, "Error", "Failed to add the datasheet.")
        else:
            QMessageBox.warning(self, "Error", "No datasheet selected.")