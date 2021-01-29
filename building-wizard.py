# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 11:17:21 2021
@author: FykeJ
"""

import itertools

#Define building basics

print("A FIRST KEY PART OF INTEGRATING CLIMATE CHANGE INTO BUILDING DESIGN IS UNDERSTANDING THE BUILDING!")
print("I AM A WIZARD THAT CAN HELP YOU!")

building_type=input("What type of building are you designing, building, or operating?  ")

design_life_end=input("What is the final year of your "+building_type+"'s expected design life?  ")
if int(design_life_end) < 2030:
    print("Looks like your "+building_type+"'s design life is pretty short!  If this is the case, you may not need to worry about using future climate information!  Stick to good historical observations instead!")
else:
    "Odds are like your  "+building_type+" might see a pretty different climate by the time it's done!"
print("Where is your building at?")
latitude=input("Decimal latitude: ")
longitude=input("Decimal longitude: ")

risk_tolerance=input("What is your risk tolerance when it comes to future climate change (h=high, m=medium, l=low)?  Understanding your risk tolerance helps decide which climate scenario to use. ")


hazard_dict={"river flooding":{"source":"National Research Council","address":"https://nrc-publications.canada.ca/eng/view/ft/?id=d72127b3-f93b-48fb-ad82-8eb09992b6b8"},
             "sea level rise":{"source":"climatedata.ca","address":"https://climatedata.ca/variable/sea-level/"},
             "extreme rain":{"source":"climatedata.ca","address":"https://climatedata.ca/variable/rx1day/"},
             "extreme heat":{"source":"climatedata.ca","address":"https://climatedata.ca/variable/tx_max/"},
             "extreme snow":{"source":"CRBCPI report","address":"https://climate-scenarios.canada.ca/?page=buildings-report#6.1-snow_loads"},
             "permafrost":{"source":"CRBCPI report","address":"https://climate-scenarios.canada.ca/?page=buildings-report#6.3-permafrost"},
             "high winds":{"source":"CRBCPI report","address":"https://climate-scenarios.canada.ca/?page=buildings-report#7.3-wind_pressures"},
             "wildfire":{"source":"climatedata.ca","address":"https://climate-scenarios.canada.ca/FWI"},
             "other":{"source":"Service Desk","address":"https://climate-change.canada.ca/support-desk"}}

infrastructure_component_dictionary={}
input_token=[]

print("What are the key components of your building?  Enter as many as you like.  Just type 'done' when done.")

while input_token != 'done':
    input_token=input("component: ")
    infrastructure_component_dictionary[input_token]=[]
infrastructure_component_dictionary.pop('done')

print("Now let's think about weather, climate and geophysical hazards for each component!")
for key in infrastructure_component_dictionary:
    print("Which of the following climate and weather impacts to the "+key+" keep you up at night now, or might in the future (y/n)?")
    for h in hazard_dict:
        if input(h+"? ") == 'y':
            infrastructure_component_dictionary[key].append(h)
    if 'other' in infrastructure_component_dictionary[key]:
        print("Looks like you are thinking of other possible hazards.  What are they?  Type 'done' when done.")
        input_token=[]
        while input_token != 'done':
            input_token=input("possible hazard: ")
            infrastructure_component_dictionary[key].append(input_token)
        infrastructure_component_dictionary[key].remove('other')
        infrastructure_component_dictionary[key].remove('done')
            
infrastructure_hazards=list(set(itertools.chain(*infrastructure_component_dictionary.values())))
print("Good job!  You've identified some key climate hazards for your building in particular, that may change due to climate change.")
print("I've found some great resources for you to explore, to find more information and data on how climate change may impact these hazards.")

for h in infrastructure_hazards:
    print(" ")
    print("************")
    print("Regarding "+h+": ")    
    if h in hazard_dict:
        print("You might find some good information at "+hazard_dict[h]["source"]+"...")
        print("Start your exploration here: "+hazard_dict[h]["address"])
    else:
        print("Hmmm, this variable potentially doesn't have good climate change information yet.")
        print("Why don't you try contacting the Climate Services Support Desk?")
        print(hazard_dict["other"]["address"]) 
    input("Press any key to continue...")
    
risk_dict={"l":"RCP8.5","m":"RCP4.5","h":"RCP2.6"}
print("Sounds like you have a ")

print("All done!  I hope I helped you find good climate data for climate change risk assessment and climate adaptation planning work!")
input("Press any key and I will vanish in a puff of smoke!")

    

    
    
    
