# plotting.py

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import os
import sys

def plot_heatmap(data, save_path=None):
    """
    Plot a heatmap for matrix-like data.
    """
    sns.heatmap(data, annot=True, cmap="coolwarm", fmt="g")
    if save_path:
        plt.savefig(save_path)
        print(f"Heatmap saved to {save_path}")
    else:
        plt.show()

def add_annotations(ax, x, y, annotations):
    """
    Add annotations to the plot.
    """
    if annotations.get('data_labels'):
        for xi, yi in zip(x, y):
            ax.annotate(f"({xi}, {yi})", xy=(xi, yi), textcoords="offset points",
                        xytext=(0,10), ha='center')
    if annotations.get('mean_line'):
        mean_y = np.mean(y)
        ax.axhline(mean_y, color='red', linestyle='--', label=f"Mean = {mean_y:.2f}")

def plot_combined_2d_graph(x_values_list, y_values_list, labels, x_label, y_label,
                           graph_type, save_path=None, **kwargs):
    """
    Plot combined 2D graph for multiple datasets.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title("Combined Graph")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    for i, (x, y) in enumerate(zip(x_values_list, y_values_list)):
        current_color = f"C{i}"
        marker = 'o' if graph_type in ['line', 'scatter'] else None

        if graph_type == 'line':
            ax.plot(x, y, marker=marker, linestyle='-', color=current_color, label=labels[i])
        elif graph_type == 'scatter':
            ax.scatter(x, y, color=current_color, marker=marker, label=labels[i])
        elif graph_type == 'bar':
            ax.bar(x, y, color=current_color, label=labels[i])
        elif graph_type == 'area':
            ax.fill_between(x, y, color=current_color, alpha=0.5, label=labels[i])
        elif graph_type == 'histogram':
            bins = kwargs.get('bins')
            if bins is None:
                # Dynamically determine bins using Freedman-Diaconis Rule
                data = np.array(y)
                q25, q75 = np.percentile(data, [25, 75])
                bin_width = 2 * (q75 - q25) * len(data) ** (-1/3)
                bins = max(int((data.max() - data.min()) / bin_width), 1) if bin_width > 0 else len(data)
            else:
                bins = int(bins)
            ax.hist(y, bins=bins, color=current_color, edgecolor='black', label=labels[i], alpha=0.5)
        elif graph_type == 'boxplot':
            ax.boxplot(y, patch_artist=True, boxprops=dict(facecolor=current_color),
                       labels=[labels[i]])
            box_patch = mpatches.Patch(color=current_color, label=labels[i])
            ax.legend(handles=[box_patch])
        else:
            print(f"Unsupported graph type: {graph_type}")

    # Add annotations
    annotations = kwargs.get('annotations', {})
    if annotations:
        add_annotations(ax, x_values_list[0], y_values_list[0], annotations)

    ax.legend()
    ax.grid(True)
    if save_path:
        plt.savefig(save_path)
        print(f"Combined graph saved to {save_path}")
    else:
        plt.show()

def plot_combined_3d_graph(x_values_list, y_values_list, z_values_list, labels,
                           x_label, y_label, z_label, save_path=None):
    """
    Plot combined 3D graph for multiple datasets.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, (x, y, z) in enumerate(zip(x_values_list, y_values_list, z_values_list)):
        if z is None:
            print(f"Skipping 2D dataset {i + 1} in 3D graph.")
            continue
        ax.scatter(x, y, z, label=labels[i])

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.legend()
    if save_path:
        plt.savefig(save_path)
        print(f"Combined 3D graph saved to {save_path}")
    else:
        plt.show()

def plot_individual_graph(x, y, z, label, x_label, y_label, z_label, graph_type,
                          save_path=None, **kwargs):
    """
    Plot individual 2D or 3D graph for a single dataset.
    """
    if graph_type == '3d':
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        if z is None:
            print(f"Dataset {label} has no Z values; skipping 3D plot.")
            return
        ax.scatter(x, y, z, label=label)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_zlabel(z_label)
        ax.legend()
        if save_path:
            plt.savefig(save_path)
            print(f"Graph for {label} saved to {save_path}")
        else:
            plt.show()
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(f"Graph for {label}")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        current_color = f"C0"  # For individual graphs, we can just use one color
        marker = 'o' if graph_type in ['line', 'scatter'] else None

        if graph_type == 'line':
            ax.plot(x, y, marker=marker, linestyle='-', color=current_color, label=label)
        elif graph_type == 'scatter':
            ax.scatter(x, y, color=current_color, marker=marker, label=label)
        elif graph_type == 'bar':
            ax.bar(x, y, color=current_color, label=label)
        elif graph_type == 'area':
            ax.fill_between(x, y, color=current_color, alpha=0.5, label=label)
        elif graph_type == 'histogram':
            bins = kwargs.get('bins')
            if bins is None:
                # Dynamically determine bins using Freedman-Diaconis Rule
                data = np.array(y)
                q25, q75 = np.percentile(data, [25, 75])
                bin_width = 2 * (q75 - q25) * len(data) ** (-1/3)
                bins = max(int((data.max() - data.min()) / bin_width), 1) if bin_width > 0 else len(data)
            else:
                bins = int(bins)
            ax.hist(y, bins=bins, color=current_color, edgecolor='black', label=label, alpha=0.5)
        elif graph_type == 'boxplot':
            ax.boxplot(y, patch_artist=True, boxprops=dict(facecolor=current_color),
                       labels=[label])
            box_patch = mpatches.Patch(color=current_color, label=label)
            ax.legend(handles=[box_patch])
        else:
            print(f"Unsupported graph type: {graph_type}")

        # Add annotations
        annotations = kwargs.get('annotations', {})
        if annotations:
            add_annotations(ax, x, y, annotations)

        ax.legend()
        ax.grid(True)
        if save_path:
            plt.savefig(save_path)
            print(f"Graph for {label} saved to {save_path}")
        else:
            plt.show()
