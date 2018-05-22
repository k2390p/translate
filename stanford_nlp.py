# Simple usage
from stanfordcorenlp import StanfordCoreNLP
import json

nlp = StanfordCoreNLP(r'C:\dev\nlp_standford\stanford-corenlp-full-2017-06-09', memory='6g', lang='zh')

sentence = '''四、 公司负责人袁仁国、主管会计工作负责人何英姿及会计机构负责人（会计主管人员）陈华声
明：保证年度报告中财务报告的真实、准确、完整。
五、 经董事会审议的报告期利润分配预案或公积金转增股本预案
'''
# print('Tokenize:', nlp.ssplit(sentence))


doc = nlp.annotate(sentence, properties={'annotators': 'ssplit', 'outputFormat': 'json'})
my_json = json.loads(doc)


for sent in my_json["sentences"]:
    print("".join([t["word"] for t in sent["tokens"]]))


# print('Part of Speech:', nlp.pos_tag(sentence))
# print('Named Entities:', nlp.ner(sentence))
# print('Constituency Parsing:', nlp.parse(sentence))
# print('Dependency Parsing:', nlp.dependency_parse(sentence))



nlp.close() # Do not forget to close! The backend server will consume a lot memery.