# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 11:17:21 2021
@author: FykeJ
"""

import itertools
import geopy

from geopy.geocoders import Nominatim


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

if yes_or_no("Type YES if you would like me to look up your location from your address, or type NO if you want to enter your location manually \n >"):
    geolocator = Nominatim(user_agent="example")
    loc_address=str(input("Location of building site (full or partial address)? \n >"))
    location = geolocator.geocode(loc_address)
    latitude = location.latitude
    longitude = location.longitude  
    print("Your latitude is..." + str(latitude))
    print("Your longitude is..." + str(longitude))
else:
    latitude=float(input("Enter your Latitude (in decimals): "))
    longitude=float(input("Enter your Longitude (in degrees west, in decimals): "))

elev=float(input("How far above sea level is your building (in meters)?"))


#NEXT STEP: UNDERSTAND HISTORICAL CLIMATE HAZZARDS IN REGION
print("NEXT I NEED SOME MORE INFORMATION ABOUT WHAT WEATHER HAZARDS ARE OF MOST CONCERN TO YOU\n")
print("I'LL ASK SOME BASIC QUESTIONS ABOUT YOUR REGION'S HISTORICAL CLIMATE, AND YOU SIMPLY INDICATE YES OR NO!\n")


# Initialize a blank list of weather hazards that the user will grow following a series of y/n questions:
hazard_dict={}

'''
# populate a dictionary-based list of hazards, and for each, a sub-dictionary of resources.
hazard_dict={"river/lake flooding":  {"resource":"National Research Council", "URL":"https://nrc-publications.canada.ca/eng/view/ft/?id=d72127b3-f93b-48fb-ad82-8eb09992b6b8"},
             "sea level rise":       {"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/sea-level/"},
             "extreme rain":         {"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/rx1day/"},
             "extreme heat":         {"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/tx_max/"},
             "extreme snow":         {"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#6.1-snow_loads"},
             "permafrost loss":      {"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#6.3-permafrost"},
             "high winds":           {"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#7.3-wind_pressures"},
             "wildfire":             {"resource":"climatedata.ca",            "URL":"https://climate-scenarios.canada.ca/FWI"},
             "smoke":                {"resource":"Service Desk",              "URL": "https://climate-change.canada.ca/support-desk"},
             "tropical storms":      {"resource":"Service Desk",              "URL": "https://climate-change.canada.ca/support-desk"},
             "erosion":              {"resource":"Service Desk",              "URL": "https://climate-change.canada.ca/support-desk"},
             "other":                {"resource":"Service Desk",              "URL":"https://climate-change.canada.ca/support-desk"}}
'''


#NEW dynamically generate hazard_dict based on user inputs.
if yes_or_no("Is your building in a region prone to severe thunderstorms?"):
    if yes_or_no("Do these storms carry the risk of flooding rains?"):
        hazard_dict["extreme rain"]={"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/rx1day/"}
    if yes_or_no("Do these storms carry the risk of damaging winds?"):
        hazard_dict["high winds"]={"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#7.3-wind_pressures"}
if yes_or_no("Is your building in a region that experiences heat waves?"):
    hazard_dict["extreme heat"]={"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/tx_max/"}
if yes_or_no("Is your building in a region that exerpeinces heavy snowfalls?"):
    hazard_dict["extreme snow"]={"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#6.1-snow_loads"}
if yes_or_no("Is your building adjacent to the ocean?"):
    if yes_or_no("Are you concerned about sea level rise at this location?"):
        if elev > 50.:
            if yes_or_no("Are you sure? Based on your elevation, it sounds like you may not have to worry about sea level rise.  Is it OK to skip an assessment of sea level rise on your building?") is False:
                hazard_dict["sea level rise"]={"resource":"climatedata.ca",            "URL":"https://climatedata.ca/variable/sea-level/"}
    if yes_or_no("Are you concerned about extra-tropical storms (including Hurricanes) at this location?"):
        hazard_dict["tropical storms"]={"resource":"Service Desk",              "URL": "https://climate-change.canada.ca/support-desk"}
    if yes_or_no("Are you concerned about shoreline erosion at this location?"):
        hazard_dict["erosion"]={"resource":"Service Desk",              "URL": "https://climate-change.canada.ca/support-desk"}
if yes_or_no("Is your building within, or surrounded by, forested area?"):
    if yes_or_no("Are you concerned about wildfire at this location?"):
        hazard_dict["wildfire"]={"resource":"climatedata.ca",            "URL":"https://climate-scenarios.canada.ca/FWI"}
    if yes_or_no("What about smoke from nearby wildfires?"):
        hazard_dict["smoke"]={"resource":"Service Desk",              "URL": "https://climate-change.canada.ca/support-desk"}
if latitude < 60.:
    if yes_or_no("Based on your latitude, it sounds like you may not have to worry about permafrost loss.  Is it OK to skip an assessment of permafrost loss on your building?") is False:
        hazard_dict["permafrost loss"]={"resource":"CRBCPI report",             "URL":"https://climate-scenarios.canada.ca/?page=buildings-report#6.3-permafrost"}
if yes_or_no("Is your building within a floodplain? Or adjacent to a lake?"):
        hazard_dict["river/lake flooding"]={"resource":"National Research Council", "URL":"https://nrc-publications.canada.ca/eng/view/ft/?id=d72127b3-f93b-48fb-ad82-8eb09992b6b8"}
    
#and allow for 'other' entries
        
if yes_or_no("Any other weather hazards you want to tell me about before we continue?"):
    hazard_dict[input("->")]={"resource":"Service Desk",              "URL": "https://climate-change.canada.ca/support-desk"}
    
print(hazard_dict)    
'''


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

'''

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

    

    
