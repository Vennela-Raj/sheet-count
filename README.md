# Sheet Counting Application

## Project Overview

The Sheet Counting Application is a web-based tool designed to count the number of sheets in a stack using computer vision techniques. This application processes uploaded images of sheet stacks, enhances the images, and uses edge detection and intensity analysis to count the individual sheets.

## Frameworks/Libraries/Tools

- **Flask**: A web framework for Python used to create the web application.
- **OpenCV**: A library for computer vision used for image processing and sheet detection.
- **NumPy**: A library for numerical computations used for handling image data.
- **SciPy**: A library used for signal processing, specifically for finding peaks in the intensity projections.
- **Matplotlib**: A plotting library used for visualizing images (optional for debugging).

## Installation Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Vennela-Raj/sheet-count.git

2.**Navigate to the Project Directory**

    cd sheet-count

3.**Create and Activate a Virtual Environment**

    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

4.**Install Dependencies**

  Create a requirements.txt file listing the project dependencies, or use the following command if requirements.txt is       already included:

    pip install Flask opencv-python-headless numpy scipy matplotlib

5.**Run the Application**

    python app.py

Open your web browser and navigate to http://127.0.0.1:5000 to use the application.

## Usage

**Upload an Image**

Click the "Choose File" button to select an image of a sheet stack from your local machine.
Click the "Upload and Count" button to submit the image.

**View Results**

After processing, the application will display the number of sheets detected along with the uploaded image.
