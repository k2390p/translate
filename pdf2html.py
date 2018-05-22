#!/usr/bin/env python3
"""
PDF to HTML conversion - first step of the process.
Batch processes a folder full of PDFs using pdf2htmlEX
producing a HTML folder.

This HTML uses just CSS positioning for layout. We need
further work to add sematic tags: transcript.py 
"""
import glob, os, time, multiprocessing
import config
from transcript import semanticize
from threading import Thread
from googleTranslateReplace import translationMethod


def pdf2html(language, vendor, pdf_path, upload_folder, file_name, *args):
    fn = pdf_path.split('/')[-1].replace('.pdf','')
    # --embed cfijo = don't embed Css, Fonts, Images, Js, Outlines (> man pdf2htmlEX)
    
    os.system('pdf2htmlEX --embed-external-font 0\
                          --external-hint-tool ttfautohint\
                          --process-nontext 0\
                          --embed cfijo\
                          --dest-dir %s/%s\
                          %s %s.html' % (config.HTML_DIR, fn, pdf_path, fn))
    time.sleep(.2)
    semanticTraget = config.HTML_DIR+"/"+file_name.split('.')[0]+"/"+file_name.split('.')[0]+".html"
    semanticHTM = config.HTM_DIR+"/"+file_name.split('.')[0]+".htm"
    filenName = file_name.split('.')[0]
    semanticize(semanticTraget)    
    # print(semanticHTM + "   _______    "+ filenName)
    translationMethod(semanticHTM, filenName, language, vendor)


if __name__ == '__main__':
    os.makedirs(config.HTML_DIR, exist_ok=True)
    p = multiprocessing.Pool(4)
    print(p.map(pdf2html, glob.glob(config.PDF_DIR + '/*.pdf')))