import sys
import re

wordCountDict={}
biGramTableWithoutSmoothing=[]
biGramTableWithSmoothing=[]
biGramProbWithoutSmoothing=[]
biGramProbWithSmoothing=[]
totalVocabulary = 0

def calcVocaulary():
    tokens=[]
    corpus = sys.argv[1]
    with open("Corpus.txt",'r') as f:
        for line in f:
            for word in line.split():
                if(word==',' or word=='.' or word==':' or word==';' or word=='-'):
                    continue
                else:
                    tokens.append(word.lower())
    #elimiate duplicates
    x=[]
    for word in set(tokens):
        x.append(word)
    tokens=x
    #print("Vocaulary:",len(tokens))
    totalVocabulary = len(tokens)
    return len(tokens)


def unigramWithoutSmoothing(sentence):
    wordCountDict.clear()
    wordList = splitInputSentence(sentence)
    for word in wordList:
        count=0
        strPattern1 = r"[\s+\.,!;\?:\b^]"+word+r"\b[\s+$\.,!;\?:]"
        strPattern2 = r"^"+word+r"\b[\s+$\.,!;\?:]"
        count += patternCount(strPattern1)
        count += patternCount(strPattern2)
        wordCountDict[word]=count
    #print('\nUnigram count for sentence:\n\n'+sentence+'\n')
    #print(wordCountDict)
    
def buildBigramTableWithoutSmoothing(sentence):
    biGramTableWithoutSmoothing.clear()
    wordList1 = splitInputSentence(sentence)
    wordList2 = wordList1
    
    for word1 in wordList1:
        tempList=[]
        for word2 in wordList2:
            count = 0
            strPattern1 = r'[\s+\.,!;\?:\b^]'+word1+r'[\b\.,!;\?:\s+]\b'+word2+r'\b[\s+$\.,!;\?:]'
            count+=patternCount(strPattern1)
            tempList.append(count)
        biGramTableWithoutSmoothing.append(tempList)
    #print('\nBigram count for sentence without smoothing:\n\n'+sentence+'\n')
    print('\nBigram count without smoothing:\n')
    for l in biGramTableWithoutSmoothing:
        print(l,'\n')
        
def buildBigramTableWithSmoothing(sentence):
    biGramTableWithSmoothing.clear()
    wordList1 = splitInputSentence(sentence)
    wordList2 = wordList1
    
    for word1 in wordList1:
        tempList=[]
        for word2 in wordList2:
            count = 0
            strPattern1 = r'[\s+\.,!;\?:\b^]'+word1+r'[\b\.,!;\?:\s+]\b'+word2+r'\b[\s+$\.,!;\?:]'
            count+=patternCount(strPattern1)
            tempList.append(count+1)
        biGramTableWithSmoothing.append(tempList)
    #print('\nBigram count for sentence with smoothing:\n\n'+sentence+'\n')
    print('\nBigram count with smoothing:\n')
    for l in biGramTableWithSmoothing:
        print(l,'\n')
        
def bigramProbWithoutSmoothing(sentence):
    biGramProbWithoutSmoothing.clear()
    i = 0
    wordList = splitInputSentence(sentence)
    for word in wordList:
        deno = wordCountDict[word]
        l = biGramTableWithoutSmoothing[i]
        tempList=[]
        for entry in l:
            tempList.append(entry/deno)
        biGramProbWithoutSmoothing.append(tempList)
        i+=1
    #print('\nBigram probability for sentence without smoothing:\n\n'+sentence+'\n')
    print('\nBigram probability without smoothing:\n')
    for l in biGramProbWithoutSmoothing:
        print(l,"\n")

def bigramProbWithSmoothing(sentence):
    biGramProbWithSmoothing.clear()
    totalVocabulary=calcVocaulary()
    i = 0
    wordList = splitInputSentence(sentence)
    for word in wordList:
        deno = wordCountDict[word]+totalVocabulary
        l = biGramTableWithSmoothing[i]
        tempList=[]
        for entry in l:
            tempList.append(entry/deno)
        biGramProbWithSmoothing.append(tempList)
        i+=1
    #print('\nBigram probability for sentence with smoothing:\n\n'+sentence+'\n')
    print('\nBigram probability with smoothing:\n')
    for l in biGramProbWithSmoothing:
        print(l,"\n")
    
