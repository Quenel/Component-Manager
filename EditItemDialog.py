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






class EditItemDialog(QDialog):
    
    def __init__(self,id, name, model, description, datasheet, image_path, qty, storage_location, purchase_place, project, ordered, price_per_unit, used_part):
        super().__init__()
        self.setWindowTitle("Edit Item")
        self.setWindowModality(Qt.ApplicationModal)
        self.id = id
        self.name = name
        self.model = model
        self.qty = qty
        self.storage_location = storage_location
        self.ordered = ordered
        self.datasheet = datasheet
        self.description = description
        self.image_path = image_path
        self.purchase_place = purchase_place
        self.project = project
        self.price_per_unit = price_per_unit
        self.used_part = used_part

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit(name)
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Model:"))
        self.model_input = QLineEdit(model)
        layout.addWidget(self.model_input)

        layout.addWidget(QLabel("Quantity:"))
        self.qty_input = QLineEdit()
        self.qty_input.setText(str(qty))
        layout.addWidget(self.qty_input)

        layout.addWidget(QLabel("Storage Location:"))
        self.storage_input = QLineEdit(storage_location)
        layout.addWidget(self.storage_input)

        layout.addWidget(QLabel("Purchase Place:"))
        self.purchase_input = QLineEdit(purchase_place)
        layout.addWidget(self.purchase_input)

        layout.addWidget(QLabel("Price per Unit:"))
        self.price_per_unit_input = QLineEdit(price_per_unit)
        layout.addWidget(self.price_per_unit_input)

        layout.addWidget(QLabel("Project:"))
        self.project_input = QLineEdit(project)
        layout.addWidget(self.project_input)

        layout.addWidget(QLabel("Description:"))
        self.description_input = QTextEdit(description)
        layout.addWidget(self.description_input)

        layout.addWidget(QLabel("Ordered:"))
        self.ordered_checkbox = QCheckBox()
        self.ordered_checkbox.setChecked(ordered == 1)
        if (ordered == 1):
            self.ordered_checkbox.setChecked(True)  # Set the checkbox as marked
        layout.addWidget(self.ordered_checkbox)


        layout.addWidget(QLabel("Used Part:"))
        self.used_part_checkbox = QCheckBox()
        self.used_part_checkbox.setChecked(used_part==1)
        if (used_part == 1):
            self.used_part_checkbox.setChecked(True)
        layout.addWidget(self.used_part_checkbox)




        layout.addWidget(QLabel("Datasheet:"))
        self.datasheet_button = QPushButton("Change Datasheet")
        self.datasheet_button.clicked.connect(self.change_datasheet)
        layout.addWidget(self.datasheet_button)




        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def change_datasheet(self):
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
                self.datasheet_button.setText("Datasheet Changed")
                self.datasheet = target_path
            except OSError:
                QMessageBox.warning(self, "Error", "Failed to change the datasheet.")
        else:
            QMessageBox.warning(self, "Error", "No datasheet selected.")

    def accept(self):
        # Get the updated item data from the input fields
        
        updated_name = self.name_input.text()
        updated_model = self.model_input.text()
        updated_qty = self.qty_input.text()
        updated_storage_location = self.storage_input.text()
        updated_ordered = 1 if self.ordered_checkbox.isChecked() else 0
        updated_description = self.description_input.toPlainText()
        updated_datasheet = self.datasheet
        updated_purchase_place = self.purchase_input.text()
        updated_project = self.project_input.text()
        updated_price_per_unit = float(self.price_per_unit_input.text()) if self.price_per_unit_input.text() else 0.0
        updated_used_part = 1 if self.used_part_checkbox.isChecked() else 0



        # Update the item in the database with the new information
        # Assuming you have a function called 'update_item' that updates the item in the database
        update_item(self.id, updated_name, updated_model, updated_qty, updated_storage_location,
                    updated_ordered, updated_description, updated_datasheet, updated_purchase_place, updated_project, updated_price_per_unit, updated_used_part)

        # Close the dialog
        self.close()


def update_item(id, updated_name, updated_model, updated_qty, updated_storage_location, updated_ordered,
                updated_description, updated_datasheet, updated_purchase_place, updated_project, updated_price_per_unit, updated_used_part):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Update the item in the database using SQL UPDATE statement
    c.execute('''UPDATE items SET Name = ?, Model = ?, Qty = ?, Storage_Location = ?, Ordered = ?,
                 Description = ?, Datasheet = ?, Purchase_Place = ?, Project = ?, Price_Per_Unit = ?, Used_Part = ? WHERE ID = ?''',
              (updated_name, updated_model, updated_qty, updated_storage_location, updated_ordered,
               updated_description, updated_datasheet, updated_purchase_place, updated_project,updated_price_per_unit,updated_used_part, id))

    conn.commit()
    conn.close()