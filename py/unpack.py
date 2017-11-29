# -*-coding: utf-8 -*-
# #Python 2.7에서 한글 경로 입력을 위해 Python 설치 폴더의 Lib 밑 site.py - setencoding()함수의 첫 if문을 1로 변경

import os, subprocess
import re as rep

import optparse, zipfile, sys

import xml.etree.ElementTree as ET



def execute_cmd(cmd):  # 명령프롬프트를 통해 명령 실행
    my_env = os.environ

    print  (cmd)
    p = subprocess.Popen(cmd, env=my_env, shell=True, stdout=subprocess.PIPE)
    line = p.stdout.readline()

    print   (p.communicate())

def apktool_unpack(apkfile, output):  # 대상 apk 파일 unpacking 및 디버깅을 위한 -d옵션 unpacking
    print("file", apkfile)
    print("output",output)
    execute_cmd('D:/Utils/apktool.bat d "' + apkfile + '" -o "' + output + '" ')
    #execute_cmd('D:/Utils/apktool.bat d -d "' + apkfile + '" -o "' + output + '_d"')

def keytools_unpack(apkfile, output):
    print("file", apkfile)
    print("output",output)
    execute_cmd('"c:\\Program Files\\Java\\jre1.8.0_151\\bin\\keytool.exe" -printcert -file "' + apkfile + '" > "' + output + '.cert" ')

def manifest_unpack(apkfile, output):
    # print("file", apkfile)
    # print("output",output)

    f = open(apkfile, 'r', encoding='utf-8')
    perList = []
    actList = []
    while True:
        line = f.readline()
        if not line: break
        # permissions = rep.findall('"android.permission.*"', line)
        permissions = rep.findall('"android.permission.+[A-Z_]"', line)
        # actions = rep.findall('"android.intent.action.*"', line)
        actions = rep.findall('"android.intent.action.+[A-Z_]"', line)

        if (len(permissions)>0) :
    #        print("!!!!!", permissions)
            perList += permissions
        if (len(actions) > 0):
     #       print("@@@@@", actions)
            actList += actions
    f.close()

    # print(perList, actList)
    fileName = output + '.txt'
    # print(fileName.replace('\\','/'))
    fileName = fileName.replace('\\','/')
    print ("!@#!@#!@# ", fileName)
    fw = open(fileName, 'w', encoding='utf-8')
    fw.write(str(perList))
    fw.write(str(actList))
    fw.close()



def keytool(datapath, outputpath, pos = 6):
    for (path, dir, files) in os.walk(datapath):
        if 'original' not in path:
            continue

        for filename in files:
            ext = os.path.splitext(filename)[-1]
            name = os.path.splitext(filename)[0]

            if ext == '.RSA':
                outname = path.split('\\')[pos]
                print("keytool unpack %s/%s" % (path, filename))
                apktool_path = "%s\\%s" % (outputpath, outname)
                inputpath = "%s/%s" % (path, filename)

                keytools_unpack(inputpath, apktool_path)

def apktool(datapath, outputpath, pos = 6):
    for (path, dir, files) in os.walk(datapath):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            name = os.path.splitext(filename)[0]

            if ext == '.vir':

                print("apk unpack %s/%s" % (path, filename))
                output = "%s\\%s" % (outputpath, name)
                inputpath = "%s/%s" % (path, filename)

                apktool_unpack(inputpath, output)

def manifest(datapath, outputpath, pos = 6):
    for (path, dir, files) in os.walk(datapath):
        if 'original' in path:
            continue
        if 'res' in path:
            continue
        if 'smali' in path:
            continue

        for filename in files:
            if 'AndroidManifest' not in filename:
                continue
            ext = os.path.splitext(filename)[-1]
            name = os.path.splitext(filename)[0]


            if ext == '.xml':
                outname = path.split('\\')[pos]
                print("manifest unpack %s/%s" % (path, filename))
                output = "%s\\%s" % (outputpath, outname)
                inputpath = "%s/%s" % (path, filename)

                manifest_unpack(inputpath, output)


if __name__ == '__main__':
    apktool('D:\\work\\testdata\\Challenge_andro_1st_dataset\\Benign_samples_1st_1500',
            'D:\\work\\testdata\\pretest\\1st\\b')
    apktool('D:\\work\\testdata\\Challenge_andro_1st_dataset\\Malware_samples_1st_500',
            'D:\\work\\testdata\\pretest\\1st\\m')
    apktool('D:\\work\\testdata\\Challenge_andro_2nd_dataset',
            'D:\\work\\testdata\\pretest\\2nd')

    keytool('D:\\work\\testdata\\pretest\\1st\\b', 'D:\\work\\testdata\\outtest\\1st\\b')
    keytool('D:\\work\\testdata\\pretest\\1st\\m', 'D:\\work\\testdata\\outtest\\1st\\m')
    keytool('D:\\work\\testdata\\pretest\\2nd', 'D:\\work\\testdata\\outest\\2nd', 5)

    manifest('D:\\work\\testdata\\pretest\\1st\\b', 'D:\\work\\testdata\\outtest\\1st\\b')
    manifest('D:\\work\\testdata\\pretest\\1st\\m', 'D:\\work\\testdata\\outtest\\1st\\m')
    manifest('D:\\work\\testdata\\pretest\\2nd', 'D:\\work\\testdata\\outtest\\2nd', 5)

    print
    "END"

#출처: http: // yprefer.tistory.com / 2[YPrefer's Develop&Security]