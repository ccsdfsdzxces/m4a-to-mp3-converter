# M4A to MP3 Converter

This is a Python-based GUI application for converting M4A audio files to MP3 format using FFmpeg. The application provides an easy-to-use interface for selecting input files, specifying an output folder, and monitoring the conversion progress.

## Features

- Select multiple M4A files for conversion.
- Specify an output folder for the converted MP3 files.
- Monitor conversion progress with a progress bar.
- View the final conversion results (success and failure counts).

## Prerequisites

1. **Python 3.6 or higher**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/).
2. **FFmpeg**: This program requires FFmpeg to perform the audio conversion. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/) and ensure it is installed and added to your system's PATH.

## Installation

1. Clone or download this repository to your local machine.
2. Install the required Python libraries by running the following command in your terminal or command prompt:

   ```sh
   pip install tkinter
Note: tkinter is included by default in most Python installations. If you encounter issues, ensure your Python installation includes tkinter.

Usage
Run the program by executing the following command in the terminal or command prompt:

The GUI window will open. Follow these steps to use the application:

Select M4A Files: Click the "选择M4A文件" button to select one or more M4A files for conversion.
Clear List: If needed, click the "清除列表" button to clear the selected files.
Select Output Folder: Click the "选择输出文件夹" button to specify the folder where the converted MP3 files will be saved.
Start Conversion: Click the "开始转换" button to begin the conversion process. The progress bar will update as files are converted.
Once the conversion is complete, a message box will display the results, including the number of successful and failed conversions.

Notes
Ensure FFmpeg is installed and accessible. The program will attempt to locate FFmpeg in common directories or the system PATH. If FFmpeg is not found, an error message will be displayed.
The default FFmpeg path in the code is set to:
ffmpeg.exe
Update this path in the find_ffmpeg method if your FFmpeg installation is located elsewhere.
Troubleshooting
FFmpeg Not Found: If you see an error message about FFmpeg not being found, ensure it is installed and added to your system's PATH. Alternatively, update the find_ffmpeg method in the code with the correct path to your FFmpeg executable.
Conversion Errors: If a file fails to convert, check the console output for error details.
License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.
