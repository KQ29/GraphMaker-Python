# plotting.py

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import os
import sys

# Import Plotly for interactive plots
import plotly.express as px
import plotly.graph_objects as go

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

def plot_violin(x_values_list, y_values_list, labels, x_label, y_label,
                save_path=None, interactive=False):
    """
    Plot violin plots for multiple datasets.
    """
    if interactive:
        # Use Plotly for interactive violin plot
        fig = go.Figure()
        for y, label in zip(y_values_list, labels):
            fig.add_trace(go.Violin(y=y, name=label, box_visible=True, meanline_visible=True))
        fig.update_layout(title="Violin Plot", xaxis_title=x_label, yaxis_title=y_label)
        fig.show()
    else:
        # Use Seaborn for static violin plot
        data = {'Y': [], 'Label': []}
        for y, label in zip(y_values_list, labels):
            data['Y'].extend(y)
            data['Label'].extend([label] * len(y))
        sns.violinplot(x='Label', y='Y', data=data)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title("Violin Plot")
        if save_path:
            plt.savefig(save_path)
            print(f"Violin plot saved to {save_path}")
        else:
            plt.show()

def plot_pairplot(data_dict, save_path=None, interactive=False):
    """
    Plot pair plots for the given datasets.
    """
    if interactive:
        print("Interactive pair plots are not supported at this time.")
        return
    else:
        import pandas as pd
        df = pd.DataFrame(data_dict)
        sns.pairplot(df)
        if save_path:
            plt.savefig(save_path)
            print(f"Pair plot saved to {save_path}")
        else:
            plt.show()

def plot_combined_2d_graph(x_values_list, y_values_list, labels, x_label, y_label,
                           graph_type, save_path=None, interactive=False, **kwargs):
    """
    Plot combined 2D graph for multiple datasets.
    """
    if interactive:
        if graph_type == 'line':
            fig = go.Figure()
            for x, y, label in zip(x_values_list, y_values_list, labels):
                fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=label))
            fig.update_layout(title="Combined Line Graph", xaxis_title=x_label, yaxis_title=y_label)
            fig.show()
        elif graph_type == 'scatter':
            fig = go.Figure()
            for x, y, label in zip(x_values_list, y_values_list, labels):
                fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name=label))
            fig.update_layout(title="Combined Scatter Plot", xaxis_title=x_label, yaxis_title=y_label)
            fig.show()
        elif graph_type == 'histogram':
            include_kde = kwargs.get('include_kde', False)
            fig = go.Figure()
            for y, label in zip(y_values_list, labels):
                fig.add_trace(go.Histogram(x=y, name=label, opacity=0.75))
            fig.update_layout(barmode='overlay', xaxis_title=y_label, yaxis_title='Count')
            fig.show()
            if include_kde:
                print("Interactive KDE is not supported in this implementation.")
        elif graph_type == 'bar':
            fig = go.Figure()
            for x, y, label in zip(x_values_list, y_values_list, labels):
                fig.add_trace(go.Bar(x=x, y=y, name=label))
            fig.update_layout(title="Combined Bar Chart", xaxis_title=x_label, yaxis_title=y_label)
            fig.show()
        else:
            print(f"Interactive plotting for '{graph_type}' is not supported.")
    else:
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
                    data = np.array(y)
                    q25, q75 = np.percentile(data, [25, 75])
                    bin_width = 2 * (q75 - q25) * len(data) ** (-1/3)
                    bins = max(int((data.max() - data.min()) / bin_width), 1) if bin_width > 0 else len(data)
                else:
                    bins = int(bins)
                ax.hist(y, bins=bins, color=current_color, edgecolor='black', label=labels[i], alpha=0.5, density=kwargs.get('include_kde', False))
                if kwargs.get('include_kde', False):
                    sns.kdeplot(y, ax=ax, color=current_color)
            elif graph_type == 'boxplot':
                ax.boxplot(y, patch_artist=True, boxprops=dict(facecolor=current_color), labels=[labels[i]])
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
                           x_label, y_label, z_label, save_path=None, interactive=False):
    """
    Plot combined 3D graph for multiple datasets.
    """
    if interactive:
        fig = go.Figure()
        for x, y, z, label in zip(x_values_list, y_values_list, z_values_list, labels):
            if z is None:
                print(f"Skipping 2D dataset '{label}' in 3D graph.")
                continue
            fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', name=label))
        fig.update_layout(title="Combined 3D Scatter Plot", scene=dict(
            xaxis_title=x_label,
            yaxis_title=y_label,
            zaxis_title=z_label
        ))
        fig.show()
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for x, y, z, label in zip(x_values_list, y_values_list, z_values_list, labels):
            if z is None:
                print(f"Skipping 2D dataset '{label}' in 3D graph.")
                continue
            ax.scatter(x, y, z, label=label)
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
                          save_path=None, interactive=False, **kwargs):
    """
    Plot individual 2D or 3D graph for a single dataset.
    """
    if interactive:
        if graph_type == '3d':
            if z is None:
                print(f"Dataset '{label}' has no Z values; skipping 3D plot.")
                return
            fig = go.Figure()
            fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', name=label))
            fig.update_layout(title=f"3D Scatter Plot for {label}", scene=dict(
                xaxis_title=x_label,
                yaxis_title=y_label,
                zaxis_title=z_label
            ))
            fig.show()
        elif graph_type == 'line':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=label))
            fig.update_layout(title=f"Line Graph for {label}", xaxis_title=x_label, yaxis_title=y_label)
            fig.show()
        elif graph_type == 'scatter':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name=label))
            fig.update_layout(title=f"Scatter Plot for {label}", xaxis_title=x_label, yaxis_title=y_label)
            fig.show()
        elif graph_type == 'histogram':
            include_kde = kwargs.get('include_kde', False)
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=y, name=label, opacity=0.75))
            fig.update_layout(title=f"Histogram for {label}", xaxis_title=y_label, yaxis_title='Count')
            fig.show()
            if include_kde:
                print("Interactive KDE is not supported in this implementation.")
        elif graph_type == 'violin':
            fig = go.Figure()
            fig.add_trace(go.Violin(y=y, name=label, box_visible=True, meanline_visible=True))
            fig.update_layout(title=f"Violin Plot for {label}", xaxis_title=x_label, yaxis_title=y_label)
            fig.show()
        else:
            print(f"Interactive plotting for '{graph_type}' is not supported.")
    else:
        if graph_type == '3d':
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            if z is None:
                print(f"Dataset '{label}' has no Z values; skipping 3D plot.")
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
        elif graph_type == 'violin':
            data = {'Y': y, 'Label': [label]*len(y)}
            sns.violinplot(x='Label', y='Y', data=data)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(f"Violin Plot for {label}")
            if save_path:
                plt.savefig(save_path)
                print(f"Violin plot for {label} saved to {save_path}")
            else:
                plt.show()
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.set_title(f"Graph for {label}")
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            current_color = f"C0"
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
                    data = np.array(y)
                    q25, q75 = np.percentile(data, [25, 75])
                    bin_width = 2 * (q75 - q25) * len(data) ** (-1/3)
                    bins = max(int((data.max() - data.min()) / bin_width), 1) if bin_width > 0 else len(data)
                else:
                    bins = int(bins)
                ax.hist(y, bins=bins, color=current_color, edgecolor='black', label=label, alpha=0.5, density=kwargs.get('include_kde', False))
                if kwargs.get('include_kde', False):
                    sns.kdeplot(y, ax=ax, color=current_color)
            elif graph_type == 'boxplot':
                ax.boxplot(y, patch_artist=True, boxprops=dict(facecolor=current_color), labels=[label])
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
