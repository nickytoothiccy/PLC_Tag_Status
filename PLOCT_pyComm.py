from pycomm3 import LogixDriver

class Tag:
    def __init__(self, name, data_type, value):
        self.name = name
        self.data_type = data_type
        self.value = value

# Connect to the PLC
plcPath = "10.42.110.39"
# Check the connection with try command
try:
    with LogixDriver(path=plcPath) as plc:
        # Read all tags
        tags = plc.get_tag_list()
        # list of tags
        tag_instances = []
        # dictionary of tags
        tag_groups = {}

        # read all tags and sort them by data type
        for tag in tags:
            response = plc.read(tag)
            tag_instance = Tag(response.tag, response.type, response.value)
            tag_instances.append(tag_instance)
            # group tags by data type if doesn't already exist
            if response.type not in tag_groups:
                tag_groups[response.type] = []

            tag_groups[response.type].append(tag_instance)

        # Print # of tag groups
        print(f"Number of tag groups: {len(tag_groups)}")
        # Print tag groups
        for data_type, tag_group in tag_groups.items():
            print(f"Data Type: {data_type}")
            for tag_instance in tag_group:
                print(f"Tag: {tag_instance.tag_name}, Value: {tag_instance.value}")
        

except:
    print("PLC connection failed")
    exit()
