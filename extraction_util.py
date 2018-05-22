import pdfbox
from google_translate import translate
import os


def extract_pdf(file_path, upload_folder, file_name, *args):

    print('extracting text from: {0}'.format(file_path))
    p = pdfbox.PDFBox()
    text = p.extract_text(file_path)
    formatted_text = "<br/>".join(text.splitlines())
    translation = translate(formatted_text[0:4000])

    formatted_translation = translation.replace('<br/>', '\n')

    f_name = file_name.split('.')[0]
    uploaded_file_path = os.path.join(upload_folder, f_name + '_translated.txt')

    with open(uploaded_file_path, "w") as f:
        f.write(formatted_translation)
    # trans_text = translation.split('\\n')
    #
    # for t in trans_text:
    #     print(t)


if __name__ == '__main__':
    extract_pdf(r'C:\dev\flask-file-uploader-master\data\sample.pdf')

