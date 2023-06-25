import sqlite3
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy, QDialog, QLabel, QDialogButtonBox, QMessageBox, QCheckBox, QFileDialog
from PyQt5.QtGui import QColor, QImage, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer
import sys
import os
import shutil
import subprocess
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QTextEdit

from AddItemDialog import AddItemDialog
from ViewItemDialog import ViewItemDialog
import csv




# Create the SQLite database connection
conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS items
             (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
             Name TEXT, 
             Model TEXT, 
             Description TEXT, 
             Datasheet TEXT, 
             Image TEXT, 
             Qty INTEGER, 
             Storage_Location TEXT, 
             Purchase_Place TEXT, 
             Project TEXT, 
             Ordered INTEGER, 
             Price_Per_Unit INTEGER, 
             Used_Part INTEGER)''')

app = QApplication(sys.argv)


# Set the application icon
app_icon_path = "icon.PNG"
app_icon = QIcon(app_icon_path)
app.setWindowIcon(app_icon)


























class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Component Manager")
        self.resize(1400, 600)
    
        # Create a central widget and set it as the main window's central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a horizontal layout manager for the main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Create a widget for the left side
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        # Create a QTableWidget to display the database entries
        self.table_widget = QTableWidget()
        left_layout.addWidget(self.table_widget)

        # Adjust the column widths to stretch and fill the available space
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Create a custom widget for the right side
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)


        # # Create a QLineEdit for the text box
        # self.text_box = QLineEdit()
        # self.text_box.textChanged.connect(self.search_items)
        # right_layout.addWidget(self.text_box)

        # # Create buttons and add them to the right layout
        # button1 = QPushButton("Search Item")
        # button1.clicked.connect(self.search_items)
        # right_layout.addWidget(button1)

# Create a QLabel to display the image
        image_label = QLabel()
        pixmap = QPixmap("logo.PNG")  # Load the image
        scaled_pixmap = pixmap.scaled(600, 300, Qt.AspectRatioMode.KeepAspectRatio)  # Resize the image
        image_label.setPixmap(scaled_pixmap)  # Set the image pixmap
        right_layout.addWidget(image_label)

        # Create a spacer item to maintain spacing between the buttons
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout.addWidget(spacer)




        # Create a QLineEdit for the text box
        self.text_box = QLineEdit()
        self.text_box.textChanged.connect(self.search_items)
        right_layout.addWidget(self.text_box)


        # Create the refresh button
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_items)
        right_layout.addWidget(refresh_button)

            # Create the export button
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)
        right_layout.addWidget(export_button)

        button2 = QPushButton("Add New Item")
        button2.clicked.connect(self.show_add_item_dialog)
        right_layout.addWidget(button2)

        # Set the stretch factor for the left and right widgets
        main_layout.addWidget(left_widget, 2)
        main_layout.addWidget(right_widget, 1)

        self.load_data()


    def load_data(self, search_term=None):
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)

            query = "SELECT ID, Name, Model, Qty, Storage_Location, Ordered FROM items"
            if search_term:
                   query += f" WHERE Name LIKE '%{search_term}%' OR Model LIKE '%{search_term}%' OR Description LIKE '%{search_term}%'"

            
            c.execute(query)
            data = c.fetchall()

            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(6)
            self.table_widget.setHorizontalHeaderLabels(
                ["ID", "Name", "Model", "Qty", "Storage Location", "", "Ordered"])
            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            for row, item in enumerate(data):
                for col, value in enumerate(item):
                    item_widget = QTableWidgetItem(str(value))
                    self.table_widget.setItem(row, col, item_widget)

                    if col == 3 and item[5] == 1:
                        item_widget.setBackground(QColor("yellow"))
                        item_widget.setText(f"{item[3]} (On Order)")

                view_button = QPushButton("View")
                view_button.setStyleSheet("background-color: blue; color: white;")
                view_button.clicked.connect(lambda _, r=row: self.view_item(r))
                self.table_widget.setCellWidget(row, 5, view_button)
            

    def show_add_item_dialog(self):
        dialog = AddItemDialog()
        if dialog.exec_() == QDialog.Accepted:
            item_data = dialog.get_item_data()
            self.add_item(*item_data, dialog.datasheet if hasattr(dialog, 'datasheet') else '')


    

    def add_item(self, name, model, qty, storage_location, price_per_unit, description, project, ordered, purchase_price_input, used_part,  place_of_purchase, datasheet=None):
        c.execute(
            "INSERT INTO items (Name, Model, Qty, Storage_Location, Price_per_unit, Description, Project, Ordered, Price_Per_Unit, Used_Part, Purchase_Place, Datasheet) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, model, qty, storage_location, price_per_unit, description, project, ordered, purchase_price_input, used_part,  place_of_purchase, datasheet))
        conn.commit()
        self.load_data()



    def view_item(self, row):
        item_id_text = self.table_widget.item(row, 0).text()
        if item_id_text:
            try:
                item_id = int(item_id_text)
            except ValueError:
                QMessageBox.warning(self, "Invalid ID", "Invalid ID value.")
                return
        else:
            QMessageBox.warning(self, "Invalid ID", "Empty ID value.")
            return
        c.execute(
            "SELECT ID, Name, Model, Description, Datasheet, Image, Qty, Storage_Location, Purchase_Place, Project, Ordered, Price_Per_Unit, Used_Part FROM items WHERE ID = ?",
            (item_id,))
        item_info = c.fetchone()
        id, name, model, description, datasheet, image, qty, storage_location, purchase_place, project, ordered, price_per_unit, used_part = item_info if item_info else (
        "", "", "", "", "", "", "", "", "", "", "", "", "", "")
        #print(item_info)
        #print(name)



        dialog = ViewItemDialog(id, name, model, description, datasheet, image, qty, storage_location, purchase_place, project, ordered, price_per_unit, used_part)
        
        dialog.setGeometry(100, 100, 600, 400)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()


    def refresh_items(self):
            self.load_data("")
        
    def search_items(self):
            search_term = self.text_box.text()
            self.load_data(search_term)





    def export_to_csv(self):
        # Get all the data from the database
        c.execute("SELECT * FROM items")
        data = c.fetchall()

        # Get the column names
        column_names = [column[0] for column in c.description]

        # Combine column names and data into a list of rows
        rows = [column_names] + data

        # Open a file dialog to choose the save location
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save as CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, "w", newline="") as csvfile:
                    csv_writer = csv.writer(csvfile)
                    # Write the rows to the CSV file
                    csv_writer.writerows(rows)
                QMessageBox.information(self, "Export Successful", "Data exported to CSV successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Export Failed", f"Failed to export data to CSV:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Export Cancelled", "Export to CSV cancelled.")



 

c.execute('''CREATE TABLE IF NOT EXISTS items
             (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
             Name TEXT, 
             Model TEXT, 
             Description TEXT, 
             Datasheet TEXT, 
             Image TEXT, 
             Qty INTEGER, 
             Storage_Location TEXT, 
             Purchase_Place TEXT, 
             Project TEXT, 
             Ordered INTEGER, 
             Price_Per_Unit INTEGER, 
             Used_Part INTEGER)''')


# Create and show the main window
window = MainWindow()
window.show()

# Start the event loop
sys.exit(app.exec_())