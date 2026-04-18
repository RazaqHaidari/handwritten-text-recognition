# Handwritten Text Recognition System using Deep Learning

## 📌 Project Overview

This project is a web-based OCR (Optical Character Recognition) system developed using Flask that converts handwritten images into digital text. It uses a hybrid approach combining a custom OCR pipeline and Google Vision API to balance accuracy and accessibility.

## 🚀 Features

* Handwritten text recognition from images
* Hybrid OCR system:

  * Free users: OpenCV + Tesseract (~60–80% accuracy)
  * Logged-in users: Google Vision API (~90–99% accuracy)
* Image preprocessing (grayscale, resizing, sharpening, thresholding)
* User authentication (Login/Signup)
* Role-based OCR processing
* Handwritten-style text generator (PIL)
* Downloadable output

## 🛠️ Tech Stack

* Backend: Flask (Python)
* Image Processing: OpenCV
* OCR Engine: Tesseract OCR
* API: Google Vision API
* Database: SQLite (SQLAlchemy)
* Frontend: HTML, CSS

## ⚙️ System Workflow

User uploads image → Preprocessing → Check login:

* If logged in → Google Vision API
* Else → Tesseract OCR
  → Extract text → Generate output → Display & Download

## 📂 Project Structure

* app.py → Main Flask app
* model.py → Custom OCR pipeline
* predict.py → Google Vision API integration
* generator.py → Handwriting generator
* templates/ → HTML files
* static/ → CSS, uploads

## ▶️ How to Run

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:

   ```bash
   python app.py
   ```
4. Open browser and go to:

   ```
   http://127.0.0.1:5000/
   ```

## 🔐 Note on Security

Sensitive files like API keys are not included in this repository. Use environment variables (.env) to store credentials securely.

## 🎯 Future Improvements

* Improve custom OCR accuracy using deep learning models
* Add spell correction using NLP
* Deploy system on cloud
* Add multi-language support

## 👨‍💻 Author

Razaq Haidari
MCA Final Year Student
Chandigarh University

---

⭐ If you like this project, consider giving it a star!
