# ProConverter

## How to Run the Code

### Installation Steps:

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/5mbl/ocr-backend.git
   ```
2. **Install Dependencies:**

- **Pytesseract:** ¹

  - Download and install [tesseract-ocr-w64-setup-5.3.3.20231005.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe).
  - After installation, locate the installed directory (e.g., `C:\Program Files (x86)\Tesseract-OCR`).
  - Download the German training data file from [here](https://github.com/tesseract-ocr/tessdata/blob/main/deu.traineddata).
  - Copy the downloaded file into the "tessdata" directory within the installed Tesseract directory (e.g., `C:\Program Files (x86)\Tesseract-OCR\tessdata`).
  - Specifying tesseract.exe Path in Code:

    ```python
    # app.py (line 35)

    #pytesseract for OCR
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    ```

- **Poppler:** ²

  - Go to [Poppler Windows Releases](https://github.com/oschwartz10612/poppler-windows/releases/).
  - Under **Release 23.11.0-0 Latest v23.11.0-0**, navigate to **Assets 3**
  - Download **Release-23.11.0-0.zip**.
  - Extract the downloaded zip file.
  - Add the extracted Poppler folder to a location such as: `C:\Users\UserName\Downloads\Release-23.11.0-0`.
  - Add the path `C:\Users\UserName\Downloads\Release-21.11.0-0` to the system variable **Path** in the **Environment Variables**.
  - Specifying Poppler Path in Code:

    ```python
    # app.py (line 38)

    # poppler for pdf2img
    poppler_path = r"C:\poppler-23.11.0\Library\bin"

    ```

- **Activating the virtual enviroment:**
  - Terminal: `python -m venv myenv`
- **Install requirements.txt:**

  - `pip install -r requirements.txt`

- **Start the Application**
  - `run flask`

## References

¹ https://smartextract.ai/pytesseract/

² https://stackoverflow.com/questions/53481088/poppler-in-path-for-pdf2image
