# data_processing.py

from tqdm import tqdm
import time

def process_data(data, progress=True):
    """
    Process data with an optional progress bar.
    """
    processed_data = []
    if progress:
        for value in tqdm(data, desc="Processing data", unit="item"):
            time.sleep(0.1)  # Simulate processing time
            processed_data.append(float(value))
    else:
        processed_data = [float(value) for value in data]
    return processed_data

def load_data_from_file(file_path):
    """
    Load X and Y values from a CSV file.
    The file should have two columns: X and Y.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        x_values = []
        y_values = []
        for line in lines:
            x, y = line.strip().split(',')
            x_values.append(x)
            y_values.append(y)
        return x_values, y_values
    except Exception as e:
        print(f"Error loading data from file: {e}")
        return [], []
