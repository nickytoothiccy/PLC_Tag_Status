from pycomm3 import LogixDriver
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
            # get additional info
            self.name = plc.get_plc_name()
        return data