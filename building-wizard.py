# -*- coding: utf-8 -*-
"""
A decision support tool for integrating climate change into building design, maintenance, and renovation.
"""

import json
from geopy.geocoders import Nominatim
from collections import Counter
import webbrowser
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

draw_stuff('wizard_start')

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
construction_date=input("When was your "+building_type+" constructed or retrofitted? Or, if you're still in the desing stage, what's the anticipated year of completion?")
design_life=input("What is your "+building_type+"'s intended design life (inteded service life before an intervention is required (retrofit, modernize, demolish, etc.)?\n >")
if int(design_life) < 20:
    raise TypeError("Looks like your "+building_type+"'s design life is pretty short!  If this is the case, you may not need to worry about using future climate information!  Stick to good historical observations instead!\n")

design_year=int(construction_date) + int(design_life)
decade=10*(round(int(design_year)/10))
if decade > 2070:
    print("NOTE: Just a heads up, I only have climate data that goes until the year 2100. Your building's design life exceeds this time frame. I'll just stick to showing you data from the 30-year period spanning 2071-2100.")
    decade=2070
    
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
print("STEP 2: WEATHER AND CLIMATE HAZARDS")
print("\n")

print("NEXT I NEED SOME MORE INFORMATION ABOUT WHAT WEATHER HAZARDS ARE OF MOST CONCERN TO YOU\n")
print("I'LL PROVIDE SOME STATEMENTS, AND YOU SIMPLY TELL ME IF ANY OF THESE HAZARDS ARE OF CONCERN TO YOU!\n")
draw_stuff("clouds")
print("\n")
input("Press ENTER to continue...")
# %%

# Initialize a blank list of weather hazards that the user will grow following a series of y/n questions:
hazard_dict={}

# Load the master list of climate hazards, from which a subset of user-specific building hazards is built,
with open('master_hazard_database.json', 'r') as j:
    master_hazard_dict = json.loads(j.read())

#Dynamically generate a customized thazard_dict based on user prompts.
hazard_list=["extreme rain","high winds","extreme heat","extreme cold","extreme snow","wildfire","river/lake flooding"]
for key in hazard_list:
    print(clear)
    draw_stuff(key)
    print(key.upper())
    print(master_hazard_dict[key]["impact_statement"])
    if yes_or_no("Is your region prone to severe storms that bring heavy rains?\n"):
        hazard_dict[key]=master_hazard_dict[key] 
    else:
        print ("\n")
        print ("Hmm, okay - so your region does not experience this hazard. But what about in the future?")
        print ("I have some future climate data on "+key.upper()+" for a period that include the "+str(decade)+"'s, your building's estimated end-of-service-life")
        input("Press ENTER and I'll show it to you. After you've had a look, come back here and we'll discuss.")
        if master_hazard_dict[key]["resource"]=="climatedata.ca":
            url="https://climatedata.ca/explore/variable/?coords="+str(latitude)+","+str(longitude)+",12&geo-select=&var="+str(master_hazard_dict[key]["var"])+"&var-group="+str(master_hazard_dict[key]["group"])+"&mora=ann&rcp=rcp85&decade="+str(decade)+"s&sector="
        else:
            #TODO: for at least CRBCPI, find nearest city from NBCC representative locations
            url=master_hazard_dict[key]["URL"]
        webbrowser.open(url,new=2,autoraise=False)
        print ("\n")
        print ("So tell me: what did you see? Are there future values that exceed those observed in the historical period? Are there trends or patterns in the data? Is there a net increase or decrease over time?")
        if yes_or_no("Based on the data you just saw, do you think that "+ key.upper()+ " could still emerge as a hazard in the future? If yes, I'll add this hazard to the list."):
            hazard_dict[key]=master_hazard_dict[key]
   
print(clear)
draw_stuff('sea level rise')    
print ("JUST ONE QUICK QUESTION BEFORE I CONTINUE...")    
if yes_or_no("Is your region near the ocean?\n"): #Jer: not sure we need this hierarchy of questions for SLR.  Kind of redundant..?
    if elev > 50.:
        key="sea level rise"
        print(key.upper())
        print(master_hazard_dict[key]["impact_statement"])
        if yes_or_no("Based on your elevation, even though your region is near the ocean, it sounds like you may not have to worry about sea level rise.  Is it OK to skip an assessment of sea level rise on your building?\n") is False:
            hazard_dict[key]=master_hazard_dict[key]
    else:
        key="sea level rise"
        hazard_dict[key]=master_hazard_dict[key]            

if latitude > 55.: #This threshold was quickly set - should re-evaluate based on CRBCPI or other, Canadian permafrost map.
    draw_stuff('extreme cold')
    key="permafrost loss"
    print(key.upper())
    print(master_hazard_dict[key]["impact_statement"])
    if yes_or_no("Does any permafrost occur in your region?\n"):
        hazard_dict[key]=master_hazard_dict[key]
    print(clear)


# %%
# And allow for 'other' entries
print(clear)
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

# TODO - improve this langauge and approach to describing future uncertainty in terms of risk.

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

# %%
### PIEVC Step 2: DATA GATHERING ###

# TODO: hone initial component list and list-generating language, so that user is guided towards an appropriate level of depth

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
#loop thorugh each haz, from 1-10 how much does it concern you?
print(clear)
print("\n")
print("THIS PART OF THE PROGRAM IS UNDER CONSTRUCTION...")
print("\n")
print("We want to user to reflect on the magnitiude or the severity of these hazards, so that we can later rank which hazards and which components are seemingly most at risk from climate change. Will be most qualitative, and will not be as detailed as a proper risk computation from liklihood and magnitude.")
print("\n")
input("Press ENTER to continue...")    
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

print("SOME PARTING WISDOME BEFORE I LEAVE YOU TO CONTINUE ON YOUR QUEST...")
print("Here are some resources for you to explore, to find information on how the hazards that may matter for your building may change with climate change!")
for h,r in l_sorted:
    print("\nFor "+h+", you may want to check out: " + hazard_dict[h]["resource"] + ":\n" + hazard_dict[h]["URL"])
    #if hazard_dict[h]["resource"]=="climatedata.ca":
        #url="https://climatedata.ca/explore/variable/?coords="+str(latitude)+","+str(longitude)+",12&geo-select=&var="+str(hazard_dict[h]["var"])+"&var-group="+str(hazard_dict[h]["group"])+"&mora=ann&rcp=rcp85&decade="+str(decade)+"s&sector="
        #webbrowser.open(url,new=2,autoraise=False)

#TODO: Improve this closing guidance.
print("\n")
print("You now have some links to climate data that speaks to hazards you think may impact your building!")
print("You can now use this data to better understand how the likelihood and magnitude of these hazards will change.")
print("You, in close collaboration with your building’s operators and stakeholders can develop a feeling for how consequential these changes will be using a risk assessment that compares present-day climate risks to future risks.")
print("Then, if you see climate change increasing your building’s risks beyond a reasonable amount: you can develop adaptation actions that will ensure your building’s resilience!")
print("\n")
draw_stuff('wizard_end')
print ("POOF! ALL DONE")


#%%


    
