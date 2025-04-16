# Calcium Imaging Analyzer

A standalone application for analyzing calcium imaging data with a graphical user interface.

## Features

- Load and process calcium imaging data from CSV files
- Adjustable parameters for data processing and peak detection
- Multiple visualization options:
  - Calcium traces
  - Raster plots
  - Synchronization analysis
- Export processed data and analysis results

## Installation

1. Make sure you have Python 3.8 or later installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python calcium_analyzer.py
   ```

2. In the application:
   - Click "Browse" to select your calcium imaging data file (CSV format)
   - Set the recording parameters:
     - Recording length (in seconds)
     - Image interval (in seconds)
     - Whether stimulation was applied
   - Adjust peak detection parameters:
     - Height threshold
     - Prominence threshold
   - Click "Process Data" to analyze the data
   - Use the "Results" tab to view different visualizations
   - Click "Export Results" to save the processed data and analysis results

## Input Data Format

The input CSV file should have the following structure:
- First column: Background signal
- Second column onwards: Individual neuron signals
- No header row required

## Output Files

The application generates the following output files:
- `processed_data.csv`: Normalized calcium traces
- `peak_amplitudes.csv`: Peak amplitudes for active cells
- `peak_widths.csv`: Peak widths for active cells

## License

This project is licensed under the MIT License - see the LICENSE file for details. 