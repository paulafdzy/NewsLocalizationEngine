import numpy as np
import sys
import pandas as pd
from jinja2 import Template
import json
import scipy.stats as ss
from scipy.stats import percentileofscore
import math

#open metadata and get all the parameters
with open('metadata.json') as json_file:
    data = json.load(json_file)
    dataset = data['Data-Path']
    year = data['Year']
    subject = data['Subject']
    source = data['Source']
    given_title = data['Title']

#get data from spreadsheet
finaldata = pd.read_csv(dataset)

#sort into columns
fips_code = finaldata['FIPS'].tolist()
county = finaldata['COUNTY'].tolist()
lst= finaldata[subject].tolist()
state = finaldata['STATE'].tolist()

county_number = []
for item in lst:
    if item == "Na" or item == "na":
        county_number.append(None)
    else:
        county_number.append(float(item))

def localized_Text(fips):
    f = int(fips)
    i = fips_code.index(f)

    slst = []
    state_total = 0
    num_counties = 0
    this_state= state[i]

    for c in range(0, len(fips_code)):
        if state[c] == this_state:
            if county_number[i] == None:
                pass
            else:
                state_total = state_total + float(county_number[c])
                if float(county_number[c]) > 0:
                    num_counties = num_counties + 1
                    slst.append(float(county_number[c]))
                    if c == i:
                        index = len(slst)-1

    state_average = int(state_total/ num_counties)
    ranks = []
    #print(slst)
    ranks.append(ss.rankdata(slst))
    if county_number[i] == None:
        generated_text = "No text available for your county."
        generated_title = "Not Available"
    else:
        rank = ranks[0][index]
        percentile = percentileofscore(county_number, float(county_number[i]))
        percentile = int(percentile)
        if float(county_number[i]) > state_average:
             highlow = "higher than"
        elif float(county_number[i]) == state_average:
             highlow = "the same as"
        else:
             highlow = "lower than"


        t = Template("The {{y}} {{s}} in {{c}} (which is the closest county in your area that collects such data), was {{cn}}, which is {{hl}} the state average of {{sa}}, according to the {{src}}. Within the state, {{c}} has the {{r}} highest {{s}}, and it is on the {{p}} percentile in the country.")
        ti= Template(given_title)

        generated_text = t.render( y = year, s = subject, c = county[i], cn = county_number[i], hl = highlow, sa = state_average, src = source, r = rank, p = percentile)
        generated_title = ti.render(c = county[i])

#make file and write json obj
    jsonobject = {
    "Text": str(generated_text),
    "Title": str(generated_title),
    "County" : str(county[i])
    }
    textjson = json.dumps(str(jsonobject))
    workfile = str(fips) + ".json"
    f = open(workfile, 'w')
    f.write(textjson)


 #create file for every fips code
for num in fips_code[1000:1010]:
    if math.isnan(num):
        pass
    else:
        c = int(num)
        localized_Text(c)
        print("done")

#localized_Text(fips)
