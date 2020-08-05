import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import re
import string




#Reading data and droping the Columns that are not required for this analysis.
pd.options.display.max_columns = None
pd.options.display.max_rows = None
#pd.reset_option("display.max_rows")

reading = pd.read_csv ("DataAnalyst.csv")
selected = reading [['Job Title', 'Salary Estimate', 'Job Description','Rating', 
                      'Company Name', 'Location', 'Size', 'Industry', 'Sector']]

df = pd.DataFrame(selected)
df.columns=["title", "salary", "description", "rating", "company", "location", "size",
                        "industry", "sector"]

# Adding a .txt file with words we don't want to count since they are irrelevant.
stopwords = set(line.strip() for line in open('stopwords.txt'))



    
titleDict = {}
titleList = []
title50 = []

descDict = {}
descList = []
desc50 = []

for i in range(len(df)):
    titleTemp = df["title"][i].translate(str.maketrans('', '', string.punctuation))
    descTemp = df["description"][i].translate(str.maketrans('','', string.punctuation))
    
    titleTemp = titleTemp.lower()
    descTemp = descTemp.lower()
    
    titleWords = titleTemp.split()
    descWords = descTemp.split()

#-----------------TITLE loop---------------------------------------------
    for word in titleWords:
        if word not in stopwords:
            if word not in titleDict:
                titleDict[word] = 1
            else:
                titleDict[word] += 1
#-----------------DESCRIPTION loop--------------------------------------- 
    for word in descWords:
        if word not in stopwords:
            if word not in descDict:
                descDict[word] = 1
            else:
                descDict[word] += 1
                
                
                
#-----------------TITLE prep--------------------------------------------- 
for key, val in list(titleDict.items()):
    titleList.append((val, key))
    
titleList.sort(reverse=True)

for key, val in titleList[:50]:
    title50.append((key, val))


dfTitle = pd.DataFrame(title50, columns = ['Count', 'Word'])
dfTitle["Count"] = dfTitle["Count"].transform(lambda x: np.log(x))
dfTitle.plot.bar(x='Word',y='Count')


#-----------------DESCRIPTION prep-------------------------------------- 
for key, val in list(descDict.items()):
    descList.append((val, key))
    
descList.sort(reverse=True)


for key, val in descList[:51]:
    desc50.append((key, val))


dfDesc = pd.DataFrame(desc50, columns = ['Count', 'Word'])
dfDesc.drop(dfDesc.loc[dfDesc['Word']=="•"].index, inplace=True)
#dfDesc["Count"] = dfDesc["Count"].transform(lambda x: np.log(x))
dfDesc.plot.bar(x='Word',y='Count')







'''************************************************************************
Cleaning the "Salary" column to convert it to int and split it into Minimum Salary
and Maximum Salary and scaling to thousand dollars.'''

df["salaryMin"] = selected.salary.str.extract("\$([?0-9]+)", expand=False)
df["salaryMax"] = selected.salary.str.extract("-\$([?0-9]+)", expand=False)
df = df.drop (["salary"], axis=1)

df["salaryMin"]=df["salaryMin"].apply(pd.to_numeric, errors='coerce')
df["salaryMax"]=df["salaryMax"].apply(pd.to_numeric, errors='coerce')
df = df.convert_dtypes()

for i in range(len(df)):
    df["salaryMax"][i] = df["salaryMax"][i] * 1000
    df["salaryMin"][i] = df["salaryMin"][i] * 1000 

df = df.drop([2149])
df.drop(df.loc[df['size']=="-1"].index, inplace=True)
df.drop(df.loc[df['size']=="Unknown"].index, inplace=True)

