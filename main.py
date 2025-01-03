import xml.etree.ElementTree as ET
import json
import tkinter as tk
from tkinter import filedialog, messagebox

def xml_to_dict(element):
    """
    Recursively converts an XML element and its children into a dictionary.
    """
    result = {}
    if element.text and element.text.strip():
        result["text"] = element.text.strip()

    # Include attributes as child objects
    if element.attrib:
        for key, value in element.attrib.items():
            result[key] = value

    for child in element:
        child_result = xml_to_dict(child)
        if child.tag not in result:
            result[child.tag] = child_result
        else:
            # If the tag is already in the result, make it a list
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_result)

    return result

def convert_xml_to_json(xml_string):
    """
    Converts an XML string to JSON.
    """
    try:
        root = ET.fromstring(xml_string)
        xml_dict = {root.tag: xml_to_dict(root)}
        return json.dumps(xml_dict, indent=4)
    except ET.ParseError as e:
        return f"Error parsing XML: {e}"

def select_file():
    """Open a file dialog to select an XML file."""
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                xml_content = file.read()
                json_result = convert_xml_to_json(xml_content)

                # Save JSON result to file
                save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
                if save_path:
                    with open(save_path, "w") as json_file:
                        json_file.write(json_result)
                        messagebox.showinfo("Success", f"JSON file saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def create_ui():
    """Create a simple UI for the XML to JSON converter."""
    root = tk.Tk()
    root.title("XML to JSON Converter")

    select_button = tk.Button(root, text="Select XML File", command=select_file)
    select_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_ui()
