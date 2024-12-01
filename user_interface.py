# user_interface.py

import sys

def get_yes_no(prompt, default='no'):
    """
    Prompt the user for a yes/no answer with validation.
    """
    while True:
        choice = input(f"{prompt} (yes/no) [default: {default}]: ").strip().lower()
        if not choice and default:
            choice = default
        if choice in ['yes', 'no']:
            return choice
        else:
            print("Please enter 'yes' or 'no'.")

def get_positive_integer(prompt, default=None):
    """
    Prompt the user for a positive integer with validation.
    """
    while True:
        value = input(f"{prompt}" + (f" [default: {default}]" if default else "") + ": ").strip()
        if not value and default is not None:
            return default
        try:
            int_value = int(value)
            if int_value > 0:
                return int_value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

def get_float_list(prompt):
    """
    Prompt the user to enter a list of floats.
    """
    while True:
        values = input(f"{prompt}: ").strip().split()
        try:
            float_values = [float(value) for value in values]
            return float_values
        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces.")

def get_graph_type(prompt, valid_options, default='line'):
    """
    Prompt the user to select a graph type with validation.
    """
    valid_options_str = ', '.join(valid_options)
    while True:
        choice = input(f"{prompt} (options: {valid_options}) [default: {default}]: ").strip().lower()
        if not choice and default:
            choice = default
        if choice in valid_options:
            return choice
        else:
            print(f"Invalid graph type. Please choose from: {valid_options_str}.")

def get_input_with_default(prompt, default=None):
    """
    Prompt the user for input with an optional default value.
    """
    input_str = f"{prompt}"
    if default is not None:
        input_str += f" [default: {default}]"
    input_str += ": "
    value = input(input_str).strip()
    if not value and default is not None:
        return default
    return value

def confirm_action(prompt, default='yes'):
    """
    Prompt the user to confirm an action.
    """
    return get_yes_no(prompt, default=default)

def get_annotations():
    """
    Prompt the user for annotations settings.
    """
    annotations = {}
    add_annotations_choice = get_yes_no("Do you want to add annotations to the graph", default='no')
    if add_annotations_choice == 'yes':
        data_labels_choice = get_yes_no("Do you want to add data labels", default='no')
        if data_labels_choice == 'yes':
            annotations['data_labels'] = True
        mean_line_choice = get_yes_no("Do you want to add a mean line", default='no')
        if mean_line_choice == 'yes':
            annotations['mean_line'] = True
    return annotations

def get_bins():
    """
    Prompt the user for histogram bins settings.
    """
    bins_choice = get_yes_no("Do you want to specify the number of bins", default='no')
    if bins_choice == 'yes':
        bins_input = get_positive_integer("Enter the number of bins")
        return bins_input
    else:
        print("The number of bins will be determined automatically based on the data.")
        return None

def get_datasets():
    """
    Prompt the user to input datasets.
    """
    datasets = []
    num_datasets = get_positive_integer("Enter the number of datasets", default=1)
    for i in range(num_datasets):
        print(f"\nDataset {i + 1}:")
        x_data = get_float_list("Enter the X values (separated by spaces)")
        y_data = get_float_list("Enter the Y values (separated by spaces)")
        if len(x_data) != len(y_data):
            print("X and Y values must have the same length.")
            sys.exit(1)
        z_data = None
        is_3d = get_yes_no("Is this a 3D dataset", default='no')
        if is_3d == 'yes':
            z_data = get_float_list("Enter the Z values (separated by spaces)")
            if len(z_data) != len(x_data):
                print("X, Y, and Z values must have the same length.")
                sys.exit(1)
        label = get_input_with_default(f"Enter label for Dataset {i + 1}", default=f"Dataset {i + 1}")
        datasets.append({
            'x': x_data,
            'y': y_data,
            'z': z_data,
            'label': label
        })
    return datasets

def get_heatmap_data():
    """
    Prompt the user to input data for a heatmap.
    """
    rows = get_positive_integer("Enter the number of rows for the heatmap")
    cols = get_positive_integer("Enter the number of columns for the heatmap")
    matrix = []
    print("Enter the values row by row (space-separated):")
    for _ in range(rows):
        while True:
            row_values = input().strip().split()
            if len(row_values) != cols:
                print(f"Please enter exactly {cols} values.")
                continue
            try:
                row = [float(value) for value in row_values]
                matrix.append(row)
                break
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")
    return matrix

def get_save_path(prompt):
    """
    Prompt the user for a save path if they choose to save the graph.
    """
    save_choice = get_yes_no(prompt, default='no')
    if save_choice == 'yes':
        save_path = input("Enter file path to save the graph: ").strip()
        return save_path
    else:
        return None
