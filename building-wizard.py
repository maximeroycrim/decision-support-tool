# -*- coding: utf-8 -*-
"""
A decision support tool for integrating climate change into building design, maintenance, and renovation.
"""

import json

from geopy.geocoders import Nominatim

from collections import Counter

# Load the master list of climate hazards, from which a subset of user-specific building hazards is built,
with open('master_hazard_database.json', 'r') as j:
    master_hazard_dict = json.loads(j.read())

# Quick function to error-catch non-standard y/n responses
def yes_or_no(question):
    while "Please reply 'y' or 'n'":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply != "":
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

if yes_or_no("Type YES if you would like me to look up your location from your address, or type NO if you want to enter your location manually \n >"):
    geolocator = Nominatim(user_agent="example")
    loc_address=str(input("Location of building site (full or partial address)? \n >"))
    location = geolocator.geocode(loc_address)
    latitude = location.latitude
    longitude = location.longitude  
    print("Your latitude is..." + str(latitude))
    print("Your longitude is..." + str(longitude))
else:
    latitude=float(input("Enter your Latitude (in decimals): \n >"))
    longitude=float(input("Enter your Longitude (in degrees west, in decimals): \n >"))

elev=float(input("How far above sea level is your building (in meters)? \n >"))

#NEXT STEP: UNDERSTAND HISTORICAL CLIMATE HAZZARDS IN REGION
print("NEXT I NEED SOME MORE INFORMATION ABOUT WHAT WEATHER HAZARDS ARE OF MOST CONCERN TO YOU\n")
print("I'LL ASK SOME BASIC QUESTIONS ABOUT YOUR REGION'S HISTORICAL CLIMATE, AND YOU SIMPLY INDICATE YES OR NO!\n")

# %%

# Initialize a blank list of weather hazards that the user will grow following a series of y/n questions:
hazard_dict={}

#Dynamically generate a customized thazard_dict based on user prompts.
if yes_or_no("Is your building in a region prone to severe storms that bring heavy rains?\n"):
    if yes_or_no("Do these storms ever bring flooding rains (so-called 'pluvial' or 'overland' flooding)?\n"):
    #if yes_or_no("Do these storms ever bring flooding rains (so-called 'pluvial' or 'overland' flooding)?\n"):
    #    key="extreme rain"
    #    hazard_dict[key]=master_hazard_dict[key]  #TODO: add infiltration,..
if yes_or_no("Does your region experience heavy winds?\n"):
    key="high winds"
    hazard_dict[key]=master_hazard_dict[key]
if yes_or_no("Is your building in a region that experiences prolonged and dangerous heat waves?\n"):
    key="extreme heat"
    hazard_dict[key]=master_hazard_dict[key]
if yes_or_no("Is your building in a region that experiences heavy, damaging, snowfalls?\n"):
    key="extreme snow"
    hazard_dict[key]=master_hazard_dict[key]
if yes_or_no("Is your building near the ocean?\n"): #Jer: not sure we need this hierarchy of questions for SLR.  Kind of redundant..?
    if yes_or_no("Are you concerned about sea level rise at this location?\n"):
        if elev > 50.:
            if yes_or_no("Based on your elevation, it sounds like you may not have to worry about sea level rise.  Is it OK to skip an assessment of sea level rise on your building?\n") is False:
                key="sea level rise"
                hazard_dict[key]=master_hazard_dict[key]
        else:
            key="sea level rise"
            hazard_dict[key]=master_hazard_dict[key]            
#    if yes_or_no("Are you concerned about extra-tropical storms (including Hurricanes) at this location?\n"): #The actual hazards from these storms is wind, rain, and coastal flooding.  Since we cover these already, not sure we need to include a specific storm category here...?
#        key="tropical storms"
#        hazard_dict[key]=master_hazard_dict[key]
#    if yes_or_no("Are you concerned about marine coastal erosion at this location?\n"): #Shoreline erosion is an impact that is caused by wind/wave hazard.  So, not sure we need to add it to list of hazards.  Also, should be clear on erosion in marine, and also river/lake perspectives
#        key="erosion"
#        hazard_dict[key]=master_hazard_dict[key]
if yes_or_no("Is your region prone to wildfires or smoke from nearby wildfires?\n"):
        key="wildfire"
        hazard_dict[key]=master_hazard_dict[key]
if latitude > 60.: #This threshold was quickly set - should re-evaluate based on CRBCPI or other, Canadian permafrost map.
    if yes_or_no("Does any permafrost occur in your region?\n"):
        key="permafrost loss"
        hazard_dict[key]=master_hazard_dict[key]
else:
   if yes_or_no("Based on your latitude, it sounds like you may not have to worry about permafrost loss.  Does this sound right?\n") is False:
        print("OK, let's keep permafrost in the mix.")
        key="permafrost loss"
        hazard_dict[key]=master_hazard_dict[key]
