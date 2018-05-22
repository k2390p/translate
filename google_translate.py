# google-cloud-translate==1.3.1


def translate(text):
    # [START translate_quickstart]
    # Imports the Google Cloud client library
    from google.cloud import translate

    # Instantiates a client
    translate_client = translate.Client()

    # The text to translate

    # The target language
    target = 'en'

    # Translates some text into Russian
    translation = translate_client.translate(
        text,
        target_language=target)

    print(translation)
    # print(u'Text: {}'.format(text))
    # print(u'Translation: {}'.format(translation['translatedText']))
    # [END translate_quickstart]
    return translation['translatedText']


if __name__ == '__main__':
    import os
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\\Users\\admin\\Downloads\\338243e517d6.json"
    print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

    text = u'''四、 公司负责人袁仁国、主管会计工作负责人何英姿及会计机构负责人（会计主管人员）陈华声
明：保证年度报告中财务报告的真实、准确、完整。
五、 经董事会审议的报告期利润分配预案或公积金转增股本预案'''

    translate(text)
