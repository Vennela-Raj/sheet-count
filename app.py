from flask import Flask, render_template, request, redirect
import cv2
import numpy as np
import os
from scipy.signal import find_peaks

app = Flask(__name__)

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for brown and cream
    lower_brown = np.array([10, 100, 20])
    upper_brown = np.array([30, 255, 200])
    lower_cream = np.array([0, 0, 200])
    upper_cream = np.array([50, 50, 255])

    # Create masks
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    mask_cream = cv2.inRange(hsv, lower_cream, upper_cream)
    mask = cv2.bitwise_or(mask_brown, mask_cream)

    # Find contours and crop the image to the bounding box of detected areas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(np.concatenate(contours))
        cropped_image = image[y:y+h, x:x+w]
    else:
        cropped_image = image

    # Convert to grayscale
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    
    return image, cropped_image, gray

def enhance_image(gray_image, output_path):
    # Apply Adaptive Histogram Equalization for better contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    hist_eq = clahe.apply(gray_image)
    
    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(hist_eq, (5, 5), 0)
    
    # Apply Canny Edge Detection
    edges = cv2.Canny(blurred, 50, 150)
    
    # Save the enhanced image
    cv2.imwrite(output_path, edges)
    
    return edges

def count_sheets_by_intensity(edges_image):
    # Vertical projection of intensity
    vertical_projection = np.sum(edges_image, axis=1)
    
    # Find peaks in the vertical projection
    peaks, _ = find_peaks(vertical_projection, distance=10, height=np.max(vertical_projection)/3)
    
    # Filter peaks to count valid sheets
    return len(peaks)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Save the uploaded file
            image_path = os.path.join('static/uploads', file.filename)
            file.save(image_path)
            
            # Process the image
            original, cropped, gray = preprocess_image(image_path)
            
            # Save the enhanced image
            enhanced_image_path = os.path.join('static/uploads', 'enhanced_' + file.filename)
            edges = enhance_image(gray, enhanced_image_path)
            
            # Count sheets
            count = count_sheets_by_intensity(edges)
            
            return render_template('index.html', original=image_path, enhanced=enhanced_image_path, count=count)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
