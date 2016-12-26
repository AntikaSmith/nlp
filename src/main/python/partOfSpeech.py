import nltk
import os
from nltk.tokenize import word_tokenize

def buildMap(data):
    """
    build the map from document id to annotation lines
    @data: raw data string
    """
    dList = data.split("\n")
    dDict = dict()
    for line in dList:
        key = line.split("\t")[0]
        if (key in dDict):
            dDict[key].append(line)
        else:
            dDict[key] = [line]
    return dDict

def matchAnno(word, annos, offset, string):
    """
    @word: string, like: Tricyclic
    @annos: annotation lines list,like:
        CA2157668C	A	0	22	Tricyclic benzazepines	FAMILY
        CA2157668C	A	105	111	carbon	SYSTEMATIC
    @offset: int, the start offset of the word
    @string: the full text
    """
    for aList in annos:
        try:
            index = string.index(word, offset)
            if int(aList[2]) == index:
                return ("B" + aList[-1], index)
            elif int(aList[2]) < index and int(aList[3]) > index:
                return ("I" + aList[-1], index)
        except ValueError:
            while(offset < len(string) -1 and string[offset] == ' '):
                offset += 1
            return ("OTHER", offset)#if the word has been parsed
    while(offset < len(string) -1 and string[offset] == ' '):
                offset += 1
    return ("OTHER", offset)

def allocateTag(tags):
    result = []
    import re
    for tag in tags:
        for word in re.split('(-)', tag[0]):
            if word != '':
                result.append((word, tag[1]))
    return result

def lexFeature(rawWord):
    word = rawWord.strip()
    import re
    hasPunkt = len(re.findall('\w', word)) != len(word)
    hasDigit = len(re.findall('\d', word)) != 0
    firstIsCapital = (word[0] >= 'A' and word[0] <= 'Z')
    allAreCapital = False
    if firstIsCapital:
        allAreCapital = (re.match('[A-Z]+', word).string == word)
    prefix = word[0:4]
    postfix = word[-4:]
    stem = ''
    if len(word) <= 4:
        stem = word
    else:
        stem = word[2:5]
    return [hasPunkt, hasDigit, firstIsCapital, allAreCapital, prefix, postfix, stem]
    
    

def readFile(setName):
    """
    @setName: the name of the dataset. It can be train, dev or test
    """
    file = open("target/original_" + setName + ".tsv", "r", encoding = "utf-8")
    original = file.read()
    file.close()
    file = open("target/annotation_" + setName + ".tsv", "r", encoding = "utf-8")
    annotation = file.read()
    file.close()

    id2Anno = buildMap(annotation)

    results = []
    import nltk.data
    sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for doc in original.split("\n"):
        if len(doc.split("\t")) < 3:
            print("doc split error:$doc\n" + doc + "\n")
            continue
        docId, title, text = doc.split("\t")
        annos = [anno.split('\t') for anno in id2Anno[docId]]
        tAnnos = [anno for anno in annos if anno[1] == 'T']
        aAnnos = [anno for anno in annos if anno[1] == 'A']
        
        def computeSpecies(tags, string, annosPlaceholder):
            offset = 0
            for tag in tags:
                annoClass, index = matchAnno(tag[0], annosPlaceholder, offset, string)
                offset = index + len(tag[0])
                results.append([docId, tag[0], index, offset, tag[1]] + lexFeature(tag[0]) + [annoClass])
        
        titleList = word_tokenize(title)
        titleTags = allocateTag(nltk.pos_tag(titleList))
        computeSpecies(titleTags, title, tAnnos)
        results.append("\n")
        
        sentenceList = sentence_detector.tokenize(text)
        for sentence in sentenceList:
            textList = word_tokenize(sentence)
            textTags = allocateTag(nltk.pos_tag(textList))

            computeSpecies(textTags, text, aAnnos)
            results.append("\n")

    crfFile = open("target/" + setName + ".data", "w", encoding = "utf-8")
    for result in results:
        crfFile.write("\t".join(str(i) for i in result) + "\n")
    crfFile.close()
    return 0

import sys
readFile(sys.argv[1])
    
