import docx2txt

# extract text
#text = docx2txt.process("static/upload/R1resume_001.docx")

# extract text and write images in /tmp/img_dir
text = docx2txt.process("static/upload/R1resume_001.docx", "/tmp/img_dir") 
print(text)
