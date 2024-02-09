# from api.auth import userRegister  # Importieren der Auth-Routen
from db.models import User  # Importieren Sie das User-Modell
from api.extractImg2Text import apiBlueprint
from flask import Flask, render_template, request, redirect, url_for, flash,session,send_file,Response
from db.db import db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import csv
import os
import tempfile


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import pytesseract

import io
import zipfile
from pdf2image import convert_from_bytes
from pdf2image import convert_from_path


from flask import Flask, render_template, request, send_file
from pdf2image import convert_from_bytes
import io
import zipfile


from PIL import Image, ImageDraw, ImageFont

# Setting PATH

# pytesseract for OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# poppler for pdf2img
poppler_path = r"C:\poppler-23.11.0\Library\bin"




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'passwortxyz123'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
with app.app_context():
    db.create_all()  # creating the DB


# Import the blueprint after initializing the app
app.register_blueprint(apiBlueprint, url_prefix='/api')



@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    if session.get("user_name"):
        user_name = session.get("user_name")

        return render_template('index.html',user_name=user_name)
    else:
        return redirect("/login")
  


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Dieser Benutzername ist bereits vergeben.')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session["user_name"] = username

        user = User.query.filter_by(username=username).first()
        print(user)
        if user is not None:
            # Hier können Sie die Benutzersitzung einrichten
            # Leitet zu einer anderen Seite um, z.B. die Startseite
            return redirect(url_for('home'))
        else:
            flash('Ungültiger Benutzername oder Passwort!')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session["user_name"] = username

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username is already taken. Please choose another.', 'danger')
        else:
            # Add a new user
            new_user = User(username=username, password_hash=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('home'))

    return render_template('signup.html')



@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))










