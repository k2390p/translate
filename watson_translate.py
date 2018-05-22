# google-cloud-translate==1.3.1
# coding=utf8
import os
import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import json
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator

def translate(text):
    # [START translate_quickstart]
    # Imports the Google Cloud client library
    from google.cloud import translate
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./338243e517d6.json"
    # Instantiates a client
    translate_client = translate.Client()

    # The text to translate

    # The target language
    target = 'en'

    # Translates some text into Russian
    translation = translate_client.translate(
        text,
        target_language=target)

    # print(translation)
    # print(u'Text: {}'.format(text))
    # print(u'Translation: {}'.format(translation['translatedText']))
    # [END translate_quickstart]
    return translation['translatedText']


if __name__ == '__main__':
    import os
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./338243e517d6.json"
    #print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    
    #watson credentials
    language_translator = LanguageTranslator(
    username='d0d279bc-31a0-4468-ac0b-37118d36b4f7',
    password='Qt4TvHYUNvdy')

    path=r"/Users/FITLab/Desktop/watson/chinese_reduced.pdf"
    print(path)
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    codec = 'utf-8'
    format='text'
    password=''
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text2trans = retstr.getvalue().decode()
    fp.close()
    device.close()
    retstr.close()


    translation = ""
    # print('#### HTML FILE CREATED ##### ')
    # Html_file= open("chinese_reduced.html","w")
    # Html_file.write(text2trans)
    # Html_file.close()
    # num_lines = sum(1 for line in open('chinese_reduced.html'))
    # print(num_lines)
    with open('/Users/FITLab/Desktop/watson/HTML/chinese_reduced/chinese_reduced.html') as f:
        lines = f.readlines()
    for i in range(0, len(lines), 20):
        print("#"+str(i))
        x = lines[i:i+20]
        # print(str(x))
        # str(x).replace('\ n','')
        # str(x).replace('\ N','')
        # x = str(x).replace('\n','')
        translation+=translate(str(x))
        

    # text = [text2trans[start:start+2000] for start in range(0, len(text2trans), 2000)]
    # translation = ""
    # models = language_translator.list_models()
    # for item in text[:]:
        # print("#### TEXT being printed  : "+item)
        # translation = language_translator.translate(
        # text=item, 
        # model_id='zh-en-patent')
        # print(item)
        #translation+=translate(item)
        # print(json.dumps(translation, indent=2, ensure_ascii=False))

    # print(json.dumps(models, indent=2))
    # print("#### All TEXT IS TRANSLATED ####" + json.dumps(translation, indent=2, ensure_ascii=True))
    # translation = language_translator.translate(
    # text=text2trans, 
    # model_id='zh-en-patent')
    # print(json.dumps(translation, indent=2, ensure_ascii=False))

    # print("################")
    translation = translation.replace(r"\n","")
    translation = translation.replace(r"\U000f0401","")
    translation = translation.replace(r"\ n","")
    translation = translation.replace("&#39;, &#39;","")
    translation = translation.replace("&#39;","")
    translation = translation.replace(r"\U000f03ff","")
    translation = translation.replace(r"  "," ")
    translation = translation.replace(r"   "," ")
    
    
    
    
    
    print(translation)
    # print("################")
    
    print('#### TRANSLATED FILE CREATED ##### ')
    Html_file= open("/Users/FITLab/Desktop/watson/HTML/chinese_reduced/htmlFile_translated.html","w")
    Html_file.write(translation.rstrip())
    Html_file.close()

    # print(translate(text))
