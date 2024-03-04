from pylogix import PLC
import sys
import pandas as pd
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QMainWindow, QWidget, QRadioButton, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QComboBox, QMessageBox, QAction
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# Global variable
ipAddress = ''
# Thread class for multi-threading
# class WorkerThread(QThread):
#     progress_updated = pyqtSignal()

#     def run(self):
#         for i in range(101):
#             self.progress_updated.emit()
#             self.msleep(50)

class TAG():
    def __init__(self, name, data_type, value):
        self.name = name
        self.data_type = data_type
        self.value = value

class Controller():
    def __init__(self, plc_path):
        self.comm = PLC(plc_path)

    def read_all_tags(self):
        # Read all tags in the controller
        with self.comm as plc:
            tag_list = plc.GetTagList()

        return tag_list

    def readTagValue(self, tagName):
        with self.comm as plc:
            try:
                strLen = plc.Read('{}.LEN'.format(tagName)).Value
                ret = plc.Read('{}.DATA'.format(tagName), int(strLen)).Value
                value = ''.join([chr(d) for d in ret])
                return value
            except:
                return ''

class PopUp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Controller IP")
        self.setGeometry(100, 100, 300, 100)

        self.label = QLabel("Controller IP:", self)
        self.label.move(20, 20)

        self.textbox = QLineEdit(self)
        self.textbox.move(120, 20)
        self.textbox.setText("10.42.110.39")  # Default IP address

        self.button = QPushButton("Connect", self)
        self.button.move(120, 60)
        self.button.clicked.connect(self.connect_to_controller)

    def connect_to_controller(self):
        ipAddress = self.textbox.text()
        # Create an instance of the PLC class
        plc = Controller(ipAddress)
        # go to the main instruction
        self.close()
        MainApp.readController(MainApp,plc)

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading...")
        self.setFixedSize(600, 200)

        self.label = QLabel("Loading...", self)
        self.label.setStyleSheet("font-size: 20px; color: red;")

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.toggle_label)
        # self.timer.start(500)  # Flashing interval in milliseconds

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        # # Create a worker thread
        # self.worker = WorkerThread()
        # # Connect the worker thread's signal to a slot
        # self.worker.progress_updated.connect(self.update_progress)
        # # Start the worker thread
        # self.worker.start()

class GUI(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("PLC Tag Status")
        self.setGeometry(100, 100, 800, 600)

        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)
        
        # Enable sorting
        self.table_widget.setSortingEnabled(True)  # Add this line to enable sorting

        self.update_table(df)

    def update_table(self, df):
        # Temporarily disable sorting to prevent potential performance issues while updating the table
        self.table_widget.setSortingEnabled(False)  # Disable sorting while updating table
        
        self.table_widget.setRowCount(len(df))
        self.table_widget.setColumnCount(len(df.columns))
        self.table_widget.setHorizontalHeaderLabels(df.columns)

        for i, row in enumerate(df.values):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(i, j, item)

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        
        # Re-enable sorting after the table has been updated
        self.table_widget.setSortingEnabled(True)  # Re-enable sorting after updating table

class MainApp(object):
    def __init__(self):
        # Launch the pop-up window
        app = QApplication([])
        self.window = PopUp()
        self.window.show()
        sys.exit(app.exec_())

    def loadAllTagData(self, plc):
        # Create a loading screen
        loading_screen = LoadingScreen()
        loading_screen.show()
        # start the worker thread
        # worker_thread = WorkerThread()
        # worker_thread.progress_updated.connect(loading_screen.update_progress)
        # worker_thread.start()
        # Read all tags
        tags = []
        tagReadData = plc.read_all_tags()
        # Sort tags by data_type
        for i in tagReadData.Value:
            if 'Program:' in i.TagName:
                temp = plc.readTagValue(i.TagName)
                if temp is None:
                    temp = 'None'
                tags.append(TAG(i.TagName, i.DataType, temp))

        sorted_tags = sorted(tags, key=lambda tag: tag.data_type, reverse=True)
        # for x in sorted_tags:
        #     print(f"Tag Name: {x.name}, Data Type: {x.data_type}, Value: {x.value}")

        # Convert the sorted_tags list into a dictionary
        tag_dict = {
            'Tag Name': [tag.name for tag in sorted_tags],
            'Data Type': [tag.data_type for tag in sorted_tags],
            'Value': [tag.value for tag in sorted_tags]
        }

        # Create a DataFrame from the tag_dict
        df = pd.DataFrame(tag_dict)
        loading_screen.close()
        

        self.window = GUI(df)
        self.window.show()

    def readController(self, plc):
        # Print out the controller properties
        for attr in dir(plc):
            if not attr.startswith('__'):  # Ignore built-in attributes
                value = getattr(plc, attr)
                if not callable(value):  # Ignore methods
                    print(f"Attribute: {attr}, Value: {value}")
        

if __name__ == "__main__":
    app = MainApp()
    app.main()



   
