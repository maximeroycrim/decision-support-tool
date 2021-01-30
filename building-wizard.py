# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 11:17:21 2021
@author: FykeJ
"""

import itertools

def yes_or_no(question):
    while "Please reply 'y' or 'n'":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

print("I AM A WIZARD THAT WILL GUIDE YOU IN STARTING YOUR BUILDING RISK ASSESSMENT AND ADAPTATION PLANNING PROCESS!\n")
print("IF YOU ARE LUCKY I MAY EVEN FIND SOME GOOD CLIMATE DATA FOR YOU!\n")
print("FOLLOW ALONG WITH ME ON THE EASY STEPS OF THIS MAGICAL JOURNEY!  IT WILL BE FUN!\n")

### PIEVC Step 1: PROJECT DEFINITION ###

building_type=input("What type of building are you designing, building, or operating?\n >")
building_stage=input("What stage of the building process are you in?\n >")

design_life=input("How many years, from today, do you expect your "+building_type+" to last?\n >")
if int(design_life) < 20:
    raise TypeError("Looks like your "+building_type+"'s design life is pretty short!  If this is the case, you may not need to worry about using future climate information!  Stick to good historical observations instead!\n")
        
## Get location
# TODOS
# -replace with town/city name query, which can be converted to latitude/longitude
# -provide either name, or latitude/longitude in some standard format.  Wizard can parse appropriately.
print("Where is your building at?")
latitude=float(input("Latitude (in decimals): "))
longitude=float(input("Longitude (in degrees west, in decimals): "))
elev=float(input("How far above sea level is your building (in meters)?"))

lake_river_proximity=yes_or_no("Is your building even remotely close any rivers or lakes?")

# Prepopulate a dictionary-based list of hazards, and for each, a sub-dictionary of resources.
hazard_dict={"river/lake flooding":  {"resource":"National Research Council", "URL":"https://nrc-publications.canada.ca/eng/view/ft/?id=d72127b3-f93b-48fb-ad82-8eb09992b6b8"},
             "sea level rise":       {"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/sea-level/"},
             "extreme rain":         {"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/rx1day/"},
             "extreme heat":         {"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/tx_max/"},
             "extreme snow":         {"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#6.1-snow_loads"},
             "permafrost loss":      {"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#6.3-permafrost"},
             "high winds":           {"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#7.3-wind_pressures"},
             "wildfire":             {"resource":"climatedata.ca",            "URL":"https://climate-scenarios.canada.ca/FWI"},
             "other":                {"resource":"Service Desk",              "URL":"https://climate-change.canada.ca/support-desk"}}

# Do an initial screen to weed out obviously non-applicable hazards.  This reduces user work later.
if latitude < 60.:
    if yes_or_no("Based on your location, it sounds like you may not have to worry about permafrost loss.  Is it OK to skip an assessment of permafrost loss on your building?") is True:
        hazard_dict.pop("permafrost loss")

if elev > 50.:
    if yes_or_no("Based on your location, it sounds like you may not have to worry about sea level rise.  Is it OK to skip an assessment of sea level rise on your building?") is True:
        hazard_dict.pop("sea level rise")
        
if lake_river_proximity is False:
    if yes_or_no("Based on your location, it sounds like you may not have to worry about river or lake flooding.  Is it OK to skip an assessment of river/lake flooding on your building?") is True:
        hazard_dict.pop("river/lake flooding")

### PIEVC Step 2: DATA GATHERING ###
print("\n")
print("NOW LET'S THINK ABOUT YOUR BUILDING IN MORE DETAIL!\n")

# Initialize a list of building components that the user will grow interactively.
building_component_dict={}

# Prompt the user to define the components of their building.  This list can be as long as needed.
print("What are the key, major components of your building?  Enter as many as you like.  (or Ctrl-C when done)\n")
try:
    while True:
        building_component_dict[input("->")]=[] #make a dictionary key for each listed component, and set value to a blank list
except KeyboardInterrupt:
    pass

#Now prompt the user to consider the weather/climate impacts, on a componentwise basis.
##Provide some standard hazards, and then prompt user to add more if needed
print("\n")
print("NOW LET'S THINK ABOUT CLIMATE WEATHER HAZARDS!\n")
for key in building_component_dict:
    print("Which of the following climate and weather impacts to the ***"+key+"*** of your building keep you up at night now, or might in the future?\n")
    for h in hazard_dict:
        if yes_or_no(h) is True:
            building_component_dict[key].append(h) #append each relevant hazard to the list of hazards for each component
    if 'other' in building_component_dict[key]: #extend list with any custom hazards provided by user.
        print("Looks like you are thinking of other hazards.  What are they?  (Type Ctrl-C when done).")
        try:
            while True:
               building_component_dict[key].append(input("->"))
        except KeyboardInterrupt:
            pass        
        building_component_dict[key].remove('other') #clean up redundant 'other' entry
        
#Collect all hazards into a common, non-repeating list
#TODO: don't do this, rather, present output by component (like Ryan's approach)
infrastructure_hazards=list(set(itertools.chain(*building_component_dict.values())))

risk_tolerance=input("What is your risk tolerance when it comes to future climate change (h=high, m=medium, l=low)? Understanding your risk tolerance helps decide which climate scenario to use. ")
risk_dict={"l":"RCP8.5","m":"RCP4.5","h":"RCP2.6"}

print("GOOD JOB!  BY CONSIDERING POTENTIAL CLIMATE HAZARDS FOR EACH COMPONENT OF YOUR BUILDING, YOU ARE ON YOUR WAY TO A FULL CLIMATE CHANGE RISK ASSESSMENT!\n")
print("LET ME SUMMARIZE YOUR RESULTS, AND POINT YOU TO SOME POTENTIAL SOURCES OF GOOD PAST AND FUTURE CLIMATE INFORMATION THAT IS RELEVANT TO YOUR BUILDING!\n")
print("REFLECTING YOUR RISK TOLERANCE, YOU MAY WANT TO CONSIDER EXPLORING THE "+risk_dict[risk_tolerance]+" CLIMATE SCENARIO WITHIN THE FUTURE CLIMATE INFORMATION!\n")

#TODO: remake this to present things by component, instead of by climate hazard.
#TODO: use lat/lon to, where possible, grab climatedata or other data, and provide a qualitative trend direction statement.

for h in infrastructure_hazards:
    print(" ")
    print("************")
    print("Regarding "+h+": ")    
    if h in hazard_dict:
        print("You might find some good information at "+hazard_dict[h]["resource"]+"...")
        print("Start your exploration here: "+hazard_dict[h]["URL"])
    else:
        print("Hmmm, this variable potentially doesn't have good climate change information yet.")
        print("Why don't you try contacting the Climate Services Support Desk?")
        print(hazard_dict["other"]["URL"]) 
    input("Press any key to continue...")

print("YOU SHOULD EXPLORE THIS INFORMATION")
input("Press any key and I will vanish in a puff of smoke!")

    

    
