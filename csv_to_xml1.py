from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from xml.dom import minidom
import pandas as pd
import re

diaryData = pd.read_csv('diary.csv', sep=',#', encoding='utf-8')
data = pd.read_csv('persons.csv', sep=',#', encoding='utf-8')


def Cleaner(file):
    with open(file, 'r') as f:
        first = f.readline()
        first = re.sub('"','', first)
        f = f.read()
        f = re.sub('\n', '!!ПЕРЕНОС!!', f)
        f = re.sub('"!!ПЕРЕНОС!!"', '"\n"', f)
        f = re.sub(',#,#', ',#" ",#', f)
    with open(file, 'w') as g:
        g.write(first)
        g.write(f)

def TeiHeader(data, diaryData, n):
    root = Element('teiHeader')

    fileDesc = SubElement(root, 'fileDesc')
    titleStmt = SubElement(fileDesc, 'titleStmt')
    author = SubElement(titleStmt, 'author')

    id = SubElement(author, 'id')
    id.set('type', 'person')
    id.set('id', data["id"][n].strip('"'))
    id.text = data["id"][n].strip('"')

    surname = SubElement(author, 'name')
    surname.set('type', 'surname')
    surname.text = data["lastName"][n].strip('"')
    name = SubElement(author, 'name')
    name.set('type', 'name')
    name.text = data["firstName"][n].strip('"')
    patr = SubElement(author, 'name')
    patr.set('type', 'patronim')
    patr.text = data["thirdName"][n].strip('"')
    nick = SubElement(author, 'name')
    nick.set('type', 'nickname')
    nick.text = data["nickname"][n].strip('"')

    sex = SubElement(author, 'sex')
    if data["gender"][n].strip('"') == '0':
        sex.set('value', 'F')
        sex.text = 'Женский'
    else:
        sex.set('value', 'M')
        sex.text = 'Мужской'

    info = SubElement(author, 'info')
    info.text = data["info"][n].strip('"')
    add_info = SubElement(author, 'add_info')
    add_info.text = data["additional_info"][n].strip('"')

    wiki = SubElement(author, 'wiki')
    wiki.set('href', data["wikiLink"][n].strip('"'))
    wiki.text = 'Wikipedia'

    publicationStmt = SubElement(fileDesc, 'publicationStmt')

    scrmbldInfo = str(data["edition"][n].strip('"'))
    pub = SubElement(publicationStmt, 'publisher')
    publisher = re.search('\*\*Издания: \*\*(.*?)\*\*', scrmbldInfo)
    if publisher:
        publisher = publisher.group(1)
    if publisher == None:
        publisher = re.search('(\*\*Издания: \*\*)(.*?)', scrmbldInfo)
        if publisher:
            publisher = publisher.group(1)
    if publisher == None:
        publisher = ''
    for i in publisher.split('!!Перенос!!!!Перенос!!'):
        pub = SubElement(publicationStmt, 'publisher')
        pub.text = i

    diaryInfo = SubElement(fileDesc, 'daityInfo')
    idDiary = SubElement(diaryInfo, 'idDiary')
    idDiary.set('value', str(diaryData['"id"'][n-1]).strip('"'))
    idDiary.text = str(diaryData['"id"'][n-1]).strip('"')
    startDate = SubElement(diaryInfo, 'date')
    startDate.set('event', 'start')
    startDate.set('when', diaryData['"firstNote"'][n-1].strip('"'))
    endDate = SubElement(diaryInfo, 'date')
    endDate.set('event', 'end')
    endDate.set('when', diaryData['"lastNote"'][n-1].strip('"'))
    status = SubElement(diaryInfo, 'status')
    status.text = diaryData['"status"'][n-1].strip('"')

    sourceDesc = SubElement(root, 'sourceDesc')
    s = SubElement(sourceDesc, 'source')
    source = re.search('\*\*Источник:\*\*(.*?)\*\*', scrmbldInfo)
    if source:
        source = source.group(1)
    if source == None:
        source = re.search('\*\*Источник:\*\*(.*?)$', scrmbldInfo)
        if source:
            source = source.group(1)
    if source == None:
        source = ''
    sourcetext = re.search('[.*?]', source)
    link = re.search('(http.*?)', source)
    if link != None:
        s.sub('href', link)
    else:
        sourcetext = source
    s.text = sourcetext

    revisionDesc = SubElement(root, 'revisionDesc')
    rev = re.search('\*\*Подготовка текста:\*\*(.*?)\*\*', scrmbldInfo)
    if rev:
        rev = rev.group(1)
    if rev == None:
        rev = re.search('\*\*Подготовка текста:\*\*(.*?)$', scrmbldInfo)
        if rev:
            rev = rev.group(1)
    if rev == None:
        rev = ''
    for i in rev.split(','):
        SubElement(revisionDesc, 'revisionist').text = i

    return root

def bodyTei(entryData):
    root = Element('body')
    print(entryData)
    for i in range(1, len(entryData)):
        root.append(entry(entryData, i))
    return root

def entry(data, n):
    root = Element('div')
    root.set('type', 'entry')
    root.set('id', data['"id"'][n].strip('"'))
    header = SubElement(root, "entryHeader")
    date = SubElement(header, "date")
    date.set('when', data['"date"'][n].strip('"'))
    if data['"dateTop"'][n].strip('"') != '0000-00-00':
        date.set('type', 'start')
        date2 = SubElement(header, "date")
        date2.set('type', 'end')
        date2.set('when', data['"dateTop"'][n].strip('"'))
    if data['"julian_calendar"'][n].strip('"') == '1':
        date.set('calendar', 'Julian')
        date2.set('calendar', 'Julian')
    text_el = SubElement(root, "text")
    text = data['"text"'][n].strip('"')
    text = re.sub('[ ]{2,}', '\n', text)
    text_el.text = text
    return root

def Tei(data, diaryData, notes):
    root = Element('ProjitoCorpora')
    root.append(TeiHeader(data, diaryData, n=175))
    notes = notes[notes['"diary"'] == '"194"']
    root.append(bodyTei(notes))
    return root

#print(tostring(TeiHeader(data.iloc[[175]], diaryData, 175)))

notes = pd.read_csv('notes_beautiful_short.csv', sep=',#', encoding='utf-8')
notes = notes[notes['"diary"'] == '"194"']
tree = tostring(Tei(data, diaryData, notes), encoding="unicode")
xmlstr = minidom.parseString(tree).toprettyxml(indent="   ")
with open('TEI.xml', 'w', encoding='utf-8') as f:
    f.write(xmlstr)