def splitInputSentence(inputSentence):
    token = []
    wordList = inputSentence.split(" ")
    for word in wordList:
        if word!=',' and word!=";" and word!="-" and word!=".":
            token.append(word)
    wordList=token
    return wordList

def patternCount(regex):
    corpus = sys.argv[1]
    try:
        f = open(corpus)
        fileContent = f.read()
        pattern = re.compile(regex, re.IGNORECASE)
        res = re.findall(pattern, fileContent)
        return len(res)
    except Exception as e:
        print(e.type)
        return 0
    
def totalProbWithOutSmoothing(sentence):
    wordList = splitInputSentence(sentence)
    prob=1.0
    for i in range(1,len(wordList)-1):
        prob*=biGramProbWithoutSmoothing[i-1][i]
    i = i+1
    prob*=biGramProbWithoutSmoothing[i-1][i]
    
    #total number of lines in the corpus
    content = open(sys.argv[1]).read()
    lines = content.split(".")
    num_lines = len(lines )
    
    #prob of start of the word
    strPattern = r"\.\s*"+wordList[0]+r"\s+"
    count1 = patternCount(strPattern)
    strPattern = r"^"+wordList[0]+r"\b[\s*$\.,!;\?:]"
    count1+= patternCount(strPattern)
    prob*=(count1/num_lines)
    
    #prob of end of the word
    strPattern = r"[\s+,!\?:]"+wordList[-1]+r"\s*[\.;$]"
    count2 = patternCount(strPattern)
    prob*=(count2/num_lines)

    print("\nTotal prob without smoothing:",prob)

def totalProbWithSmoothing(sentence):
    totalVocabulary=calcVocaulary()
    wordList = splitInputSentence(sentence)
    prob=1.0
    for i in range(1,len(wordList)-1):
        prob*=biGramProbWithSmoothing[i-1][i]
    prob*=biGramProbWithSmoothing[i-1][i]
        
    #total number of lines in the corpus
    content = open(sys.argv[1]).read()
    lines = content.split(".")
    num_lines = len(lines )
    
    #prob of start of the word
    strPattern = r"\.\s*"+wordList[0]+r"\s+"
    count1 = patternCount(strPattern)
    strPattern = r"^"+wordList[0]+r"\b[\s*$\.,!;\?:]"
    count1+= patternCount(strPattern)
    prob*=((count1+1)/(num_lines+totalVocabulary))
        
    #prob of end of the word
    strPattern = r"[\s+,!\?:]"+wordList[-1]+r"\s*[\.;$]"
    count2 = patternCount(strPattern)
    prob*=((count2+1)/(num_lines+totalVocabulary))
    
    print("\nTotal prob with smoothing:",prob)
    
def withoutSmoothing(sentence):
    buildBigramTableWithoutSmoothing(sentence)
    bigramProbWithoutSmoothing(sentence)
    totalProbWithOutSmoothing(sentence)

def withSmoothing(sentence):
    calcVocaulary()
    buildBigramTableWithSmoothing(sentence)
    bigramProbWithSmoothing(sentence)
    totalProbWithSmoothing(sentence)
    
def main():
    corpus = sys.argv[1]
    sentence1 = (sys.argv[2]).strip()
    sentence2 = (sys.argv[3]).strip()
    print("****** SENTENCE1 ********\n")
    print(sentence1)
    unigramWithoutSmoothing(sentence1)
    withoutSmoothing(sentence1)
    withSmoothing(sentence1)
    print("****** SENTENCE2 ********\n")
    print(sentence2)
    unigramWithoutSmoothing(sentence2)
    withoutSmoothing(sentence2)
    withSmoothing(sentence2)
    
if __name__ == "__main__":
    main()
