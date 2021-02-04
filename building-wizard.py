# -*- coding: utf-8 -*-
"""
A decision support tool for integrating climate change into building design, maintenance, and renovation.
"""

import json
from geopy.geocoders import Nominatim
from collections import Counter

from textart import draw_stuff

#SETUP FUCNTIONS

# Quick function to error-catch non-standard y/n responses
def yes_or_no(question):
    while "Please reply 'y' or 'n'":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply != "":
            if reply[0] == 'y':
                return True
            if reply[0] == 'n':
                return False



#%%
          
#some interesting string that will clear console and return cursor to top left. Don't ask how it works!
clear="\033[H\033[J"

print(clear)
print("HAZZUH!")
print("\n")

draw_stuff('wizard')

print("\n")
print("I AM A WIZARD THAT WILL GUIDE YOU IN STARTING YOUR BUILDING RISK ASSESSMENT AND ADAPTATION PLANNING PROCESS!\n")
print("IF YOU ARE LUCKY I MAY EVEN FIND SOME GOOD CLIMATE DATA FOR YOU!\n")
print("FOLLOW ALONG WITH ME ON THE EASY STEPS OF THIS MAGICAL JOURNEY!  IT WILL BE FUN!\n")
print("\n")
input("Press Enter to continue...")

### PIEVC Step 1: PROJECT DEFINITION ###
print(clear)
print("\n")
print("STEP 1: BASIC PROJECT DEFINITION")
print("\n")
draw_stuff('house')
print("\n")

building_type=input("What type of building are you designing, building, or operating?\n >")
building_stage=input("What stage of the building process are you in? (design stage, construction stage, retrofit, etc.) \n >")

design_life=input("What is your "+building_type+"'s intended design life (inteded service life before an intervention is required (retrofit, modernize, demolish, etc.)?\n >")
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
print(clear)
print("\n")
print("STEP 2: HISTORICAL AND FUTURE WEATHER AND CLIMATE HAZARDS")
print("\n")

print("NEXT I NEED SOME MORE INFORMATION ABOUT WHAT WEATHER HAZARDS ARE OF MOST CONCERN TO YOU\n")
print("I'LL PROVIDE SOME STATEMENTS ABOUT HOW CLIMATE CHANGE MAY IMPACT THE WEATHER IN YOUR REGION, AND YOU SIMPLY TELL ME IF ANY OF THESE HAZARDS ARE OF CONCERN TO YOU!\n")

# %%

# Initialize a blank list of weather hazards that the user will grow following a series of y/n questions:
hazard_dict={}

# Load the master list of climate hazards, from which a subset of user-specific building hazards is built,
with open('master_hazard_database.json', 'r') as j:
    master_hazard_dict = json.loads(j.read())

#Dynamically generate a customized thazard_dict based on user prompts.
draw_stuff('rain')
key="extreme rain"
print(key.upper())
print(master_hazard_dict[key]["impact_statement"])
print(master_hazard_dict[key]["direction_statement"])
if yes_or_no("Is your region prone to severe storms that bring heavy rains, either NOW or IN THE FUTURE BASED ON THE ABOVE STATEMENT?\n"):
    hazard_dict[key]=master_hazard_dict[key] 
print(clear)
draw_stuff('tornado')
key="high winds"
print(key.upper())
print(master_hazard_dict[key]["impact_statement"])
print(master_hazard_dict[key]["direction_statement"])
if yes_or_no("Is your region prone to heavy winds, either NOW or IN THE FUTURE BASED ON THE ABOVE STATEMENT?\n"):
    hazard_dict[key]=master_hazard_dict[key]
print(clear)
draw_stuff('sun')   
key="extreme heat"
print(key.upper())
print(master_hazard_dict[key]["impact_statement"])
print(master_hazard_dict[key]["direction_statement"])    
if yes_or_no("Is your region prone to prolonged and dangerous heat wave, either NOW or IN THE FUTURE BASED ON THE ABOVE STATEMENT?\n"):
    hazard_dict[key]=master_hazard_dict[key]
print(clear)

draw_stuff('north')    
key="extreme cold"
print(key.upper())
print(master_hazard_dict[key]["impact_statement"])
print(master_hazard_dict[key]["direction_statement"])    
if yes_or_no("Is your region prone to prolonged and dangerous cold snaps, either NOW or IN THE FUTURE BASED ON THE ABOVE STATEMENT?\n"):
    hazard_dict[key]=master_hazard_dict[key]   
print(clear)
draw_stuff('snowfall')    
key="extreme snow"
print(key.upper())
print(master_hazard_dict[key]["impact_statement"])
print(master_hazard_dict[key]["direction_statement"])    
if yes_or_no("Is your region prone to heavy, damaging, snow storms or snow accumulation, either NOW or IN THE FUTURE BASED ON THE ABOVE STATEMENT?\n"):
    hazard_dict[key]=master_hazard_dict[key]
