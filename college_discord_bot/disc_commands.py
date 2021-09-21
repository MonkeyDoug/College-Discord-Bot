#!/usr/bin/env python3

import requests
import re
import string
from bs4 import BeautifulSoup

args = []
# For Testing
# link = 'https://www.collegedata.com/college-search/university-of-pennsylvania'

def scraping(link,args):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html5lib')
    container = soup.find('script', attrs = {'id':'__NEXT_DATA__'})
    match = re.search(r'\{.*\}',container.prettify())
    main = match.group()

    try:
        first_aggr =  '>>> ' + descriptions(main) + '\n' + averages(main) + '\n' + early(main) + '\n' + rate(main) + '\n' + COA(main) + '\n' + mascot(main)
    except AttributeError:
        return 'Please type the full name of the college/university.'

    r = requests.get(link + '/academics')
    soup = BeautifulSoup(r.content, 'html5lib')
    container = soup.find('script', attrs = {'id':'__NEXT_DATA__'})
    match = re.search(r'\{.*\}',container.prettify())
    main = match.group()

    second_aggr = '\n' + most_popular(main) + '\n' + special_programs(main)

    final = first_aggr + second_aggr + '\n**For More Information visit:** ' + link
    return final

def descriptions(text):
    descriptions = re.search(r',"description":".*?\",',text).group()
    descriptions = descriptions[16:-2]

    descriptions = '__**Descriptions:**__ ' + descriptions

    return descriptions

def rate(text):
    admission_rate = re.search(r'Overall Admission Rate.*?\["(.*?)"\]',text).group(1)

    admission_rate = '__**Admission Rate:**__ ' + admission_rate

    return admission_rate

def early(text):
    early = re.findall(r'Early.*?\["(.*?)"\]',text)
    early_action = early[0] + ' '
    early_decision = early[1]

    early = '__**Early Action:**__ ' + early_action + '__**Early Decision:**__ ' + early_decision

    return early

def averages(text):
    GPA = re.search(r'GPA.*?\["(.*?)"\]',text).group(1)
    GPA = '__**GPA:**__ ' + GPA + ' '

    SAT_MATH = re.search(r'SAT Math.*?\["(.*?)"\]',text).group(1).replace('"','').replace(',','/')
    SAT_MATH = '__**SAT Math:**__ ' + SAT_MATH + ' '

    SAT_EBRW = re.search(r'SAT EBRW.*?\["(.*?)"\]',text).group(1).replace('"','').replace(',','/')
    SAT_EBRW = '__**SAT EBRW:**__ ' + SAT_EBRW + ' '

    ACT = re.search(r'ACT.*?\["(.*?)"\]',text).group(1).replace('"','').replace(',','/')
    ACT = '__**ACT:**__ ' + ACT

    averages = GPA + SAT_MATH + SAT_EBRW + ACT

    return averages

def COA(text):
    cost = re.search(r'\$\d+,\d+',text).group()

    cost = '__**Cost of Attendance:**__ ' + cost

    return cost

def mascot(text):
    mascot = re.search(r'Mascot.*?\["(.*?)"\]',text).group(1)

    mascot = "__**Mascot:**__ " + mascot
    return mascot

def most_popular(text):
    programs = re.search(r'Most Popular.*?\["(.*?)"\]',text).group(1).replace('"','')

    programs = '__**Most Popular Disciplines:**__ ' + programs
    return programs

def special_programs(text):
    programs = re.search(r'Special Programs.*?\["(.*?)"\]',text).group(1).replace('"','')

    programs = '__**Special Programs:**__ ' + programs
    return programs
