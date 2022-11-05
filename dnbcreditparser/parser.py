import logging
from dateutil import parser
import requests
import json
import logging
import pandas as pd
from datetime import datetime, timedelta
import pandas as pd
import PyPDF2
import re
import copy
logger = logging.getLogger(__name__)

class CreditRating:
    def __init__(self, name, line):
        self.name = name
        self.line = line
        self.ratings = []
        self.alfanum = []

    def add_rating(self, rate):
        rate = rate.replace("-", "")
        rate = rate.strip()
        if rate.isnumeric():
            self.ratings.append(rate)
        elif rate == "na":
            self.ratings.append('0')

    def add_alfa_rating(self, rate):
        rate = rate.replace("-", "")
        rate = rate.strip()
        if len(rate) > 0:
            self.alfanum.append(rate)

    def post_processes_ratings(self):
        temp = []
        i = 0
        while i < len(self.ratings):
            if len(self.ratings[i])>=5:
                temp.append(float(self.ratings[i][:3]))
                temp.append(float(self.ratings[i][3:6]))
                i=i+2
            elif len(self.ratings[i])==4:
                temp.append(float(self.ratings[i][:3]))
                i=i+1
            else:
                temp.append(float(self.ratings[i]))
                i=i+1
        self.ratings = []
        temp2=[]
        i = 0
        greatest=0
        while i < len(temp):
            if i==0:
                temp2.append(temp[i])
                greatest=temp[i]
            else:
                if temp[i]<greatest:
                    temp2.append(greatest)
                else:
                    temp2.append(temp[i])
                    greatest = temp[i]
            i=i+1
        i=len(temp2)-1
        greatest = 10000
        while i>=0:
            if temp2[i]==0:
                self.ratings.insert(0,greatest)
            else:
                self.ratings.insert(0, temp2[i])
                greatest=temp2[i]
            i=i-1


    def processes_ratings(self):
        temp = []
        i = 0
        while i < len(self.ratings):
            if self.ratings[i]=="1" or (len(self.ratings[0]) > 1 and len(
                    self.ratings[i]) == 1):  # If first element is very low rating, do not check for split fields
                newval = self.ratings[i] if i + 1 == len(self.ratings) else self.ratings[i] + self.ratings[i + 1]
                temp.append(newval)
                i = i + 2
            elif i>1 and (len(self.ratings[i])==2 and len(self.ratings[i-1])==3):
                newval = self.ratings[i] if i + 1 == len(self.ratings) else self.ratings[i] + self.ratings[i + 1]
                temp.append(newval)
                i = i + 2
            elif i<(len(self.ratings)-1) and (len(self.ratings[i])==2 and len(self.ratings[i+1])==4):
                firstval=self.ratings[i] + self.ratings[i+1][0]
                secval = self.ratings[i + 1][1:]
                temp.append(firstval)
                temp.append(secval)
                i = i + 2
            else:
                temp.append(self.ratings[i])
                i = i + 1
        self.ratings = []
        for newel in temp:
            if newel.isnumeric():
                self.ratings.append((newel))
    def __str__(self):
        return self.name + " rating=" + str(self.ratings[0:7])

from pathlib import Path


def parse_credit_rating(filepath):
    if isinstance(filepath, str):
        columns = Path(filepath).name.split("_")
    else:
        columns = filepath.name.split("_")
    dt = columns[0]
    dtiso = "20" + dt[0:2] + "-" +dt[2:4] + "-" + dt[4:6]
    try:
        pdfReader = PyPDF2.PdfFileReader(filepath)
    except:
        return None, None
    companies = []
    def parse_page(pagenr):
        pageObj = pdfReader.getPage(pagenr)
        lines = pageObj.extractText().split("\n")
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            try:
                company = re.match("((.*?)( AS| AB| ASA| A/S))+", line).group()
                # print(company)
                ratingcompany = CreditRating(company, line)
                companies.append(ratingcompany)
                ratingline = line[len(company):]  # The rest of the line after name
                columns = ratingline.split('/')
                if len(columns[-1:]) > 0:
                    firstel = columns[-1:][0]  # There should only be one element after  the / character
                    firstel = firstel.replace("-", "")
                    firstel = firstel.strip()  # Get rid of white space
                    ratinglist = firstel.split( " ")
                    for r in ratinglist:
                        ratingcompany.add_rating(r)
                for r in columns[:-1]:
                    ratingcompany.add_alfa_rating(r)
            except:
                pass
            idx = idx + 1

    for i in range(20):
        parse_page(i)

    for c in companies:
        splits = re.split(r'\s+and\s+|,(?!\s*AB|\s*AS)\s*', c.name)
        if len(splits) > 0:
            c.name = splits[0]
            for s in splits[1:]:
                cc = copy.deepcopy(c)
                cc.name = s
                companies.append(cc)
    dicts = []
    for c in companies:
        if len(c.ratings) > 0:
            c.processes_ratings()
            c.processes_ratings()
            c.processes_ratings()
            c.post_processes_ratings()
            # print(c)
        if len(c.ratings) < 8:
            continue
        dicts.append(
            {
                "company": c.name,
                "3M": c.ratings[0],
                "1Y": c.ratings[1],
                "2Y": c.ratings[2],
                "3Y": c.ratings[3],
                "5Y": c.ratings[4],
                "7Y": c.ratings[5],
                "10Y": c.ratings[6],
            }
        )
    df = pd.DataFrame.from_dict(dicts)
    return dtiso, df