print(clear)
draw_stuff('sea')    
print ("JUST ONE QUICK QUESTION BEFORE I CONTINUE...")    
if yes_or_no("Is your region near the ocean?\n"): #Jer: not sure we need this hierarchy of questions for SLR.  Kind of redundant..?
    if elev > 50.:
        key="sea level rise"
        print(key.upper())
        print(master_hazard_dict[key]["impact_statement"])
        print(master_hazard_dict[key]["direction_statement"])
        if yes_or_no("Based on your elevation, even though your region is near the ocean, it sounds like you may not have to worry about sea level rise.  Is it OK to skip an assessment of sea level rise on your building?\n") is False:
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
print(clear)

draw_stuff('lightning')
key="wildfire"
print(key.upper())
print(master_hazard_dict[key]["impact_statement"])
print(master_hazard_dict[key]["direction_statement"])
if yes_or_no("Is your region prone to wildfires or smoke from wildfires, either NOW or IN THE FUTURE BASED ON THE ABOVE STATEMENT?\n"):
        hazard_dict[key]=master_hazard_dict[key]
print(clear)

if latitude > 55.: #This threshold was quickly set - should re-evaluate based on CRBCPI or other, Canadian permafrost map.
    draw_stuff('north')
    key="permafrost loss"
    print(key.upper())
    print(master_hazard_dict[key]["impact_statement"])
    print(master_hazard_dict[key]["direction_statement"])
    if yes_or_no("Does any permafrost occur in your region?\n"):
        hazard_dict[key]=master_hazard_dict[key]
    print(clear)
#else:
#   if yes_or_no("Based on your latitude, it sounds like you may not have to worry about permafrost loss.  Is it OK to skip an assessment of sea level rise on your building?\n") is False:
#        print("OK, let's keep permafrost in the mix.")
#        key="permafrost loss"
#        hazard_dict[key]=master_hazard_dict[key]

draw_stuff('rain')
key="river/lake flooding"
print(key.upper())
print(master_hazard_dict[key]["impact_statement"])
print(master_hazard_dict[key]["direction_statement"])
if yes_or_no("Is your region lowlying, and susceptible to river or lake flooding either NOW or IN THE FUTURE BASED ON THE ABOVE STATEMENT?\n"):
    hazard_dict[key]=master_hazard_dict[key]
print(clear)

# %%
# And allow for 'other' entries
token=[]
if yes_or_no("Any other weather hazards you want to tell me about before we continue?\n"):
    print("Please enter these hazards below (or type 'done' if you are done)")
    while True:
        token=input("->")
        if token != "done":
            hazard_dict.update({token:master_hazard_dict["other"]})  #Get user-inputted hazard and assign default 'other' hazard information to new, user-defined hazard.
        else:
            break
           

# %%
# GAUGE USER'S RISK TOLERANCE

print(clear)
print("\n")
print("STEP 3: RISK TOLERANCE AND CAPACITY ANALYSIS - **UNDER CONSTRUCTION**")
print("\n")

print ("\n")
print ("BEFORE WE CONTINUE, IT'S IMPORTANT THAT WE HAVE 'THE TALK'. YOU KNOW WHAT I MEAN. LET'S TALK ABOUT THE BIG ELEPHANT IN THE ROOM: UNCERTAINTY.")
print ("\n")
print ("UNLIKE HISTORICAL CLIMATE NORMALS, FUTURE CLIMATE CONDITIONS CAN'T BE BOILED DOWN TO A SINGLE NUMBER.")
print ("IN FACT, THE FUTURE IS FAR FROM CERTAIN. THE AMOUNT OF FUTURE CLIMATE CHANGE ONE NEEDS TO PLAN FOR DEPENDS LARGELY ON FUTURE GREENHOUSE EMISSIONS.")
print ("\n")
print ("YOU COULD ALWAYS 'PLAN FOR THE WORST AND HOPE FOR THE BEST,' BUT IT ISN'T ALWAYS FINANCIALLY POSSIBLE TO PLAN FOR ALL POSSIBLE FUTURE HAZARDS.")
print ("\n")
print ("I WANT TO GUAGE YOUR TOLERANCE FOR FUTURE CLIMATE UNCERTAINY BY ASKING A FEW SIMPLE QUESTIONS : ")
print ("\n")
print ("How would you rate your risk tolerance? This is the maximum amount of uncertainty you are willing to take on and still be able to sleep at night")
financial_tolerance=input("answer: l=low tolerance; m=medium tolerance; h=high tolerance \n >")

print ("How would you rate your risk capcity? This is the amount of risk you must take on in order to achieve your goals.")
financial_capacity=input("answer: l=low capacity; m=medium capacity; h=high capacity \n >")

print ("How would your rate your building's adaptive capacity? In other words, this is how much additional capacity the current design has to withstand an increase in climate risks.")
adaptive_capacity=input("answer: l=low capacity; m=medium capacity; h=high capacity \n >")