if yes_or_no("Is your regions lowlying, and susceptible to river or lake flooding?\n"):
        key="river/lake flooding"
        hazard_dict[key]=master_hazard_dict[key]

# %%
# And allow for 'other' entries

if yes_or_no("Any other weather hazards you want to tell me about before we continue?\n"):
    print("Please enter these hazards below (or Ctrl-C when done)")  #replace Ctrl-C with a 'done'
    try:
        while True:
            val=input("->")
            if val=='done': # see above
                break
            hazard_dict.update({input("->"):master_hazard_dict["other"]})  #Get user-inputted hazard and assign default 'other' hazard information to new, user-defined hazard.
    except KeyboardInterrupt:
        pass            

# %%

#risk_tolerance=input("What is your risk tolerance when it comes to future climate change (h=high, m=medium, l=low)? Understanding your risk tolerance helps decide which climate scenario to use. ")
#risk_dict={"l":"RCP8.5","m":"RCP4.5","h":"RCP2.6"}

### PIEVC Step 2: DATA GATHERING ###
print("\n")
print("NOW LET'S THINK ABOUT YOUR BUILDING IN MORE DETAIL!\n")

# Initialize a list of building components that the user will grow interactively.
# This list will store component-specific hazards.
building_component_dict={}

# Prompt the user to define the components of their building.  This list can be as long as needed.
print("What are the key, major components of your building?  Enter as many as you like.  (or Ctrl-C when done)\n") #TODO: make pre-populated components and systems list
try:
    while True:
        building_component_dict[input("->")]=[] #make a dictionary key for each listed component, and set value to a blank list.  This list will grow in next loop.
except KeyboardInterrupt:
    pass

#%%

#Now prompt the user to consider the weather/climate impacts, on a componentwise basis.
##Provide some standard hazards, and then prompt user to add more if needed
print("\n")
print("NOW LET'S THINK AGAIN ABOUT CLIMATE WEATHER HAZARDS!\n")
for component in building_component_dict:
    print("Which of the following climate and weather impacts to the ***"+component+"*** of your building keep you up at night now, or might in the future?\n")
    for h in hazard_dict:
        if yes_or_no(h) is True:
            building_component_dict[component].append(h) #append each relevant hazard to the list of hazards for each component
    if 'other' in building_component_dict[component]: #extend list with any custom hazards provided by user.
        print("Looks like you are thinking of other hazards.  What are they?  (Type Ctrl-C when done).")
        try:
            while True:
               building_component_dict[component].append(input("->"))
        except KeyboardInterrupt:
            pass        
        building_component_dict[component].remove('other') #clean up redundant 'other' entry
#TODO: make logic to reorder list by priority
#%% 

print("GOOD JOB!  IN CONSIDERING POTENTIAL CLIMATE HAZARDS FOR EACH COMPONENT OF YOUR BUILDING, YOU HAVE STARTED ON YOUR WAY TO A FULL CLIMATE CHANGE RISK ASSESSMENT!\n")
print("LET ME SUMMARIZE YOUR RESULTS, AND TRY TO POINT YOU TO SOME POTENTIAL SOURCES OF GOOD PAST AND FUTURE CLIMATE INFORMATION THAT IS RELEVANT TO YOUR BUILDING!\n")

sep="\n->"
# Summarize hazards by component
for component in building_component_dict:
    print("Let's consider the "+component+" of your building.")
    print("It sounds like your building's "+component+" could be vulnerable to climate change-caused shifts to:\n"+sep+sep.join(building_component_dict[component]))
    print(" ")

# Find component(s) with most/least vulnerabilities.  Code deals with ties.
mx = max(len(x) for x in iter(building_component_dict.values()))
mn = min(len(x) for x in iter(building_component_dict.values()))
most_vulnerable_components=[k for k, v in iter(building_component_dict.items()) if len(v)==mx]
least_vulnerable_components=[k for k, v in iter(building_component_dict.items()) if len(v)==mn]


print("Based on these lists, it looks like your most vulnerable building components may be:\n"+sep+sep.join(most_vulnerable_components))
print("\nIt might make sense to focus most on this component during your climate change risk assessment.")
print("Conversely, your least vulnerable building components look to me to be:\n"+sep+sep.join(least_vulnerable_components)+"\n")

# Rank hazards by # of times they are mentioned as component hazards.  Display top hazards.
hazard_list=sum(building_component_dict.values(), [])
l_sorted=Counter(hazard_list).most_common()
max_len=min(3,len(l_sorted))
print("Based on these lists, the top climate hazards for your building appear to be:\n")
for h in range(max_len):
    print("->"+l_sorted[h][0])
print("\nIt might make sense to focus most on these hazards during your climate change risk assessment climate data gathering.")

print("Your next steps:")


    
