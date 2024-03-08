##wrd to htm
import mammoth

#pdf
from pdf2docx import parse
from typing import Tuple
import pdfcrowd
import sys


def convert_pdf2docx(input_file: str, output_file: str, pages: Tuple = None):
    """Converts pdf to docx"""
    if pages:
        pages = [int(i) for i in list(pages) if i.isnumeric()]
    result = parse(pdf_file=input_file,
                   docx_with_path=output_file, pages=pages)
    summary = {
        "File": input_file, "Pages": str(pages), "Output File": output_file
    }
    # Printing Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return result



resume_doc="R1resume_001.docx"
rd=resume_doc.split(".")
resume_pdf=rd[0]+".pdf"
'''resume_html=rd[0]+".html"
custom_styles = "b => i"
input_filename="static/upload/"+resume_doc
with open(input_filename, "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file, style_map = custom_styles)
    text = result.value
    with open("static/upload/"+resume_html, 'w') as html_file:
        html_file.write(text)'''



import aspose.words as aw

# Load word document
doc = aw.Document("static/upload/"+resume_doc)

# Save as PDF
doc.save("static/upload/"+resume_pdf)
