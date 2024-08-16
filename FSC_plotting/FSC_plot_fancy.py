import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

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

    # Convert lists to numpy arrays for easier calculation
    x_values = np.array(x_values)
    y_values = np.array(y_values)

    # Find the intersection point where y = 0.143
    y_target = 0.143

    # Find the index where the curve crosses y_target
    idx = np.where(np.diff(np.sign(y_values - y_target)))[0]

    if len(idx) > 0:
        idx = idx[0]  # Take the first crossing point
        # Linear interpolation to find the exact intersection point
        x_intersection = x_values[idx] + (y_target - y_values[idx]) * (x_values[idx + 1] - x_values[idx]) / (y_values[idx + 1] - y_values[idx])
    else:
        x_intersection = None

    # Plotting the data
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, color='black', label='Corrected')

    # Plot the red horizontal line up to the intersection point
    if x_intersection is not None:
        plt.hlines(y=y_target, xmin=0, xmax=x_intersection, color='gold', linestyle='--', label='Gold standard FSC')

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
