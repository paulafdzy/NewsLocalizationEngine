import numpy as np
import sys
import pandas as pd
from jinja2 import Template
import json
import scipy.stats as ss
from scipy.stats import percentileofscore

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
county_number= finaldata[subject].tolist()
state = finaldata['STATE'].tolist()
#state average, state


#to calculate with codeeee
state_list =
rank = []
state_average={}
for this_state in state_list:
    slst = []
    state_total = 0
    num_counties = 0
    for i in range(0, len(county)):
        if state[i] == this_state:
            slst.append(county_number[i])
            state_total = state_total + county_number[i]
            num_counties = num_counties + 1
    state_average[this_state] = state_total/ num_counties
    state_rank.append(ss.rankdata(slst))





def localized_Text(fips):

    f = int(fips)
    i = fips_code.index(f)

    t = Template("The {{y}} {{s}} in {{c}}, (which is the closest county in your
     area that collects such data), was {{cn}}, which is {{hl}} the state
     average of {{sa}}, according to {{src}}. Within the state, {{c}} has the {{r}}
     highest {{s}}, and it is on the {{p}} percentile in the country.")

    ti= Template(given_title)
    percentile = percentileofscore(county_number, county_number[i])

#generate templates
    if county_number[i] > state_average:
        highlow = "higher than"
    elif county_number[i] == state_average:
        highlow = "the same as"
    else:
        highlow = "lower than"


    generated_text = t.render( y = year, s = subject, c = county[i],
    cn = county_number[i], hl = highlow, sa = state_average[state[i]],
    src = source, r = rank[i], p = percentile)

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
# for num in fips_code:
#     if math.isnan(num):
#         pass
#     else:
#         c = int(num)
#         localized_Text(c)
#         print("done")

