#!/usr/bin/python3
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import random
from random import randint
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def getBaseFunction(codetag):
    ans=""
    for tag in codetag:
        ans+=tag.text
    return ans;

def getCont(cont):
    ques={}
    ans=""
    ptags=cont.find_all("p")
    for tag in ptags:
        if len(tag.text) == 1:
            break
        else:
            ans+=(tag.text+"\n")
    #print(ans)
    ques["statement"]= ans
    testcase=[]
    pretag=cont.find_all("pre")
    for i in range(0, len(pretag)):
        case={}
        case["content"]=pretag[i].text
        if pretag[i].findPrevious().name == "img":
            image=pretag[i].findPrevious()
            case["imageSrc"]= image["src"]
        else:
            case["imageSrc"]= None
        testcase.append(case)
    ques["testcase"]=testcase
    return ques

def getAccuracy(accDump):
    accepted=accDump[0].text
    accepted=int(accepted.replace(',', ''))
    submission=accDump[1].text
    submission=int(submission.replace(',', ''))
    if submission == 0:
        return 0
    else:
        return accepted/submission
def getVotes(votesDump):
    vote={
        "upVote": -1,
        "downVote": -1
    }
    for item in votesDump:
        if item.text != "Add to List" or item.text != "Share":
            #print(item.text)
            if vote["upVote"] == -1:
                vote["upVote"]= item.text
            elif vote["downVote"] == -1:
                vote["downVote"]= item.text
    return vote
def getSimilarQues(quesDump):
    queslist=[]
    for item in quesDump:
        data={}
        qName=item.find_all("a", class_="title__1kvt")
        qDiff=item.find_all("div", class_="difficulty__ES5S")
        data["name"]=qName[0].text
        data["quesLink"]=qName[0].attrs["href"]
        data["difficulty"]=qDiff[0].text
        queslist.append(data)
    return queslist

def getElements(comp):
    elements=[]
    for item in comp:
        data=item.text
        if data != "Yes" and data != "No" and data != "More":
            elements.append(data)
    return elements

def parseDoc(filename):
    questionInfo={}
    with open(filename) as fp:
        soup=BeautifulSoup(fp,'html.parser')
        #Question Name
        extra=" - LeetCode"
        title=soup.title.text
        if title.endswith(extra):
            title=re.sub(extra, '', title)
        questionInfo["name"]=title
        #Question Difficulty
        questionInfo["difficulty"]=soup.find("div", attrs={"diff":True}).text
        votesDump=soup.find_all("button", class_="btn__r7r7")
        votes=getVotes(votesDump)
        #Question Votes
        questionInfo["votes"]=votes;
        accDump=soup.find_all("div", class_="css-jkjiwi")
        #Question Accuracy
        questionInfo["accuracy"]= getAccuracy(accDump)*100
        #Getting Helper Function
        codetags=soup.find_all("pre", class_="CodeMirror-line")
        questionInfo["baseFunction"]=getBaseFunction(codetags)
        queslinkDump=soup.find("div", attrs={"data-key": "description", "data-disabled":"false"})
        link=queslinkDump.find("a")
        questionInfo["queslink"]=link['href']
        des=soup.find_all("div", class_=re.compile("^description"))
        #Fetching the content 
        cont=des[0].find_all("div", class_="question-content__JfgR")
        if len(cont) != 0:
            questionInfo["content"]= getCont(cont[0])
        else:
            questionInfo["content"]= "Content doesn't exist"
        #Getting Company Tags
        comp=des[0].find_all("span", class_="btn-content__10Tj")
        companies=getElements(comp)
        if len(companies) != 0:
            questionInfo["companies"]=companies
        else:
            questionInfo["companies"]=[]
        #Getting Question Tags
        quest=des[0].find_all("span", class_="tag__2PqS")
        questionTags=getElements(quest)
        if len(questionTags) != 0:
            questionInfo["topicTag"]=questionTags
        else:
            questionInfo["topicTag"]=[]
        #Get Similar Questions
        simques=des[0].find_all("div", class_="question__25Pw")
        similarQuest=getSimilarQues(simques)
        if len(similarQuest) != 0:
            questionInfo["similarQuestion"]=similarQuest
        else:
            questionInfo["similarQuestion"]=[]
        colleges=['IIT Guwahati', 'IIIT Hyderabad', 'IIIT Guwahati', 'IIT KGP', 'IIT Delhi', 'IIT Bombay', 'Bits Pilani', 'Bits Goa', 'NIT Silchar', 'NIT Kurukshetra', 'YMCA']
        job_nature=['FT', 'Internship', 'Both']
        mode=['Online', 'Offline', 'both']
        questionInfo["colleges"]=random.sample(colleges, randint(0,6))
        questionInfo["jobNature"]=random.choice(job_nature)
        questionInfo["mode"]=random.choice(mode)
        return questionInfo

def obj_dict(obj):
    return obj.__dict__

def main():
    filelist=open("config.txt").read().splitlines()
    result=[]
    count=0
    for filename in filelist:
        try:
            if count == 334:
                count+=1
                continue
            info=parseDoc(filename) 
            result.append(info)
            count=count+1
            if count == 334:
                print(info)
            if len(info["companies"]) == 0:
                print(bcolors.WARNING+ filename, " Companies Tag Not present" + bcolors.ENDC)
            else:
                print(bcolors.OKGREEN+ "Parsing "+filename +" Success! " + bcolors.ENDC)
        except:
            print(bcolors.FAIL+ "Exception occurred at file ", filename + bcolors.ENDC)
    
    #Converting into JSON
    finalres={
        "Questions": result
    }
    json_string = json.dumps(finalres, default=obj_dict)
    result_file= open("result.json", "w")
    result_file.write(json_string)
    result_file.close()
    print(bcolors.OKGREEN+ "JSON Created Success, check Questions.json" + bcolors.ENDC)
if __name__ == "__main__":
    main()

