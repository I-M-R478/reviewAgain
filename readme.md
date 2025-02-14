Web Scraper and File Uploader

This project is a simple web application built with Python (Flask) that allows teachers to upload and scrape data from student submissions. Teachers can upload PDF or image files, extract text from them, and review the extracted content. The application also saves uploaded files and their extracted data to a database for later review.

Features

Upload Files:

Supports PDF and image file uploads.

Extract Text:

Extracts text from uploaded files using OCR for images and text extraction for PDFs.

Save to Database:

Saves file metadata and extracted text to an SQLite database.

View Extracted Text:

Displays extracted text for review immediately after upload.

Technologies Used

Backend: Flask

Database: SQLite

Frontend: HTML, CSS (Bootstrap-like styling)

Libraries:

Flask: Web framework

sqlite3: Database management

Pillow: For image handling

PyPDF2: For PDF text extraction

pytesseract: OCR for image text extraction