def convert_csv_to_txt(csv_file_path, txt_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = ['\t'.join(row) for row in csv_reader]

    with open(txt_file_path, 'w') as txt_file:
        txt_file.write('\n'.join(data))


@app.route('/csv-to-txt')
def csvToTxt():
    return render_template('csv_txt.html')



@app.route('/convert-csv', methods=['POST'])
def convert_csv():
    if 'csv_file' not in request.files:
        return redirect(url_for('csvToTxt'))

    csv_file = request.files['csv_file']
    if csv_file.filename == '':
        return redirect(url_for('csvToTxt'))

    # Save the uploaded CSV file temporarily
    temp_csv_path = 'temp.csv'
    csv_file.save(temp_csv_path)

    # Define the path for the output text file
    txt_file_path = 'output.txt'

    # Convert the CSV to TXT
    convert_csv_to_txt(temp_csv_path, txt_file_path)

    # Delete the temporary CSV file
    os.remove(temp_csv_path)

    # Send the text file as a download response
    return send_file(txt_file_path, as_attachment=True)




@app.route('/png-to-pdf')
def pngToPdf():
    return render_template('png-to-pdf.html')







def convert_png_to_pdf(png_bytes):
    #Save PNG bytes to a temporary file
    temp_png_path = 'temp.png'
    with open(temp_png_path, 'wb') as temp_png_file:
        temp_png_file.write(png_bytes)

    img = Image.open(io.BytesIO(png_bytes))
    
    #Create a PDF document in memory
    pdf_bytes = io.BytesIO()
    pdf_canvas = canvas.Canvas(pdf_bytes, pagesize=letter)
    
    #Set the dimensions of the PDF to match the image
    pdf_canvas.setPageSize((img.width, img.height))

    #Draw the image on the PDF
    pdf_canvas.drawInlineImage(img, 0, 0, width=img.width, height=img.height)

    #Save the PDF
    pdf_canvas.save()

    #Close and remove the temporary PNG file
    temp_png_file.close()
    os.remove(temp_png_path)

    return pdf_bytes.getvalue()



@app.route('/convert-png-to-pdf', methods=['POST'])
def convertPngToPdf():
    if 'png_file' not in request.files:
        return redirect(url_for('index'))

    png_file = request.files['png_file']
    if png_file.filename == '':
        return redirect(url_for('index'))

    #Read the uploaded PNG file
    png_bytes = png_file.read()

    #Convert the PNG to PDF
    pdf_bytes = convert_png_to_pdf(png_bytes)

    #Send the PDF as a download response
    return send_file(io.BytesIO(pdf_bytes), as_attachment=True, download_name='output.pdf')



def convert_png_to_jpg(png_bytes):
    # Open PNG image from bytes
    img = Image.open(io.BytesIO(png_bytes))

    # Convert to RGB mode (required for saving as JPG)
    rgb_img = img.convert('RGB')

    # Save as JPG in memory
    jpg_bytes = io.BytesIO()
    rgb_img.save(jpg_bytes, 'JPEG')
    
    return jpg_bytes.getvalue()


@app.route('/png-to-jpg')
def pngToJpg():
    return render_template('png-to-jpg.html')


@app.route('/convert', methods=['POST'])
def convert():
    if 'png_file' not in request.files:
        return redirect(url_for('pngToJpg'))

    png_file = request.files['png_file']
    if png_file.filename == '':
        return redirect(url_for('pngToJpgs'))

    # Read the uploaded PNG file
    png_bytes = png_file.read()

    # Convert PNG to JPG
    jpg_bytes = convert_png_to_jpg(png_bytes)

    # Send the JPG as a download response
    return send_file(
        io.BytesIO(jpg_bytes),
        mimetype='image/jpeg',
        as_attachment=True,
        download_name='output.jpg'
    )



###############





def png_to_text(png_bytes):
    # Open the PNG image from bytes
    img = Image.open(io.BytesIO(png_bytes))

    # Perform OCR to extract text
    text = pytesseract.image_to_string(img)

    return text

@app.route('/png-to-txt')
def pngg():
    print("Tesseract Command:", pytesseract.pytesseract.tesseract_cmd)
    return render_template('png-to-txt.html')

@app.route('/converttt', methods=['POST'])
def converttt():
    if 'png_file' not in request.files:
        return redirect(url_for('index'))

    png_file = request.files['png_file']
    if png_file.filename == '':
        return redirect(url_for('index'))

    # Read the uploaded PNG file
    png_bytes = png_file.read()

    # Convert PNG to text using OCR
    result_text = png_to_text(png_bytes)

    # Create a downloadable text file
    response = Response(result_text.encode('utf-8'), content_type='text/plain; charset=utf-8')
    response.headers['Content-Disposition'] = 'attachment; filename=result.txt'

    return response








## starting reverse code




@app.route('/convert-csv-to-text', methods=['POST'])
def convert_csv_to_text():
    # Check if a file is present in the request
    if 'text_file' not in request.files:
        return render_template('csv_txt.html', error='No file provided')

    text_file = request.files['text_file']

    # Check if the file is empty
    if text_file.filename == '':
        return render_template('csv_txt.html', error='Empty file provided')

    # Read the content of the text file
    text_content = text_file.read().decode('utf-8')

    # Convert the text to a list of lines
    lines = text_content.split('\n')

    # Create a CSV string
    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data)
    for line in lines:
        csv_writer.writerow(line.split())

    # Create a response with the CSV content
    response = Response(csv_data.getvalue(), content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=output.csv'

    return response




@app.route('/convert-pdf', methods=['POST'])
def convert_pdf_to_png():
    if 'pdf_file' not in request.files:
        return render_template('index.html', error='No PDF file provided')

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return render_template('index.html', error='No file selected')

    # Temporarily save PDF to disk to convert it
    with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
        pdf_file.save(temp_pdf)
        temp_pdf_path = temp_pdf.name

    # Convert PDF to a list of images
    try:
        # Specify the poppler_path=r'C:\path\to\poppler\bin' if not added to PATH
        images = convert_from_path(temp_pdf_path, dpi=200)

        # Prepare a ZIP archive to store PNG images
        zip_bytes_io = io.BytesIO()
        with zipfile.ZipFile(zip_bytes_io, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, image in enumerate(images):
                # Save each image to a BytesIO object
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                
                # Add image to zip file
                img_byte_arr.seek(0)
                zip_file.writestr(f'image_{i+1}.png', img_byte_arr.getvalue())

        # Clean up the temporary PDF file
        os.remove(temp_pdf_path)

        # Return the ZIP file
        zip_bytes_io.seek(0)
        return send_file(zip_bytes_io, mimetype='application/zip', as_attachment=True, download_name='converted_images.zip')
    except Exception as e:
        # Clean up the temporary PDF file in case of an error
        os.remove(temp_pdf_path)
        return render_template('index.html', error=str(e))

##jpg to png



@app.route('/convert-jpg-to-png', methods=['POST'])
def convert_ppg_to_png():
    # Check if a file is present in the request
    if 'jpg_file' not in request.files:
        return render_template('index.html', error='No file provided')

    jpg_file = request.files['jpg_file']

    # Check if the file is empty
    if jpg_file.filename == '':
        return render_template('index.html', error='Empty file provided')

    # Read the JPG file
    image = Image.open(io.BytesIO(jpg_file.read()))

    # Convert the image to PNG
    png_data = io.BytesIO()
    image.save(png_data, format='PNG')
    png_data.seek(0)

    # Create a response with the PNG file
    return send_file(png_data, as_attachment=True, download_name='output.png')



def text_file_to_png(text_content, font_size=24, image_size=(600, 400)):
    """Converts text content to a PNG image."""
    img = Image.new('RGB', image_size, color='white')
    draw = ImageDraw.Draw(img)
    # Use a truetype font available on your system or specify the path to a ttf file
    font = ImageFont.truetype("arial.ttf", font_size)
    # Optionally, add some padding or calculate text positioning to center
    draw.text((10, 10), text_content, fill='black', font=font)
    
    # Save image to a bytes buffer
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)  # Move to the start of the bytes buffer

    return img_bytes

@app.route('/text_to_png', methods=['POST'])
def text_to_png():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    # Read the text content from the uploaded file
    text_content = file.read().decode('utf-8')
    
    # Convert text to PNG
    img_bytes = text_file_to_png(text_content)
    
    # Send the PNG image as a downloadable response
    return send_file(
        img_bytes,
        as_attachment=True,
        download_name='converted_image.png',
        mimetype='image/png'
    )

#############



  

if __name__ == '__main__':
    app.run(debug=True)






















if __name__ == '__main__':
    app.run(debug=True)


  














