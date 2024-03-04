from Controller import ControllerPycomm3, Tag
from io import StringIO
def main():
    user_input = input("Enter your input: ")
    while True:
        try:
            # Check if the input format is correct
            parts = user_input.split('.')
            if len(parts) != 4 or any(not part.isdigit() or not 0 <= int(part) <= 255 for part in parts):
                raise ValueError("Invalid input format. Please enter in the format xxx.xxx.xxx.xxx")
            break
        except ValueError as e:
            print(e)
            user_input = input("Enter your input again: ")
    gatherCM(user_input)

def gatherCM(ipAddress):
    # Connect to the controller
    plc = ControllerPycomm3(ipAddress)
    # Read all tags
    tags = []
    tagReadData = plc.readAllTags()
def gatherCM(ipAddress):
    # Connect to the controller
    plc = ControllerPycomm3(ipAddress)
    # Read all tags
    tags = []
    tagReadData = plc.readAllTags()
    # # Filter tags containing 'YV' in their names
    # yv_tags = [tag for tag in tagReadData if 'YV' in tag['tag_name']]
    # Extract only tag names
    tag_names = [tag['tag_name'] for tag in tagReadData if 'YV' or 'FQI' in tag['tag_name']]

    # Filter tags based on criteria
    filtered_tags = [tag_name for tag_name in tag_names if tag_name.startswith('YV_') and tag_name[3:].isdigit() and len(tag_name) == 8]

    # call the generate function
    generateDevTool(filtered_tags)

def generateDevTool(filtered_tags):
    """
    Generates a devTool based on the provided filtered_tags.

    Args:
        filtered_tags (list): A list of tag names to be included in the devTool.

    Returns:
        str: The generated devTool as a string.
    """
    # Generate the devTool
    text_object = StringIO()
    
    # we will start with fault reset and fault acknowledge
    # Append new lines to the text object
    text_object.write("// Clear all CM Faults" + '\n')
    text_object.write("if dev_clearFault then" + '\n')
    for tag_name in filtered_tags:
        text_object.write("     " + tag_name + ".PCmd_Reset := 1;" '\n')
    text_object.write("end_if;" + '\n' + '\n')
    # now for all cms in operator lock
    text_object.write("// Set all CMs to Operator Lock" + '\n')
    text_object.write("if dev_oprLock then" + '\n')
    for tag_name in filtered_tags:
        text_object.write("     " + tag_name + ".PCmd_Oper := 1;" '\n')
    text_object.write("end_if;" + '\n' + '\n')
    # now for all cms in program lock
    text_object.write("// Set all CMs to Program Lock" + '\n')
    text_object.write("if dev_progLock then" + '\n')
    for tag_name in filtered_tags:
        text_object.write("     " + tag_name + ".PCmd_Prog := 1;" '\n')
    text_object.write("end_if;" + '\n' + '\n')
    # Get the generated devTool as a string
    dev_tool = text_object.getvalue()
    
    # Close the text object
    text_object.close()
    
    # Use the generated devTool as needed
    print(dev_tool)

if __name__ == "__main__":
    main() 