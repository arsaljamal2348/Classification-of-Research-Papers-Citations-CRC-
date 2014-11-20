__author__ = 'CRC'

import re
import itertools
import operator

def getMaincontents(str1,str2):

    s1 = ''
    s2 = ''
    s3 = ''
    main_Title = re.findall(r'\w.*\s.*',str1)
    citing_Title = re.findall(r'\w.*\s.*\w.*\s.*',str2)
    abstract=['ABSTRACT','Abstract']
    intro=['INTRODUCTION','Introduction']

    for i in range(len(abstract)):
     if re.findall(re.compile(abstract[i]+'[\s\S]*?'+intro[i]),str1):
      temp = re.findall(re.compile(abstract[i]+'[\s\S]*?'+intro[i]),str1)
      clean = re.sub(re.compile(abstract[i]),"",temp[0])
      clean2 = re.sub(re.compile(intro[i]+'$'),"",clean)
      clean3 = re.sub(r'1.|I.|1|I$',"",clean2)
      main_Abstract = clean3

    if main_Title:
        s1 = main_Title[0].strip("\n")
    else:
        s1 = 'Did not find'

    if main_Abstract:
         s2 = main_Abstract.strip("\n")

    else:
      s1 = 'Did not find'

    if citing_Title:
        s3 = citing_Title[0].strip("\n")
    else:
        s3 = 'Did not find'
    return s1,s2,s3

def removeStopwords(stopList, documents):
    for item in stopList:
        for docNum in range(len(documents)):
                if item == documents[docNum]:
                    documents.pop(docNum)
                    documents.insert(docNum, "")
                    # print item + "\n" + clean_corpus[i]

    for i in range(len(documents)):
        documents[i] = filter(operator.methodcaller('strip'), documents[i])
    documents = filter(None,documents)
    return documents

def ifTitleExists(test_str,str1):
 Main = re.findall(r'[A-z][a-z\']*',str1)

 stopWordList=['is','the','of','all','and','to','can','be','as','once','for','at','am','are','has','have','had','up','his','her','in','on','no','we','do']
 clean = removeStopwords(stopWordList, Main)
 #print "\n Line62-Cleaned Title "+str(clean)+"\n"
 #map(lambda x:x.lower(),["A","B","C"])
 combo1=map(lambda x:x.lower(),clean)
 #print "\n Line62-Cleaned Title "+str(combo1)+"\n"
 combo2=[len(clean)]
 for i in range(len(clean)):
     if i==0:
         combo2[0]=clean[0]
     else:
         temp=''
         temp = clean[i].lower()
         combo2.append(temp)
 #print "\n Line62-Combo2"+str(combo2)+"\n"

 Main_title = []
 if len(Main) >= 10:
     for i in range(10):
         Main_title.append(Main[i])
 else:
   Main_title = Main

 combinations = []
 match = []
 result = []

 for L in range(2, len(Main_title)+1):
   for subset in itertools.combinations(Main_title, L):
    combinations.append(list(subset))

 store = ""
 for i in range(len(combinations)):
  for words in combinations[i]:
     store += str(words + " ")
  result.append(str(store))
  store = ""

 for i in reversed(range(len(result))):
     if re.findall(re.compile(result[i].strip(" ")),test_str):
        match.append(re.findall(re.compile(result[i].strip(" ")),test_str))
        return reference_in_citingPaper(test_str,reference_Main(test_str,match[0]))
 return "could not find main reference in citing paper"

def reference_Main(test_str,str1):

    reference=['REFERENCES','References']
    crop2 = ""

    for i in range(len(reference)):
      if(re.findall(re.compile(reference[i]+'[\S\s]*?'),test_str)):
         crop2=re.findall(re.compile(reference[i]+'[\S\s]*?$'),test_str)



    p = re.compile(str1[0]+'[\s\S]*\.\n+\[\d{0,3}\]')
    match = re.findall(p,crop2[0])
    result = str(match[0])
    innerBracket = []
    outerBracket = []
    reference = 0
    #print result
    for i in range(len(result)):
        if result[i] == "[":
          innerBracket.append(i)
        elif result[i] == "]":
          outerBracket.append(i)

    if outerBracket[0] - innerBracket[0] == 2:
        reference = result[innerBracket[0]+1]#print result[innerBracket[0]+1]
    elif outerBracket[0] - innerBracket[0] == 3:
        reference = result[innerBracket[0]+1]+""+result[outerBracket[0]-1]#print result[innerBracket[0]+1]+""+result[outerBracket[0]-1]
    elif outerBracket[0] - innerBracket[0] == 4:
        reference = result[innerBracket[0]+1]+""+result[innerBracket[0]+2]+""+result[outerBracket[0]-1]#print result[innerBracket[0]+1]+""+result[innerBracket[0]+2]+""+result[outerBracket[0]-1]
    return reference

def reference_in_citingPaper(test_str,main):

 reference=['REFERENCES','References']
 crop2 = ""

 for i in range(len(reference)):
      if(re.findall(re.compile(reference[i]+'[\S\s]*?'),test_str)):
         crop2=re.findall(re.compile(reference[i]+'[\S\s]*?$'),test_str)

 max = re.findall(re.compile('(\[\d{0,3}\])'),crop2[0])
 maxRef = max[len(max)-1]
 maxRef2 = "\\"+maxRef

 final = '\['+main+'\]'
 initial = '\['+str(int(main)-1)+'\]'

 p1 = re.compile(initial+'[\s\S]*?'+final)
 p2 = re.compile(maxRef2+'[\s\S]*?$')

 if re.findall(p1,crop2[0]):
  match = re.findall(p1,crop2[0])
 elif re.findall(p2,crop2[0]):
   match = re.findall(p1,crop2[0])
   return match[0]

 result = match[0]
 innerBracket = []
 outerBracket = []
 reference = 0
 for i in range(len(result)):
        if result[i] == "[":
          innerBracket.append(i)
        elif result[i] == "]":
          outerBracket.append(i)
 if outerBracket[1] - innerBracket[1] == 2:
        reference = innerBracket[1]#print result[innerBracket[0]+1]
 elif outerBracket[1] - innerBracket[1] == 3:
        reference = innerBracket[1]#print result[innerBracket[0]+1]+""+result[outerBracket[0]-1]
 elif outerBracket[1] - innerBracket[1] == 4:
        reference = innerBracket[1]#print result[innerBracket[0]+1]+""+result[innerBracket[0]+2]+""+result[outerBracket[0]-1]
 #for i in range(len(result[reference]-1)):

 return result[0:reference-1]

if __name__ == '__main__':


  f1 = open('IEEE Format Paper\\Android Security\\Main.txt') #1,2,7
  f2 = open('IEEE Format Paper\\Android Security\\1.txt')

  str1 = f1.read()
  str2 = f2.read()

  Main_Title,Main_Abstract,Citing_Title=getMaincontents(str1,str2)
  print "Main_Title: ",Main_Title
  print
  print "Citing_Title: ",Citing_Title
  print
  print "Main_Abstract: ",Main_Abstract
  print
  print "Reference Of Main Paper: ",ifTitleExists(str2,Main_Title)
