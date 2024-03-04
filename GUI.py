from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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


class mainWindow(QMainWindow):
    def __init__(self, plc):
        super().__init__()
        self.setWindowTitle("Controller Configuration")
        self.setGeometry(100, 100, 800, 600)
        self.stackedWidget = QStackedWidget()
        # First Stack Page
        self.page1 = QWidget()
        self.page1Layout = QVBoxLayout(self.page1)
        self.pageLoaded = False
        
        # Create label descriptors in black
        self.vendorLabel = QLabel(f"<font color='black'>Vendor:</font>")
        self.productTypeLabel = QLabel(f"<font color='black'>Product Type:</font>")
        self.productCodeLabel = QLabel(f"<font color='black'>Product Code:</font>")
        self.revisionLabel = QLabel(f"<font color='black'>Revision:</font>")
        self.statusLabel = QLabel(f"<font color='black'>Status:</font>")
        self.serialLabel = QLabel(f"<font color='black'>Serial:</font>")
        self.productNameLabel = QLabel(f"<font color='black'>Product Name:</font>")
        self.keyswitchLabel = QLabel(f"<font color='black'>Keyswitch:</font>")
        self.nameLabel = QLabel(f"<font color='black'>Name:</font>")

        
        # Create actual labels in red
        self.vendorValueLabel = QLabel(f"<font color='red'>{plc.vendor}</font>")
        self.productTypeValueLabel = QLabel(f"<font color='red'>{plc.productType}</font>")
        self.productCodeValueLabel = QLabel(f"<font color='red'>{plc.productCode}</font>")
        self.revisionValueLabel = QLabel(f"<font color='red'>{plc.revision}</font>")
        self.statusValueLabel = QLabel(f"<font color='red'>{plc.status}</font>")
        self.serialValueLabel = QLabel(f"<font color='red'>{plc.serial}</font>")
        self.productNameValueLabel = QLabel(f"<font color='red'>{plc.productName}</font>")
        self.keyswitchValueLabel = QLabel(f"<font color='red'>{plc.keyswitch}</font>")
        self.nameValueLabel = QLabel(f"<font color='red'>{plc.name}</font>")

        # Create a button to the right side that says "Tag Data"
        self.tagDataButton = QPushButton("Tag Data")
        self.tagDataButton.setStyleSheet("font-size: 16px;")
        
        # Add the labels and button to the layout
        self.page1Layout.addWidget(self.vendorLabel)
        self.page1Layout.addWidget(self.vendorValueLabel)
        self.page1Layout.addWidget(self.productTypeLabel)
        self.page1Layout.addWidget(self.productTypeValueLabel)
        self.page1Layout.addWidget(self.productCodeLabel)
        self.page1Layout.addWidget(self.productCodeValueLabel)
        self.page1Layout.addWidget(self.revisionLabel)
        self.page1Layout.addWidget(self.revisionValueLabel)
        self.page1Layout.addWidget(self.statusLabel)
        self.page1Layout.addWidget(self.statusValueLabel)
        self.page1Layout.addWidget(self.serialLabel)
        self.page1Layout.addWidget(self.serialValueLabel)
        self.page1Layout.addWidget(self.productNameLabel)
        self.page1Layout.addWidget(self.productNameValueLabel)
        self.page1Layout.addWidget(self.keyswitchLabel)
        self.page1Layout.addWidget(self.keyswitchValueLabel)
        self.page1Layout.addWidget(self.nameLabel)
        self.page1Layout.addWidget(self.nameValueLabel)
        self.page1Layout.addWidget(self.tagDataButton)
        # Create the second page with the tag table
        self.page2 = QWidget()
        self.page2Layout = QVBoxLayout(self.page2)

        self.tagTable = QTableWidget()
        self.page2Layout.addWidget(self.tagTable)
        
         # Add the pages to the stacked widget
        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)

        self.setCentralWidget(self.stackedWidget)

    def updateTable(self, df):
        # Temporarily disable sorting to prevent potential performance issues while updating the table
        self.tagTable.setSortingEnabled(False)  # Disable sorting while updating table
        
        self.tagTable.setRowCount(len(df))
        self.tagTable.setColumnCount(len(df.columns))
        self.tagTable.setHorizontalHeaderLabels(df.columns)

        for i, row in enumerate(df.values):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tagTable.setItem(i, j, item)

        self.tagTable.resizeColumnsToContents()
        self.tagTable.resizeRowsToContents()

        # Re-enable sorting after the table has been updated
        self.tagTable.setSortingEnabled(True)  # Re-enable sorting after updating table
    
    def showTagData(self, df):
        self.stackedWidget.setCurrentIndex(1)
        self.updateTable(df)
