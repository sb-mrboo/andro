import csv
import os, subprocess
import pandas as pd
import re as rep
import collections as cl
import random as rd

def getCertInfo(datapath):
    f = open(datapath, 'r')
    num = ''
    al = ''
    while True:
        line = f.readline()
        if not line: break
        cert_num = rep.findall('일련 번호: *', line)
        # print(cert_num)
        if (len(cert_num)> 0 ):
            # print('!!!!',line)
            # print('@@@@',line.split())
            # print('###',line.split()[-1])
            num = line.split()[-1]


        cert_al  = rep.findall('서명 알고리즘 이름: [a-zA-Z0-9]{1,}[^()]', line)
        # print(cert_al)
        if (len(cert_al)> 0 ):
            al = line.split()[-1]
            if ('(' in al):
                al = al.split('(')[0]


    f.close()
    # print(datapath, num,al)
    return (num,al)

def getManifestData(datapath):
    f = open(datapath, 'r', encoding='utf-8')
    list = []
    while True:
        line = f.readline()
        if not line: break
        line = line.replace('[',' ')
        line = line.replace(']', ' ')
        line = line.replace(',', ' ')
        line = line.replace('\'', ' ')
        line = line.replace('\"', ' ')
        list = line.split()

    f.close()

    return (list)


def process(df, datapath = 'D:\\work\\testdata\\out\\2nd',outName = 'filename.csv', classVal = ''):
    print(df)
    """ 
      x1 x2 x3
    i1 1 11 111 
    i2 2 22 222 
    i3 3 33 333 
    """
    # datapath = 'D:\\work\\testdata\\out\\1st\\b'
    # datapath = 'D:\\work\\testdata\\out\\1st\\m'
    #datapath = 'D:\\work\\testdata\\out\\2nd'

    for (path, dir, files) in os.walk(datapath):

        for filename in files:
            ext = os.path.splitext(filename)[-1]
            name = os.path.splitext(filename)[0]

            if ext != '.txt':
                # print()
            # elif  ext == '.cert':
            #     print()
            # else :
                continue

            inputpath = "%s/%s%s" % (path, name, ext)
            # if name in df['hash']:
            #     tempDF = df['hash' == name]
            # else :
            #     tempDF = df.loc[0]

            tempDF = df.loc[0]

            tempDF['hash'] = name
            tempDF['class'] = classVal
            ex_inputpath = "%s/%s%s" % (path, name, '.cert')
            if(os.path.exists(ex_inputpath)):
                certInfo = getCertInfo(ex_inputpath)
                tempDF['cert_num'] =  certInfo[0]
                tempDF['cert_al'] = certInfo[1]

            if ext == '.txt':
                manifestData = getManifestData(inputpath)
                counter = cl.Counter(manifestData)

                for key in counter:

                    if key.find('android', 2) > 2 :
                        print('!!!! ', key)
                        print('!!!! ', filename)
                        continue

                    if key not in df.keys():
                        df[key] = 0

                    tempDF[key] =  counter.get(key)

            # if name in df['hash']:
            #     df.loc[df['hash' == name].index] = tempDF
            # else :
            #     df.loc[len(df)] = tempDF
            df.loc[len(df)] = tempDF

    print(df.shape)
    df.to_csv(outName, sep=',', na_rep='NaN')


def joinFamily(familyFile, orgFile):
    org = pd.read_csv(orgFile)

    family = pd.read_csv(familyFile, usecols=['filename', 'family'])
    family.columns = ['hash', 'family']

    result = pd.merge(org, family, on=['hash'],how='left')
    print(result)
    result['Class'] = result['class'].apply(lambda x: 'Unknown' if 'nan' in str(x).lower() else str(x))
    result['family'] = result['family'].apply(lambda x: 'Unknown' if 'nan' in str(x).lower() else str(x))

    del result["Unnamed: 0"]
    del result["class"]


    train = result[result.Class != 'Unknown']
    test = result[result.Class == 'Unknown']

    test['Class'] = test['Class'].apply(lambda x: str(rd.randrange(0,2)) if 'unknown' in str(x).lower() else str(x))
    test['family'] = test['family'].apply(lambda x: str(rd.randrange(0, 11)))
    print( test['family'])
    # test['family'] = test['family'].apply(lambda x: 'Unknown' if '0' in x else '1')
    test['family'] = test['family'].apply(lambda x : 'Unknown' if '0' in x
                                            else 'opfake' if '1' in x
                                            else 'gappusin' if'2' in x
                                            else 'dowgin' if'3' in x
                                            else 'wapsx' if'4' in x
                                            else 'counterclank' if '5' in x
                                            else 'smstado' if'6' in x
                                            else 'smsagent' if '7' in x
                                            else 'boxer' if '8' in x
                                            else 'adwo' if '9' in x
                                            else 'airpush')
    test1 = test[test.index >= 3000]
    test2 = test[test.index < 3000]

    train.to_csv('last_train.csv', sep=',', na_rep='0', index_label='index')
    test.to_csv('last_test.csv', sep=',', na_rep='0', index_label='index')
    test1.to_csv('last_test1.csv', sep=',', na_rep='0', index_label='index')
    test2.to_csv('last_test2.csv', sep=',', na_rep='0', index_label='index')

def main(output):
    df = pd.DataFrame({'hash':[0], 'cert_num':[0], 'cert_al':[0], 'class':['']})
    datapath = 'D:\\work\\testdata\\out\\1st\\b'
    process(df, datapath, output+ '_1st_b.csv', '0')
    datapath = 'D:\\work\\testdata\\out\\1st\\m'
    process(df, datapath, output+ '_1st_m.csv', '1')
    datapath = 'D:\\work\\testdata\\out\\2nd'
    process(df, datapath, output+ '.csv', '')
# final_data-1128.csv

output = '1128'
# main(output)
joinFamily('D:\Doc\데이터과학연구소\챌린지\모바일\Challenge_andro_1st_dataset\Malware_random_list_1st_500.csv', output+ '.csv')

