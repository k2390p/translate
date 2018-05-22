# google-cloud-translate==1.3.1
# coding=utf8
import os
from io import BytesIO
import json
from bs4 import BeautifulSoup
import re
import time
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator
start_time = time.time()

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

    # print(soup)
    # print(u'Text: {}'.format(text))
    # print(u'soup: {}'.format(soup['translatedText']))
    # [END translate_quickstart]
    # print(translation)
    return translation['translatedText']


def translationMethod(doc_path, file_name, language, vendor):
    import os
    looper = 0
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./338243e517d6.json"
    translation = ''
    lines = ''
    # print("The doc path recieved for google is : "+doc_path)
    with open(doc_path) as f:
        lines = ''.join(f.readlines())

    # html = lines.decode('utf-8', 'ignore')
    # lines = lines.replace('<br>', '\n')
    # lines = lines.replace('\n', ' ')
    # print(lines)

    destination_lines = lines
    # destination_lines = destination_lines.replace('<br>', '')

    ignore_tags = ['html', 'head', 'meta', 'body', 'tr', 'td']

    # print(lines.find('二、'))
    soup = BeautifulSoup(lines, 'lxml')
    tags = soup.find_all()

    for ii, tag in enumerate(tags):
        print(str(looper) + " Lines done out of " + str(len(tags)))
        looper+=1
        if tag.name not in ignore_tags:
            if tag.name == 'table':
                for row in tag.findAll("tr"):
                    cells = row.findAll("td")

                    for cell in cells:
                        text = cell.text.strip()
                        if vendor == "Google":
                            translated = translate(text)
                        if vendor == "Watson":
                            translated = translationWatson(text, language)
                        # destination_lines = re.sub(r'\b%s\b' % text, translated, destination_lines, re.UNICODE)
                        cell.string = translated

            else:
                text = tag.text.strip()

                # print(text)
                if vendor == "Google":
                    translated = translate(text)
                if vendor == "Watson":
                    translated = translationWatson(text, language)
                # print(translated)
                # print('=============')
                # if we find match on whole text, replace
                # else try to match on tags
                # if destination_lines.find(text) != -1:
                # destination_lines = re.sub(u"\b一、 公司董事会、\b", translated, destination_lines, re.UNICODE)
                tag.string = translated

                # else:
                #     print('could not find', tag)

        # if(looper == 20):
        #     looper = 0
        #     print('#### TRANSLATED FILE CREATED ##### ')
        #     Html_file= open("/Users/FITLab/Documents/translate/"+file_name+"_translated_google.html","w")
        #     Html_file.write(str(soup).rstrip())
        #     Html_file.close()
        #     Html_file2= open("./data/"+file_name+"_translated.html","w")
        #     Html_file2.write(str(soup).rstrip())
        #     Html_file2.close()

            
            


    # print(destination_lines.find('第二节  公司简介和主要财务指标 '))

    # print(lines)
    new_soup = BeautifulSoup('<link rel="stylesheet" href="https://rawgit.com/k2390p/cdstk/master/style.css" type="text/css">', 'lxml')
    soup.head.append(new_soup)

    soup = str(soup).replace(r"\n","")
    soup = str(soup).replace(r"\U000f0401","")
    soup = str(soup).replace(r"\ n","")
    soup = str(soup).replace("&#39;, &#39;","")
    soup = str(soup).replace("&#39;","")
    soup = str(soup).replace(r"\U000f03ff","")
    soup = str(soup).replace(r"  "," ")
    soup = str(soup).replace(r"   "," ")
    soup = str(soup).replace("󰐁","")
    soup = str(soup).replace(r"󰐁","")
    
    
    
    
   
    
    # print("################")
    
    print('#### TRANSLATED FILE CREATED ##### ')
    DATA_DIR_OUT = os.path.curdir
    HTML_DIR_OUT  = os.path.join(DATA_DIR_OUT, 'OUTPUT_FOLDER')
    
    
    Html_file= open(HTML_DIR_OUT+"/"+file_name+"_"+language+"_to_English_translated_google.html","w")
    Html_file.write(soup.rstrip())
    Html_file.close()

    Html_file2= open("./data/"+file_name+"_translated.html","w")
    Html_file2.write(soup.rstrip())
    Html_file2.close()

    print("--- %s seconds ---" % (time.time() - start_time))
    # print(translate(text))


def translationWatson(text2trans,language):
        #watson credentials
    language_translator = LanguageTranslator(
    username='d0d279bc-31a0-4468-ac0b-37118d36b4f7',
    password='Qt4TvHYUNvdy')

    model = ""
    if language == "Chinese":
        model = 'zh-en-patent'
    
    if language == "Japanese":
        model = 'zh-en-patent'

    translation = language_translator.translate(
    text=text2trans, 
    model_id='zh-en-patent')
    print(json.dumps(translation, indent=2, ensure_ascii=False))