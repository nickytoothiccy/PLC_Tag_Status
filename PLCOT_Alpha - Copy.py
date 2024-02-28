from pylogix import PLC
import sys
import pandas as pd
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QMainWindow, QWidget, QRadioButton, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QComboBox, QMessageBox, QAction

class TAG():
    def __init__(self, name, data_type, value):
        self.name = name
        self.data_type = data_type
        self.value = value

class Controller():
    def __init__(self, plc_path):
        self.comm = PLC(plc_path)

    def read_all_tags(self):
        with self.comm as plc:
            tag_list = plc.GetTagList()

        return tag_list

class GUI(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("PLC Tag Status")
        self.setGeometry(100, 100, 800, 600)

        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

        self.update_table(df)

    def update_table(self, df):
        self.table_widget.setRowCount(len(df))
        self.table_widget.setColumnCount(len(df.columns))
        self.table_widget.setHorizontalHeaderLabels(df.columns)

        for i, row in enumerate(df.values):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(i, j, item)

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()


def main():
    # Create an instance of the PLC class
    plc = Controller("10.42.110.39")  # Replace with the actual PLC IP address
    # Read all tags
    tags = []
    tagReadData = plc.read_all_tags()
    # Sort tags by data_type
    for i in tagReadData.Value:
        if 'Program:' in i.TagName:
            tags.append(TAG(i.TagName, i.DataType, ''))

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
    
    app = QApplication(sys.argv)
    window = GUI(df)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

   
