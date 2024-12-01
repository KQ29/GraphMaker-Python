# main.py

from data_processing import process_data, load_data_from_file
from plotting import (
    plot_heatmap,
    plot_combined_2d_graph,
    plot_combined_3d_graph,
    plot_individual_graph,
)
import numpy as np
import sys

def main():
    try:
        # Ask if the user wants to load data from a file
        data_source = input("Do you want to load data from a file? (yes/no): ").strip().lower()
        x_values = []
        y_values = []
        z_values = []  # For 3D graphs
        labels = []

        # File-based or manual data input
        if data_source == 'yes':
            file_path = input("Enter the file path: ").strip()
            x, y = load_data_from_file(file_path)
            x_values.append(process_data(x))
            y_values.append(process_data(y))
            labels.append("Dataset 1")
            z_values.append(None)  # No Z values unless specified
        else:
            # Validate the number of datasets
            while True:
                try:
                    datasets = int(input("Enter the number of datasets: ").strip())
                    if datasets <= 0:
                        print("The number of datasets must be a positive integer.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a single positive integer.")

            # Manual input for multiple datasets
            for i in range(datasets):
                print(f"\nDataset {i + 1}:")
                x_data = input("Enter the X values (separated by spaces): ").split()
                y_data = input("Enter the Y values (separated by spaces): ").split()
                if len(x_data) != len(y_data):
                    raise ValueError("X and Y values must have the same length.")
                x_values.append(process_data(x_data))
                y_values.append(process_data(y_data))
                z_data = None
                if input("Is this a 3D dataset? (yes/no): ").strip().lower() == "yes":
                    z_data = input("Enter the Z values (separated by spaces): ").split()
                    if len(z_data) != len(x_data):
                        raise ValueError("X, Y, and Z values must have the same length.")
                    z_values.append(process_data(z_data))
                else:
                    z_values.append(None)  # No Z values for 2D datasets
                labels.append(f"Dataset {i + 1}")

        # Only ask about combining graphs if there are multiple datasets
        if len(x_values) > 1:
            combine_choice = input("Do you want to combine all graphs into one? (yes/no): ").strip().lower()
        else:
            combine_choice = "no"

        if combine_choice == 'yes':
            # Combine graphs
            x_label = input("Enter the name for the X-axis: ")
            y_label = input("Enter the name for the Y-axis: ")
            z_label = None
            graph_type = input("Enter the type of graph (line, scatter, bar, area, histogram, boxplot, heatmap, 3d): ").lower()
            if graph_type not in ['line', 'scatter', 'bar', 'area', 'histogram', 'boxplot', 'heatmap', '3d']:
                print("Invalid graph type. Defaulting to 'line'.")
                graph_type = 'line'

            kwargs = {}

            if graph_type == 'histogram':
                # Only ask about bins for histograms
                bins_choice = input("Do you want to specify the number of bins? (yes/no): ").strip().lower()
                if bins_choice == 'yes':
                    bins_input = input("Enter the number of bins: ")
                    if bins_input:
                        kwargs['bins'] = int(bins_input)
                else:
                    print("The number of bins will be determined automatically based on the data.")

            if graph_type in ['line', 'scatter', 'bar', 'area', 'histogram', 'boxplot']:
                # Only ask about annotations for applicable graph types
                annotations = {}
                add_annotations_choice = input("Do you want to add annotations to the graph? (yes/no): ").strip().lower()
                if add_annotations_choice == 'yes':
                    data_labels_choice = input("Do you want to add data labels? (yes/no): ").strip().lower()
                    if data_labels_choice == 'yes':
                        annotations['data_labels'] = True
                    mean_line_choice = input("Do you want to add a mean line? (yes/no): ").strip().lower()
                    if mean_line_choice == 'yes':
                        annotations['mean_line'] = True
                kwargs['annotations'] = annotations
            else:
                # For graph types where annotations are not applicable
                kwargs['annotations'] = {}

            if graph_type == 'heatmap':
                # Special case for heatmaps
                rows = int(input("Enter the number of rows for the heatmap: "))
                cols = int(input("Enter the number of columns for the heatmap: "))
                matrix = []
                print("Enter the values row by row (space-separated):")
                for _ in range(rows):
                    matrix.append(list(map(float, input().split())))
                save_choice = input("Do you want to save the heatmap? (yes/no): ").strip().lower()
                save_path = None
                if save_choice == 'yes':
                    save_path = input("Enter file path to save the heatmap: ").strip()
                plot_heatmap(np.array(matrix), save_path=save_path)
            elif graph_type == '3d':
                # Plot combined 3D graph
                z_label = input("Enter the name for the Z-axis: ")
                save_choice = input("Do you want to save the combined 3D graph? (yes/no): ").strip().lower()
                save_path = None
                if save_choice == 'yes':
                    save_path = input("Enter file path to save the graph: ").strip()
                plot_combined_3d_graph(
                    x_values, y_values, z_values, labels, x_label, y_label, z_label, save_path=save_path
                )
            else:
                save_choice = input("Do you want to save the combined graph? (yes/no): ").strip().lower()
                save_path = None
                if save_choice == 'yes':
                    save_path = input("Enter file path to save the graph: ").strip()

                # Plot combined 2D graph
                plot_combined_2d_graph(
                    x_values, y_values, labels, x_label, y_label, graph_type, save_path=save_path, **kwargs
                )
        else:
            # Separate graphs
            for i, (x, y, z) in enumerate(zip(x_values, y_values, z_values)):
                x_label = input(f"Enter the name for the X-axis for Dataset {i + 1}: ")
                y_label = input(f"Enter the name for the Y-axis for Dataset {i + 1}: ")
                z_label = None
                graph_type = input(
                    f"Enter the type of graph for Dataset {i + 1} (line, scatter, bar, area, histogram, boxplot, 3d): "
                ).lower()
                if graph_type not in ['line', 'scatter', 'bar', 'area', 'histogram', 'boxplot', '3d']:
                    print("Invalid graph type. Defaulting to 'line'.")
                    graph_type = 'line'
                if graph_type == '3d':
                    z_label = input("Enter the name for the Z-axis: ")

                kwargs = {}

                if graph_type == 'histogram':
                    bins_choice = input("Do you want to specify the number of bins? (yes/no): ").strip().lower()
                    if bins_choice == 'yes':
                        bins_input = input("Enter the number of bins: ")
                        if bins_input:
                            kwargs['bins'] = int(bins_input)
                    else:
                        print("The number of bins will be determined automatically based on the data.")

                if graph_type in ['line', 'scatter', 'bar', 'area', 'histogram', 'boxplot']:
                    # Only ask about annotations for applicable graph types
                    annotations = {}
                    add_annotations_choice = input(f"Do you want to add annotations to the graph for Dataset {i + 1}? (yes/no): ").strip().lower()
                    if add_annotations_choice == 'yes':
                        data_labels_choice = input("Do you want to add data labels? (yes/no): ").strip().lower()
                        if data_labels_choice == 'yes':
                            annotations['data_labels'] = True
                        mean_line_choice = input("Do you want to add a mean line? (yes/no): ").strip().lower()
                        if mean_line_choice == 'yes':
                            annotations['mean_line'] = True
                    kwargs['annotations'] = annotations
                else:
                    # For graph types where annotations are not applicable
                    kwargs['annotations'] = {}

                save_choice = input(f"Do you want to save the graph for Dataset {i + 1}? (yes/no): ").strip().lower()
                save_path = None
                if save_choice == 'yes':
                    save_path = input(f"Enter file path to save the graph for Dataset {i + 1}: ").strip()

                plot_individual_graph(
                    x, y, z, labels[i], x_label, y_label, z_label, graph_type, save_path=save_path, **kwargs
                )

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(0)
    except ValueError as e:
        print(f"Input error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
