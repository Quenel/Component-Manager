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

from EditItemDialog import EditItemDialog




class ViewItemDialog(QDialog):
    def __init__(self, id, name, model, description, datasheet, image, qty, storage_location, purchase_place, project, ordered, price_per_unit, used_part):
        super().__init__()
        self.setWindowTitle("View Item")
        self.setWindowModality(Qt.ApplicationModal)

        self.id = id
        self.name = name  # Store the 'name' parameter as an instance variable
        self.model = model  # Store the 'model' parameter as an instance variable
        self.qty = qty  # Store the 'qty' parameter as an instance variable
        self.storage_location = storage_location  # Store the 'storage_location' parameter as an instance variable
        self.ordered = ordered  # Store the 'ordered' parameter as an instance variable
        self.datasheet = datasheet  # Store the 'datasheet' parameter as an instance variable
        self.description = description  # Store the 'description' parameter as an instance variable
        self.image_path = image  # Store the 'image_path' parameter as an instance variable
        self.purchase_place = purchase_place  # Store the 'purchase_place' parameter as an instance variable
        self.project = project  # Store the 'project' parameter as an instance variable
        self.price_per_unit = str(price_per_unit)
        
        self.used_part = used_part


        layout = QVBoxLayout(self)

        label_id = QLabel(F"ID: {id}")
        layout.addWidget(label_id)

        if self.ordered == 1:  # Check if ordered is equal to 1
            label_ordered = QLabel("On Order")
            label_ordered.setStyleSheet("background-color: yellow; color: black; font-weight: bold;")
            layout.addWidget(label_ordered)
            received_button = QPushButton("Item Received")  # Add the "Item Received" button
            received_button.clicked.connect(self.mark_item_received)  # Connect the button to the mark_item_received method
            layout.addWidget(received_button)

        label_name = QLabel(f"Name: {name}")
        layout.addWidget(label_name)

        label_model = QLabel(f"Model: {model}")
        layout.addWidget(label_model)

        label_qty = QLabel(f"Qty: {qty}")
        layout.addWidget(label_qty)

        label_storage_location = QLabel(f"Storage Location: {storage_location}")
        layout.addWidget(label_storage_location)

        label_project = QLabel(f"Project: {project}")
        layout.addWidget(label_project)

        label_purchase_place = QLabel(f"Purchase Place: {purchase_place}")
        layout.addWidget(label_purchase_place)

        label_price_per_unit = QLabel(f"Purchase Price: ${price_per_unit} (Per unit)")
        layout.addWidget(label_price_per_unit)


        label_description = QLabel(f"Description: {description}")
        layout.addWidget(label_description)


        if self.used_part == 1:
             label_used_part = QLabel("Used Part!")
             layout.addWidget(label_used_part)





        open_button = QPushButton("Open Datasheet")
        open_button.clicked.connect(self.open_datasheet)
        layout.addWidget(open_button)




        edit_button = QPushButton("Edit Info")
        edit_button.clicked.connect(self.edit_info)
        edit_button.setStyleSheet("background-color: green;")
        layout.addWidget(edit_button)



        delete_button = QPushButton("Delete Item")
        delete_button.clicked.connect(self.delete_item)
        delete_button.setStyleSheet("background-color: red;")
        layout.addWidget(delete_button)



        self.datasheet = datasheet
        self.description = description
        self.image_path = image
        self.purchase_place = purchase_place
        self.project = project


    def open_datasheet(self):
        if self.datasheet and os.path.isfile(self.datasheet) and self.datasheet.endswith('.pdf'):
            try:
                url = QUrl.fromLocalFile(self.datasheet)
                QDesktopServices.openUrl(url)
            except Exception:
                QMessageBox.warning(self, "Error", "Failed to open the datasheet.")
        else:
            QMessageBox.warning(self, "Error", "Invalid or non-PDF datasheet file.")


    def delete_item(self):
            conn = sqlite3.connect('database.db')  # Establish a new connection here
            c = conn.cursor()  # Create a new cursor object
            confirm = QMessageBox.question(
                self, "Delete Item", "Are you sure you want to delete this item?", QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                c.execute("DELETE FROM items WHERE Name = ?", (self.name,))
                conn.commit()
                self.accept()






    def edit_info(self):
        # Create an instance of the EditItemDialog and pass the current item's information
        edit_dialog = EditItemDialog(self.id, self.name, self.model, self.description, self.datasheet, self.image_path,
                                    self.qty, self.storage_location, self.purchase_place, self.project,
                                    self.ordered, self.price_per_unit, self.used_part)
        if edit_dialog.exec_() == QDialog.Accepted:
            # Update the instance variables with the edited values
            self.id = edit_dialog.id
            self.name = edit_dialog.name
            self.model = edit_dialog.model
            self.qty = edit_dialog.qty
            self.storage_location = edit_dialog.storage_location
            self.ordered = edit_dialog.ordered
            self.datasheet = edit_dialog.datasheet
            self.description = edit_dialog.description
            self.image_path = edit_dialog.image_path
            self.purchase_place = edit_dialog.purchase_place
            self.project = edit_dialog.project
            self.price_per_unit = edit_dialog.price_per_unit
            self.used_part = edit_dialog.used_part


    def mark_item_received(self):
            conn = sqlite3.connect('database.db')  # Establish a new connection here
            c = conn.cursor()  # Create a new cursor object
            confirm = QMessageBox.question(
                self, "Item Received", "Has the item been received?", QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                c.execute("UPDATE items SET Ordered = 0 WHERE Name = ?", (self.name,))
                conn.commit()
                self.accept()


        