print ("Finally, what is your health and safety risk tolerance? This is the likihood that exposure to a hazard could result in harm or other adverse health impacts.")
health_tolerance=input("answer: l=low tolerance; m=medium tolerance; h=high tolerance \n >")

#risk_tolerance=input("What is your risk tolerance when it comes to future climate change (h=high, m=medium, l=low)? Understanding your risk tolerance helps decide which climate scenario to use. ")
#risk_dict={"l":"RCP8.5","m":"RCP4.5","h":"RCP2.6"}

# TODO: provide an interim summary of climate trends?

# %%
### PIEVC Step 2: DATA GATHERING ###
print(clear)
print("\n")
print("STEP 4: INVENTORY OF BUILDING SYSTEMS AND COMPONENTS")
print("\n")
print("LET'S DESCRIBE YOUR BUILDING IN MORE DETAIL!\n")
print("I NEED YOU TO GENERATE A LIST OF BUILDING COMPONENTS. I'LL GET YOU STARTED, THEN FEEL FREE TO ADD IN AS MANY AS YOU LIKE ;)")

# Initialize a list of building components that the user will grow interactively.
# This list will store component-specific hazards.
building_component_dict={}

# Load the master list of building components, from which a subset of user-specific building hazards is built,
with open('master_building_component_database.json', 'r') as j:
    master_building_component_dict = json.loads(j.read())

for c in master_building_component_dict:
    if yes_or_no("Does your builidng have " + master_building_component_dict[c]["sentence_start"] + " " + c + "?"):
        building_component_dict[c]=master_building_component_dict[c]

# Prompt the user to define the components of their building.  This list can be as long as needed.
print("What are other key, major structural or system components of your building and property?  Enter as many as you like.  (type 'done' when done)\n")

while True:
    token=input("->")
    if token != "done":
        building_component_dict[token]=[]  #Get user-inputted hazard and assign default 'other' hazard information to new, user-defined hazard.
    else:
        break 
#%%

#Now prompt the user to consider the weather/climate impacts, on a componentwise basis.
##Provide some standard hazards, and then prompt user to add more if needed
print(clear)
print("\n")
print("STEP 5: WEATHER AND CLIMATE IMPACTS ON BUILDING SYSTEMS AND COMPONENTS")
print("\n")

print("Now, let's review the climate hazards you identified, in the context of your building's components!\n")
for component in building_component_dict:
    haz=[]
    for h in hazard_dict:
        print("Let's consider "+h.upper()+", in the context of your building's "+component.upper()+".")
        print(hazard_dict[h]["impact_statement"]+"  "+hazard_dict[h]["direction_statement"]+"  Reflecting on this, might you be concerned that "+h+" could impact your "+component.upper()+" now, or could emerge as a potential impactor to your "+component.upper()+", in the future?")
        if yes_or_no("") is True:
            haz.append(h) #append each relevant hazard to the list of hazards for each component
    if 'other' in building_component_dict[component]: #extend list with any custom hazards provided by user.
        print("Looks like you are thinking of other hazards.  What are they?  (type 'done' when done).")
        while True:
            token=input("->")
            if token != "done":
                haz.append(token)  #Get user-inputted hazard and assign default 'other' hazard information to new, user-defined hazard.
        else:
            break   
        building_component_dict[component].remove('other') #clean up redundant 'other' entry
    print(clear)    
    building_component_dict[component]=haz
    
#TODO: make logic to reorder list by priority
#%% 

print(clear)
print("\n")
print("STEP 6: SUMMARY REPORT AND YOUR NEXT STEPS")
print("\n")

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

input("Press ENTER to continue...")

print(clear)

print("Based on these lists, it looks like the building components that may be most vulnerable to climate change are:\n"+sep+sep.join(most_vulnerable_components))
print("\nIt might make sense to focus most on these components during your climate change risk assessment.")
print("Conversely, your least vulnerable building components look to to be:\n"+sep+sep.join(least_vulnerable_components)+"\n")

# Rank hazards by # of times they are mentioned as component hazards.  Display top hazards.
hazard_list=sum(building_component_dict.values(), [])
l_sorted=Counter(hazard_list).most_common()
max_len=min(3,len(l_sorted))
print("Based on these lists, the top climate hazards for your building appear to be:\n")
for h in range(max_len):
    print("->"+l_sorted[h][0])
print("\nIt might make sense to focus most on these hazards during your climate change risk assessment climate data gathering.\n")

print ("Press ENTER to continue")
print (clear)

print("JUST ONE MORE PARTING BIT OF WISDOME BEFORE YOU CONTINUE YOUR QUEST...")
print("Here are some resources for you to explore, to find information on how the hazards that may matter for your building may change with climate change!")
for h,r in l_sorted:
    print("\nFor "+h+", you may want to check out: " + hazard_dict[h]["resource"] + ":\n" + hazard_dict[h]["URL"])

draw_stuff('wizard')
print ("POOF! ALL DONE")


#%%


    
