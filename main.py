# main.py

from data_processing import process_data, load_data_from_file
from plotting import (
    plot_heatmap,
    plot_combined_2d_graph,
    plot_combined_3d_graph,
    plot_individual_graph,
)
from user_interface import (
    get_yes_no,
    get_positive_integer,
    get_float_list,
    get_graph_type,
    get_input_with_default,
    confirm_action,
    get_annotations,
    get_bins,
    get_datasets,
    get_heatmap_data,
    get_save_path,
)
import numpy as np
import sys

def main():
    try:
        data_source = get_yes_no("Do you want to load data from a file", default='no')
        x_values = []
        y_values = []
        z_values = []  # For 3D graphs
        labels = []

        if data_source == 'yes':
            file_path = input("Enter the file path: ").strip()
            x, y = load_data_from_file(file_path)
            x_values.append(process_data(x))
            y_values.append(process_data(y))
            labels.append("Dataset 1")
            z_values.append(None)  # No Z values unless specified
        else:
            datasets = get_datasets()
            for dataset in datasets:
                x_values.append(process_data(dataset['x']))
                y_values.append(process_data(dataset['y']))
                z_values.append(process_data(dataset['z']) if dataset['z'] else None)
                labels.append(dataset['label'])

        combine_choice = 'no'
        if len(x_values) > 1:
            combine_choice = get_yes_no("Do you want to combine all graphs into one", default='no')

        if combine_choice == 'yes':
            x_label = get_input_with_default("Enter the name for the X-axis", default='X')
            y_label = get_input_with_default("Enter the name for the Y-axis", default='Y')
            graph_type = get_graph_type(
                "Enter the type of graph",
                ['line', 'scatter', 'bar', 'area', 'histogram', 'boxplot', 'heatmap', '3d'],
                default='line'
            )

            kwargs = {}

            if graph_type == 'histogram':
                bins = get_bins()
                if bins is not None:
                    kwargs['bins'] = bins

            if graph_type in ['line', 'scatter', 'bar', 'area', 'histogram', 'boxplot']:
                annotations = get_annotations()
                kwargs['annotations'] = annotations
            else:
                kwargs['annotations'] = {}

            if graph_type == 'heatmap':
                matrix = get_heatmap_data()
                save_path = get_save_path("Do you want to save the heatmap")
                plot_heatmap(np.array(matrix), save_path=save_path)
            elif graph_type == '3d':
                z_label = get_input_with_default("Enter the name for the Z-axis", default='Z')
                save_path = get_save_path("Do you want to save the combined 3D graph")
                plot_combined_3d_graph(
                    x_values, y_values, z_values, labels, x_label, y_label, z_label, save_path=save_path
                )
            else:
                save_path = get_save_path("Do you want to save the combined graph")
                plot_combined_2d_graph(
                    x_values, y_values, labels, x_label, y_label, graph_type, save_path=save_path, **kwargs
                )
        else:
            for i, (x, y, z) in enumerate(zip(x_values, y_values, z_values)):
                x_label = get_input_with_default(f"Enter the name for the X-axis for Dataset {i + 1}", default='X')
                y_label = get_input_with_default(f"Enter the name for the Y-axis for Dataset {i + 1}", default='Y')
                graph_type = get_graph_type(
                    f"Enter the type of graph for Dataset {i + 1}",
                    ['line', 'scatter', 'bar', 'area', 'histogram', 'boxplot', '3d'],
                    default='line'
                )

                kwargs = {}

                if graph_type == 'histogram':
                    bins = get_bins()
                    if bins is not None:
                        kwargs['bins'] = bins

                if graph_type in ['line', 'scatter', 'bar', 'area', 'histogram', 'boxplot']:
                    annotations = get_annotations()
                    kwargs['annotations'] = annotations
                else:
                    kwargs['annotations'] = {}

                if graph_type == '3d':
                    z_label = get_input_with_default("Enter the name for the Z-axis", default='Z')
                    save_path = get_save_path(f"Do you want to save the graph for Dataset {i + 1}")
                    plot_individual_graph(
                        x, y, z, labels[i], x_label, y_label, z_label, graph_type, save_path=save_path, **kwargs
                    )
                else:
                    save_path = get_save_path(f"Do you want to save the graph for Dataset {i + 1}")
                    plot_individual_graph(
                        x, y, z, labels[i], x_label, y_label, None, graph_type, save_path=save_path, **kwargs
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
