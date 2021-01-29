# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 11:17:21 2021
@author: FykeJ
"""

import itertools

#Define building basics

print("A FIRST KEY PART OF INTEGRATING CLIMATE CHANGE INTO BUILDING DESIGN IS UNDERSTANDING THE BUILDING!")
print("I AM A WIZARD THAT CAN HELP YOU!")

### PIEVC Step 1: PROJECT DEFINITION ###

building_type=input("What type of building are you designing, building, or operating?  ")
design_life_end=input("What is the final year of your "+building_type+"'s expected design life?  ")
if int(design_life_end) < 2030:
    print("Looks like your "+building_type+"'s design life is pretty short!  If this is the case, you may not need to worry about using future climate information!  Stick to good historical observations instead!")
else:
    "Odds are like your  "+building_type+" might see a pretty different climate by the time it's done!"

##Get location
#Ideas:
#-replace with town name, which can be converted to latitude/longitude
#-provide either name, or latitude/longitude in some standard format.  Wizard can parse appropriately.
print("Where is your building at?")
latitude=input("Decimal latitude: ")
longitude=input("Decimal longitude: ")

#Prepopulate a dictionary-based list of hazards, and for each, a sub-dictionary of resources.
hazard_dict={"river flooding":{"resource":"National Research Council", "URL":"https://nrc-publications.canada.ca/eng/view/ft/?id=d72127b3-f93b-48fb-ad82-8eb09992b6b8"},
             "sea level rise":{"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/sea-level/"},
             "extreme rain":  {"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/rx1day/"},
             "extreme heat":  {"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/tx_max/"},
             "extreme snow":  {"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#6.1-snow_loads"},
             "permafrost":    {"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#6.3-permafrost"},
             "high winds":    {"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#7.3-wind_pressures"},
             "wildfire":      {"resource":"climatedata.ca",            "URL":"https://climate-scenarios.canada.ca/FWI"},
             "other":         {"resource":"Service Desk",              "URL":"https://climate-change.canada.ca/support-desk"}}

### PIEVC Step 2: DATA GATHERING ###

#Initialize some lists that the user will grow interactively.
infrastructure_component_dictionary={}

#Prompt the user to define the components of their building.  This list can be as long as needed.
print("What are the key components of your building?  Enter as many as you like.  Just type 'done' when done.")
while input_token != 'done':
    input_token=input("component: ")
    infrastructure_component_dictionary[input("component: ")]=[] #make a dictionary key for each listed component, and set value to a blank list
infrastructure_component_dictionary.pop('done') #clean up

#Now prompt the user to consider the weather/climate impacts, on a componentwise basis.
##Provide some standard hazards, and then prompt user to add more if needed
print("Now let's think about weather, climate and geophysical hazards for each component!")
for key in infrastructure_component_dictionary:
    print("Which of the following climate and weather impacts to the "+key+" keep you up at night now, or might in the future (y/n)?")
    for h in hazard_dict:
        if input(h+"? ") == 'y':
            infrastructure_component_dictionary[key].append(h) #append each relevant hazard to the list of hazards for each component
    if 'other' in infrastructure_component_dictionary[key]: #extend list with any custom hazards provided by user.
        print("Looks like you are thinking of other possible hazards.  What are they?  Type 'done' when done.")
        input_token=[]
        while input_token != 'done':
            input_token=input("possible hazard: ")
            infrastructure_component_dictionary[key].append(input_token)
        infrastructure_component_dictionary[key].remove('other') #clean up 
        infrastructure_component_dictionary[key].remove('done') #clean up
            
infrastructure_hazards=list(set(itertools.chain(*infrastructure_component_dictionary.values())))
print("Good job!  You've identified some key climate hazards for your building in particular, that may change due to climate change.")
print("I've found some great resources for you to explore, to find more information and data on how climate change may impact these hazards.")

for h in infrastructure_hazards:
    print(" ")
    print("************")
    print("Regarding "+h+": ")    
    if h in hazard_dict:
        print("You might find some good information at "+hazard_dict[h]["resource"]+"...")
        print("Start your exploration here: "+hazard_dict[h]["address"])
    else:
        print("Hmmm, this variable potentially doesn't have good climate change information yet.")
        print("Why don't you try contacting the Climate Services Support Desk?")
        print(hazard_dict["other"]["address"]) 
    input("Press any key to continue...")

risk_tolerance=input("What is your risk tolerance when it comes to future climate change (h=high, m=medium, l=low)? Understanding your risk tolerance helps decide which climate scenario to use. ")
risk_dict={"l":"RCP8.5","m":"RCP4.5","h":"RCP2.6"}

print("All done!  I hope I helped you find good climate data for climate change risk assessment and climate adaptation planning work!")
input("Press any key and I will vanish in a puff of smoke!")

    

    
