from pycomm3 import LogixDriver
import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Global variable
ipAddress = ''

class Tag():
    def __init__(self, name, dataType, value):
        self.name = name
        self.dataType = dataType
        self.value = value 

class ControllerPycomm3():
    def __init__(self, plcPath):
        self.comm = LogixDriver(plcPath)
        self.vendor = ''
        self.productType = ''
        self.productCode = ''
        self.revision = ''
        self.status = ''
        self.serial = ''
        self.productName = ''
        self.keyswitch = ''
        self.name = ''
        self.programs = []
        self.tasks = []
        self.modules = []
        # read the controller data
        self.getControllerData()

    def readAllTags(self):
        # Read all tags in the controller
        with self.comm as plc:
            tagList = plc.get_tag_list()

        return tagList

    def readTagValue(self, tagName):
        with self.comm as plc:
            try:
                response = plc.read(tagName)
                value = response.value
                return value
            except:
                return ''
                
    def getControllerData(self):
        # Read controller data here
        with self.comm as plc:
            # get standard controller info
            data = plc.get_plc_info()
            self.vendor = data.get('vendor', '')
            self.productType = data.get('product_type', '')
            self.productCode = data.get('product_code', '')
            self.revision = data.get('revision', '')
            self.status = data.get('status', '')
            self.serial = data.get('serial', '')
            self.productName = data.get('product_name', '')
            self.keyswitch = data.get('keyswitch', '')

            self.name = data.get('name', '')
            self.programs = list(data.get('programs', {}).keys())
            self.tasks = list(data.get('tasks', {}).keys())
            self.modules = list(data.get('modules', {}).keys())
        return data

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
        self.button.clicked.connect(self.connectToController)

    def connectToController(self):
        ipAddress = self.textbox.text()
        # Create an instance of the PLC class
        # go to the main instruction
        self.close()
        MainApp.readController(MainApp, ipAddress)

class GUI(QMainWindow):
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
        self.programsLabel = QLabel(f"<font color='black'>Programs:</font>")
        self.tasksLabel = QLabel(f"<font color='black'>Tasks:</font>")
        self.modulesLabel = QLabel(f"<font color='black'>Modules:</font>")
        
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
        self.programsValueLabel = QLabel(f"<font color='red'>{', '.join(plc.programs)}</font>")
        self.tasksValueLabel = QLabel(f"<font color='red'>{', '.join(plc.tasks)}</font>")
        self.modulesValueLabel = QLabel(f"<font color='red'>{', '.join(plc.modules)}</font>")
        
        # Create a button to the right side that says "Tag Data"
        self.tagDataButton = QPushButton("Tag Data")
        self.tagDataButton.setStyleSheet("font-size: 16px;")
        self.tagDataButton.clicked.connect(self.showTagData)    
        
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
        self.page1Layout.addWidget(self.programsLabel)
        self.page1Layout.addWidget(self.programsValueLabel)
        self.page1Layout.addWidget(self.tasksLabel)
        self.page1Layout.addWidget(self.tasksValueLabel)
        self.page1Layout.addWidget(self.modulesLabel)
        self.page1Layout.addWidget(self.modulesValueLabel)
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

class MainApp(object):
    """
    The MainApp class represents the main application for the PLC Tag Status program.
    It initializes the application, launches a pop-up window, and handles the loading and display of tag data.
    """

    def __init__(self):
        """
        Initializes the MainApp object.

        Parameters:
        None

        Returns:
        None
        """
        # Launch the pop-up window
        app = QApplication([])
        self.window = PopUp()
        self.window.show()
        sys.exit(app.exec_())

    def loadAllTagData(self, plc):
        """
        Loads all tag data from the PLC and displays it in a GUI.

        Parameters:
        - plc (PLC): The PLC object used to read tag data.

        Returns:
        None
        """
        
        # Read all tags
        tags = []
        tagReadData = plc.readAllTags()
        
        # Sort tags by dataType
        for i in tagReadData.Value:
            if 'Program:' in i.TagName:
                temp = plc.readTagValue(i.TagName)
                if temp is None:
                    temp = 'None'
                tags.append(Tag(i.TagName, i.DataType, temp))

        sortedTags = sorted(tags, key=lambda tag: tag.dataType, reverse=True)

        # Convert the sortedTags list into a dictionary
        tagDict = {
            'Tag Name': [tag.name for tag in sortedTags],
            'Data Type': [tag.dataType for tag in sortedTags],
            'Value': [tag.value for tag in sortedTags]
        }

        # Create a DataFrame from the tagDict
        df = pd.DataFrame(tagDict)

        self.window = GUI(df)
        self.window.show()

    def readController(self, plc_address):
        """
        Reads controller data from the PLC and prints it.

        Parameters:
        - plc (PLC): The PLC object used to read controller data.

        Returns:
        None
        """
        # create a controller object``
        self.processor = ControllerPycomm3(plc_address)

        self.window = GUI(self.processor)
        self.window.show()

if __name__ == "__main__":
    app = MainApp()
    app.main()
