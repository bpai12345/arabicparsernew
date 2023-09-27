# Importing required packages
import os.path
from ArabicOcr import arabicocr
# from flask import jsonify, Flask, request
from werkzeug.utils import secure_filename
import aspose.words as aw
import fitz, sys
from PIL import Image
import os
import cv2

# app = Flask(__name__)
zoom = 2 # to increase the resolution
mat = fitz.Matrix(zoom, zoom)

# @app.route('/arabic_pdf', methods = ['POST'])
def extraction(filename):
    out_image='./fileDir/out.jpg'
    results=""
    # file = request.files['file']
    # filename = secure_filename(file.filename)
    # file.save(filename)
    extn = filename.split(".")[1]
    if extn in ['jpg', 'jpeg', 'png']: # If uploaded file is image(i.e jpg, jpeg, png) this process will trigger
        results=arabicocr.arabic_ocr(filename,out_image)
    elif extn in ['doc','docx']:
        doc = aw.Document(filename)
        saveOptions = aw.saving.PdfSaveOptions()
        saveOptions.compliance = aw.saving.PdfCompliance.PDF17
        doc.save("temp.pdf", saveOptions)
        doc = fitz.open("temp.pdf")  # open document
        for page in doc:  # iterate through the pages
            pix = page.get_pixmap()  # render page to an image
            pix.save("page-%i.png" % page.number)
            results = arabicocr.arabic_ocr("page-%i.png" % page.number,out_image)
            os.remove("page-%i.png" % page.number)
        doc.close()
        # os.remove(filename)
        # os.remove("temp.pdf")
    else :
        doc = fitz.open(filename)  # open document
        for page in doc:  # iterate through the pages
            pix = page.get_pixmap()  # render page to an image
            pix.save("page-%i.png" % page.number)
            results = arabicocr.arabic_ocr("page-%i.png" % page.number,out_image)
            os.remove("page-%i.png" % page.number)
        doc.close()
        # os.remove(filename)

    words=""
    for i in range(len(results)):
        word=results[i][1]
        words = words+" "+word
    return words
    # return jsonify({'text':words})