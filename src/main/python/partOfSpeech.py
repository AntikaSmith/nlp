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

def findSpecies(word, annos, offset, string):
    """
    @word: string, like: Tricyclic
    @annos: annotation lines list,like:
        CA2157668C	A	0	22	Tricyclic benzazepines	FAMILY
        CA2157668C	A	105	111	carbon	SYSTEMATIC
    @offset: int, the start offset of the word
    @string: the full text
    """
    for anno in annos:
        try:
            aList = anno.split("\t")
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
    for doc in original.split("\n"):
        if len(doc.split("\t")) < 3:
            print("doc split error:$doc\n" + doc + "\n")
            continue
        docId, title, text = doc.split("\t")
        titleList = word_tokenize(title)
        titleTags = nltk.pos_tag(titleList)
        textList = word_tokenize(text)
        textTags = nltk.pos_tag(textList)
        anno = id2Anno[docId]
        words = set(x for line in anno for x in word_tokenize(line.split("\t")[4]))

        def computeSpecies(tags, string):
            offset = 0
            for tag in tags:
                if tag[0] in words:
                    species, index = findSpecies(tag[0], anno, offset, string)
                    offset = index + len(tag[0])
                    results.append((docId, tag[0], tag[1], index, offset, species))
                else:
                    results.append((docId, tag[0], tag[1], offset, offset + len(tag[0]), "OTHER"))
            return 0
        computeSpecies(titleTags, title)
        computeSpecies(textTags, text)
        results.append("\n")

    crfFile = open("target/" + setName + ".data", "w", encoding = "utf-8")
    for result in results:
        crfFile.write("\t".join(str(i) for i in result) + "\n")
    crfFile.close()
    return 0    
        
    print(id2Anno["CA2128706C"])

import sys
readFile(sys.argv[0])
    
