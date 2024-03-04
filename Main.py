import sys
import pandas as pd
from PyQt5.QtWidgets import *
# In main.py
from GUI import mainWindow, PopUp
from Controller import ControllerPycomm3, Tag
# Import other necessary modules

class main():
    def __init__(self):
        # Launch the pop-up window
        self.app = QApplication([])
        self.window = PopUp()
        self.connectBtn = self.window.button
        self.connectBtn.clicked.connect(self.whoConnect)
        self.window.show()
        sys.exit(self.app.exec_())
    
    def whoConnect(self):
        # Connect to the controller
        self.ip = self.window.textbox.text()
        self.plc = ControllerPycomm3(self.ip)
        self.window.close()
        self.launchMainWindow()
    
    def launchMainWindow(self):
        # Launch the main window
        self.window = mainWindow(self.plc)
        self.window.tagDataButton.clicked.connect(self.launchTagWindow)
        self.window.show()
    
    def launchTagWindow(self):

          # Read all tags
        tags = []
        tagReadData = self.plc.readAllTags()
        # get all controller tags
        pid_tags = [
            tag
            for tag, _def in tagReadData.items()
            if _def['data_type_name'] == 'PID'
        ]
        print(pid_tags)
        # # Sort tags by dataType
        # for i in tagReadData.Value:
        #     if 'Program:' in i.TagName:
        #         temp = plc.readTagValue(i.TagName)
        #         if temp is None:
        #             temp = 'None'
        #         tags.append(Tag(i.TagName, i.DataType, temp))

        # sortedTags = sorted(tags, key=lambda tag: tag.dataType, reverse=True)

        # # Convert the sortedTags list into a dictionary
        # tagDict = {
        #     'Tag Name': [tag.name for tag in sortedTags],
        #     'Data Type': [tag.dataType for tag in sortedTags],
        #     'Value': [tag.value for tag in sortedTags]
        # }

        # # Create a DataFrame from the tagDict
        # df = pd.DataFrame(tagDict)

        # # Launch the tag window
        # self.window.stackedWidget.setCurrentIndex(1)
        # self.tagWindow.show()

if __name__ == "__main__":
    main() 