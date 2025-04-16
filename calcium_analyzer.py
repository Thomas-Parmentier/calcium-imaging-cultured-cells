import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                           QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
                           QMessageBox, QTabWidget)
from PyQt6.QtCore import Qt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from signalprocess import dataframe
import findpeaks
import plot

class CalciumAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calcium Imaging Analyzer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize variables
        self.data = None
        self.normdata = None
        self.time = None
        self.active_cells = None
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create tabs
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Input tab
        input_tab = QWidget()
        tabs.addTab(input_tab, "Input")
        input_layout = QVBoxLayout(input_tab)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setReadOnly(True)
        file_layout.addWidget(self.file_path)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        input_layout.addLayout(file_layout)
        
        # Parameters
        params_layout = QHBoxLayout()
        
        # Recording length
        length_layout = QVBoxLayout()
        length_layout.addWidget(QLabel("Recording Length (s)"))
        self.length = QDoubleSpinBox()
        self.length.setRange(0, 1000)
        self.length.setValue(180)
        length_layout.addWidget(self.length)
        params_layout.addLayout(length_layout)
        
        # Image interval
        interval_layout = QVBoxLayout()
        interval_layout.addWidget(QLabel("Image Interval (s)"))
        self.interval = QDoubleSpinBox()
        self.interval.setRange(0.1, 10)
        self.interval.setValue(0.5)
        interval_layout.addWidget(self.interval)
        params_layout.addLayout(interval_layout)
        
        # Stimulation
        stim_layout = QVBoxLayout()
        stim_layout.addWidget(QLabel("Stimulation"))
        self.stimulation = QComboBox()
        self.stimulation.addItems(["Yes", "No"])
        stim_layout.addWidget(self.stimulation)
        params_layout.addLayout(stim_layout)
        
        input_layout.addLayout(params_layout)
        
        # Peak detection parameters
        peaks_layout = QHBoxLayout()
        
        # Height threshold
        height_layout = QVBoxLayout()
        height_layout.addWidget(QLabel("Height Threshold"))
        self.height = QDoubleSpinBox()
        self.height.setRange(0, 10)
        self.height.setValue(0.5)
        height_layout.addWidget(self.height)
        peaks_layout.addLayout(height_layout)
        
        # Prominence threshold
        prominence_layout = QVBoxLayout()
        prominence_layout.addWidget(QLabel("Prominence Threshold"))
        self.prominence = QDoubleSpinBox()
        self.prominence.setRange(0, 10)
        self.prominence.setValue(0.5)
        prominence_layout.addWidget(self.prominence)
        peaks_layout.addLayout(prominence_layout)
        
        input_layout.addLayout(peaks_layout)
        
        # Process button
        process_btn = QPushButton("Process Data")
        process_btn.clicked.connect(self.process_data)
        input_layout.addWidget(process_btn)
        
        # Results tab
        results_tab = QWidget()
        tabs.addTab(results_tab, "Results")
        results_layout = QVBoxLayout(results_tab)
        
        # Plot area
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        results_layout.addWidget(self.canvas)
        
        # Plot controls
        plot_controls = QHBoxLayout()
        
        # Number of plots
        plots_layout = QVBoxLayout()
        plots_layout.addWidget(QLabel("Number of Plots"))
        self.num_plots = QSpinBox()
        self.num_plots.setRange(1, 20)
        self.num_plots.setValue(5)
        plots_layout.addWidget(self.num_plots)
        plot_controls.addLayout(plots_layout)
        
        # Plot type
        plot_type_layout = QVBoxLayout()
        plot_type_layout.addWidget(QLabel("Plot Type"))
        self.plot_type = QComboBox()
        self.plot_type.addItems(["Calcium Traces", "Raster Plot", "Synchronization", "Neuron Activity Map"])
        plot_type_layout.addWidget(self.plot_type)
        plot_controls.addLayout(plot_type_layout)
        
        # Update plot button
        update_plot_btn = QPushButton("Update Plot")
        update_plot_btn.clicked.connect(self.update_plot)
        plot_controls.addWidget(update_plot_btn)
        
        results_layout.addLayout(plot_controls)
        
        # Export button
        export_btn = QPushButton("Export Results")
        export_btn.clicked.connect(self.export_results)
        results_layout.addWidget(export_btn)
    
    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_name:
            self.file_path.setText(file_name)
    
    def process_data(self):
        if not self.file_path.text():
            QMessageBox.warning(self, "Error", "Please select a file first")
            return
        
        try:
            # Read and process data
            self.data = pd.read_csv(self.file_path.text())
            self.normdata = dataframe(self.data, self.length.value(), self.interval.value(), 
                                    self.stimulation.currentText())
            
            # Generate time array
            self.time = np.arange(start=0, stop=float(self.length.value()), 
                                step=float(self.interval.value()))
            
            # Find peaks
            (acell, nonacell, self.active_cells, numpeaks, raster_array, 
             active_raster_array, peak_widths, active_peak_widths, 
             active_peak_height, peak_raster) = findpeaks.findpeaks(
                self.normdata, self.height.value(), self.prominence.value(), 
                self.length.value())
            
            # Update status
            QMessageBox.information(self, "Success", "Data processed successfully!")
            
            # Update plot
            self.update_plot()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error processing data: {str(e)}")
    
    def update_plot(self):
        if self.normdata is None:
            return
        
        # Create a new figure instead of clearing the existing one
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        plot_type = self.plot_type.currentText()
        
        if plot_type == "Calcium Traces":
            ax = self.figure.add_subplot(111)
            plot.calciumplot(self.normdata, self.num_plots.value(), 
                           self.length.value(), self.interval.value())
        elif plot_type == "Raster Plot":
            (acell, nonacell, active_cells, numpeaks, raster_array, 
             active_raster_array, peak_widths, active_peak_widths, 
             active_peak_height, peak_raster) = findpeaks.findpeaks(
                self.normdata, self.height.value(), self.prominence.value(), 
                self.length.value())
            ax = self.figure.add_subplot(111)
            plot.spike_raster(raster_array, active_raster_array, 
                            peak_widths, active_peak_widths, 
                            self.length.value(), self.interval.value())
        elif plot_type == "Synchronization":
            (acell, nonacell, active_cells, numpeaks, raster_array, 
             active_raster_array, peak_widths, active_peak_widths, 
             active_peak_height, peak_raster) = findpeaks.findpeaks(
                self.normdata, self.height.value(), self.prominence.value(), 
                self.length.value())
            rasterpd, synchropd = plot.synchro(self.normdata, peak_raster, self.time)
            ax = self.figure.add_subplot(111)
            plot.plotsynchro(raster_array, peak_widths, synchropd, self.time)
        elif plot_type == "Neuron Activity Map":
            # Create a new figure window
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Create a meshgrid for the plot
            y = np.arange(len(self.normdata.columns))
            x = np.arange(len(self.normdata))
            X, Y = np.meshgrid(x, y)
            
            # Plot the data
            c = ax.pcolormesh(X, Y, self.normdata.T, cmap='inferno', vmin=0, vmax=5)
            plt.colorbar(c, label='Normalized Fluorescence')
            
            # Set labels and title
            ax.set_xlabel('Time (frames)')
            ax.set_ylabel('Neuron')
            ax.set_title('Neuron Activity Map')
            
            # Set y-axis ticks to show neuron numbers
            ax.set_yticks(np.arange(len(self.normdata.columns)))
            ax.set_yticklabels([f'Neuron {i+1}' for i in range(len(self.normdata.columns))])
            
            # Show the plot
            plt.show()
        
        if plot_type != "Neuron Activity Map":
            self.canvas.draw()
    
    def export_results(self):
        if self.normdata is None:
            QMessageBox.warning(self, "Error", "No data to export")
            return
        
        try:
            # Get export directory
            export_dir = QFileDialog.getExistingDirectory(self, "Select Export Directory")
            if not export_dir:
                return
            
            # Export processed data
            self.normdata.to_csv(os.path.join(export_dir, "processed_data.csv"))
            
            # Export peak properties if available
            if self.active_cells:
                (acell, nonacell, active_cells, numpeaks, raster_array, 
                 active_raster_array, peak_widths, active_peak_widths, 
                 active_peak_height, peak_raster) = findpeaks.findpeaks(
                    self.normdata, self.height.value(), self.prominence.value(), 
                    self.length.value())
                
                listamplitude, listwidth = findpeaks.export_properties(
                    active_peak_height, active_peak_widths)
                
                np.savetxt(os.path.join(export_dir, "peak_amplitudes.csv"), 
                          listamplitude, fmt="%1.3f", delimiter="\t")
                np.savetxt(os.path.join(export_dir, "peak_widths.csv"), 
                          listwidth, fmt="%1.3f", delimiter="\t")
            
            QMessageBox.information(self, "Success", "Results exported successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting results: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalciumAnalyzer()
    window.show()
    sys.exit(app.exec()) 