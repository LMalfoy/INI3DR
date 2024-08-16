import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Function to read XML file and extract data
def read_xml_and_plot(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract x and y values from the XML
    x_values = []
    y_values = []

    for coordinate in root.findall('coordinate'):
        x = float(coordinate.find('x').text)
        y = float(coordinate.find('y').text)
        x_values.append(x)
        y_values.append(y)

    # Plotting the data
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, color='black', label='Corrected')

    # Adding the red horizontal line at y = 0.143
    plt.axhline(y=0.143, color='red', linestyle='--', label='FSC gold standard')

    # Customizing the axes
    plt.xlabel("Resolution (1/Angstrom)")
    plt.ylabel("Fourier Shell Correlation")
    plt.title("Final resolution = 2.7 Angstroms")

    # Set axis limits and ticks
    plt.xlim(0.0, 0.6)
    plt.ylim(-0.2, 1.2)
    plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    plt.yticks([-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2])

    # Adding the legend
    plt.legend()

    # Display the plot
    plt.grid(True)
    plt.show()

# File path to the XML file
file_path = 'postprocess_fsc.xml'

# Call the function with the file path
read_xml_and_plot(file_path)
