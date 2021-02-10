# -*- coding: utf-8 -*-
"""
A decision support tool for integrating climate change into building design, maintenance, and renovation.
This python script is intended to demonstrate the underlying logic behind a proposed web-based decision support
tool for the climatedata.ca Building Module.  
"""

import json
from geopy.geocoders import Nominatim
import webbrowser
from textart import draw_stuff
import requests
import numpy as np
from sklearn.neighbors import BallTree, KDTree

import pandas as pd

CRBCPI_data={"dT0p5":pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+0.5C_NBCC.xls"),
             "dT1p0":pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+1.0C_NBCC.xls"),
             "dT1p5":pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+1.5C_NBCC.xls"),
             "dT2p0":pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+2.0C_NBCC.xls"),
             "dT2p5":pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+2.5C_NBCC.xls"),
             "dT3p0":pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+3.0C_NBCC.xls"),
             "dT3p5":pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+3.5C_NBCC.xls")}

#Set up nearest neighbour search on the sphere
lat=np.deg2rad(CRBCPI_data["dT0p5"]["Latitude"].values)
lon=np.deg2rad(CRBCPI_data["dT0p5"]["Longitude"].values)
ball=BallTree(np.vstack((lat,lon)).swapaxes(1,0),metric="haversine")

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
print("I am a decision support tool that will help you begin the process of integrating climate change information into your building!\n")
print("This process should take around 20 minutes to complete.  At the end, I hope you will have some pointers to some relevant climate information.\n")
print("You'll also have a better sense of the workflow for using climate information within climate change risk and adaptation planning!\n")
print("Life is short!  Let's get going!")
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
if yes_or_no("Is this an existing building?\n >"):
    building_stage="existing"
    construction_date=input("When was your "+building_type+" constructed?\n >")
else:
    building_stage=input("OK, so what stage of the building process are you in? (design stage, construction stage, retrofitting, etc.) \n >")
    construction_date=input("And what's the anticipated final year of construction? \n >")
design_life=input("What is your "+building_type+"'s intended design life (intended service life before an intervention is required (retrofit, modernize, demolish, etc.)?\n >")
if int(design_life) < 20:
    raise TypeError("Looks like your "+building_type+"'s design life is pretty short!  If this is the case, you may not need to worry about using future climate information!  Stick to good historical observations instead!\n")
design_year=int(construction_date) + int(design_life)
decade=int(round(design_year,-1))
if decade > 2070:
    if decade > 2100:
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

if not 41. <= latitude <= 84.:
    raise TypeError("Looks like your latitude is outside of Canada.  Can you re-check this?\n")
if not -142. <= longitude <= -.52:
    raise TypeError("Looks like your longitude is outside of Canada.  Can you re-check this?\n")

#find nearest CPI point (use CRBCPI_i to index climate data for this point, from CRBCPI data dictionary)
distances,CRBCPI_i=ball.query(np.deg2rad([[latitude,longitude]]),k=1)

elev=float(input("How far above sea level is your building (in meters)? \n >"))

# %%
### PIEVC Step 2: DATA GATHERING ###

# TODO: hone initial component list and list-generating language, so that user is guided towards an appropriate level of depth

print(clear)
print("\n")
print("STEP 2: INVENTORY OF BUILDING SYSTEMS AND COMPONENTS")
print("\n")
print("Let's describe your building in some more detail!\n")
print("I'll get you started with a few common building elements.  Then you can enter more afterwards.")

# Initialize a list of building components that the user will grow interactively.
# This list will store component-specific hazards.
building_component_dict={}

# Load the master list of building components, from which a subset of user-specific building hazards is built,
with open('master_building_component_database.json', 'r') as j:
    master_building_component_dict = json.loads(j.read())

for c in master_building_component_dict:
    if yes_or_no("Does your building have " + master_building_component_dict[c]["sentence_start"] + " " + c + "?"):
        building_component_dict[c]=master_building_component_dict[c]

# Prompt the user to define the components of their building.  This list can be as long as needed.
print("What are other key, major structural or system components of your building and property?\n")
print("Enter as many as you like and don't forget about your building's surroundings.  (type 'done' when done)\n")

while True:
    token=input("->")
    if token != "done":
        building_component_dict[token]=[]  #Get user-inputted hazard and assign default 'other' hazard information to new, user-defined hazard.
    else:
        break 

#%%

#NEXT STEP: UNDERSTAND HISTORICAL CLIMATE HAZZARDS IN REGION
print(clear)
print("\n")
print("STEP 3: WEATHER HAZARDS AND CLIMATE DATA")
print("\n")

print("NEXT, LET'S DEVELOP SOME INFORMATION ABOUT PRESENT AND POSSIBLE FUTURE WEATHER HAZARDS IN YOUR AREA!\n")
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
    if master_hazard_dict[key]["type"]=="threshold":
        if key=='extreme cold':
            threshold=input("\nWhat temperature threshold should I use for "+key+" days, in your experience?\n(Choose one: -15 or -25)\n >")
        if key=='extreme heat':
            threshold=input("\nWhat temperature threshold should I use for "+key+" days, in your experience?\n(Choose one: 25, 27, 29, 30 or 32)\n >")
        master_hazard_dict[key]["var"]=str(str(master_hazard_dict[key]["var"])+"_"+str(threshold))
        master_hazard_dict[key]["var_en"]=str(str(master_hazard_dict[key]["var_en"])+" "+str(threshold)+" °C")
   
    if master_hazard_dict[key]["resource"]=="climatedata.ca":
        print ("\nI've found some data on ClimateData.ca that is related to "+key.upper()+". This data is for your location. I'll open the map in your web browser, and also summarize the recent past as well as a period that includes the "+str(decade)+"s, your building's estimated end-of-service-life:\n")
        #url containing map; note this is kinda annoying... need to find a less pop-up approach if possible
        url="https://climatedata.ca/explore/variable/?coords="+str(latitude)+","+str(longitude)+",12&geo-select=&var="+str(master_hazard_dict[key]["var"])+"&var-group="+str(master_hazard_dict[key]["group"])+"&mora=ann&rcp=rcp85&decade="+str(decade)+"s&sector="
        #url containing line chart data
        data_url="https://data.climatedata.ca/generate-charts/"+str(latitude)+"/"+str(longitude)+"/"+str(master_hazard_dict[key]["var"])+"/ann"
        r = requests.get(data_url)
        data=r.json()
        #note: the year 1970 is the 'zero' year for the chart data
        #note: times are given in miliseconds from/since 1970... wonder why miliseconds?
        baseline=data['modeled_historical_median']
        total=0
        num=0
        print("Baseline period = 1971-2000")
        for row in baseline:
            if row[0] > 0:
                if row[0] <= ((2000-1970)*31536000000):
                    total+=row[1]
                    num+=1
        print("   "+str(master_hazard_dict[key]["var_en"]+": 30-yr average median = " + str(round((total/num),1))) + " " + master_hazard_dict[key]["units"])
        print("\n")
        print("Future period = "+str(decade+1)+"-"+str(decade+30)+", RCP8.5")
        
        future=data['rcp85_median']
        total=0
        num=0
        for row in future:
            if row[0] >= ((decade-1970)*31536000000):
                if row[0] <= ((decade+30-1970)*31536000000):
                        total+=row[1]
                        num+=1
        print("   "+str(master_hazard_dict[key]["var_en"]+": 30-yr average median = " + str(round((total/num),1))) + " " + master_hazard_dict[key]["units"])
        
        rcp85_range=data['rcp85_range']
        total_low=0
        total_high=0
        num=0
        for row in rcp85_range:
            if row[0] >= ((decade-1970)*31536000000):
                if row[0] <= ((decade+30-1970)*31536000000):
                    total_low+=row[1]
                    num+=1
                    total_high+=row[2]
            
        print("   "+str(master_hazard_dict[key]["var_en"]+": 30-yr average 90th p average = " + str(round((total_high/num),1))) + " " + master_hazard_dict[key]["units"])
        print("   "+str(master_hazard_dict[key]["var_en"]+": 30-yr average 10th p average = " + str(round((total_low/num),1))) + " " + master_hazard_dict[key]["units"])
    elif master_hazard_dict[key]["resource"]=="CRBCPI":
        print("TODO: display some CRBCPI data for "+str(CRBCPI_i))
    else:
        print ("\nClimateData.ca does not contain "+key.upper()+" data yet; however, I found this resource that I think might be of interest to you:")
        url=master_hazard_dict[key]["URL"]
    webbrowser.open(url,new=0,autoraise=False)
    
    if yes_or_no("Based on what you see, and without worrying about being too precise at this point in the process, could your region be prone to "+key.upper()+", either now or in the future?\n"):
        hazard_dict[key]=master_hazard_dict[key] 
        
   
print(clear)
draw_stuff('sea level rise')       
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


#%%

#Now prompt the user to consider the weather/climate impacts, on a componentwise basis.
##Provide some standard hazards, and then prompt user to add more if needed
print(clear)
print("\n")
print("STEP 4: WEATHER AND CLIMATE IMPACTS ON BUILDING SYSTEMS AND COMPONENTS")
print("\n")

print("Now, let's consider the climate hazards you identified in the context of each of your building's components!\n")
input("Press Enter to continue...")
for component in building_component_dict:
    per_component_hazard_dict={}
    for h,v in hazard_dict.items():
        print(clear)
        print("Let's consider\n    "+h.upper()+"\nin the context of your building's\n    "+component.upper()+".\n")
        print(hazard_dict[h]["direction_statement"]+"\nReflecting on this, might you be concerned that "+h+" could impact your "+component.upper()+" now, or could emerge as a potential impactor to your "+component.upper()+", in the future?")
        if yes_or_no("") is True:
            per_component_hazard_dict[h]='' #add a new component-specific hazard to list. Leave value empty for now - will fill in subsequent loop.
    print(clear)
    if per_component_hazard_dict != []:
        print("You've identified a number of hazards that could impact your building's "+component+".\n")
        print("For each hazard, identify from 1-10, how concerned you are about impacts to the "+component+".\n")
        print("\nUse the following qualitative scale:\n")
        print("    <1----------------------------------------------------------------10>")
        print("not very concerned                                           extremely concerned")
        for k,v in per_component_hazard_dict.items():
            per_component_hazard_dict[k]=int(input(k+" (1-10):"))
    
    print(clear)    
    building_component_dict[component]=per_component_hazard_dict

# %% 
# TODO: refactor following code to account for change above (now, each component dictionary entry is assigned a dictionary not a list)
print(clear)
print("\n")
print("STEP 5: SUMMARY REPORT")
print("\n")

print("GOOD JOB!  IN CONSIDERING POTENTIAL CLIMATE HAZARDS FOR EACH COMPONENT OF YOUR BUILDING, YOU HAVE STARTED ON YOUR WAY TO A FULL CLIMATE CHANGE RISK ASSESSMENT!\n")
print("LET ME SUMMARIZE YOUR RESULTS, AND TRY TO POINT YOU TO SOME POTENTIAL SOURCES OF GOOD PAST AND FUTURE CLIMATE INFORMATION THAT IS RELEVANT TO YOUR BUILDING!\n")

sep="\n->"

# Estimate component(s) with most/least vulnerabilities by summing up numerical rankings for all hazards for each component.

for component,per_component_hazard_dict in building_component_dict.items():
    sumval=0
    for hazard,ranking in per_component_hazard_dict.items():
        sumval=sumval+ranking
    
    building_component_dict[component]["total_hazard_sum"]=sumval
    
ranks=[]
for component in building_component_dict:
    ranks.append(building_component_dict[component]["total_hazard_sum"])
    
sortrank=sorted(ranks, reverse=True)

print ("\n")
print("Based on your entries, I have attempted to rank your building's components from MOST to LEAST vulnerable:\n")
j=0
for i in range(len(sortrank)):
    if i+j < len(sortrank):
        flag=0
        for component in building_component_dict:
            if building_component_dict[component]["total_hazard_sum"]==sortrank[i+j]:
                if flag != 1:
                    print("  "+str(i+j+1)+".  "+component)
                else:
                    print("  "+str(i+j+1)+". (tie)  " + component)
                    j+=1
                flag=1

print("\nIt might make sense to focus most on the components nearer the top of this list during your climate change risk assessment.")
#print("Conversely, your least vulnerable building components look to to be:\n"+sep+sep.join(least_vulnerable_components)+"\n")
'''
# Rank hazards by # of times they are mentioned as component hazards.  Display top hazards.
hazard_list=sum(building_component_dict.values(), [])
l_sorted=Counter(hazard_list).most_common()
max_len=min(3,len(l_sorted))
print("Based on these lists, the top climate hazards for your building appear to be:\n")
for h in range(max_len):
    print("->"+l_sorted[h][0])
print("\nIt might make sense to focus most on these hazards during your climate change risk assessment climate data gathering.\n")
'''
input ("Press ENTER to continue")
print (clear)

'''
print("I've identified some available climate data resources, specific to the hazards that you indicated your building may be (or become) vulnerable to!")
for h,r in l_sorted:
    print("\nTo better understand changes to "+h+" hazards, you may want to check out: " + hazard_dict[h]["resource"] + ":\n" + hazard_dict[h]["URL"])
    #if hazard_dict[h]["resource"]=="climatedata.ca":
        #url="https://climatedata.ca/explore/variable/?coords="+str(latitude)+","+str(longitude)+",12&geo-select=&var="+str(hazard_dict[h]["var"])+"&var-group="+str(hazard_dict[h]["group"])+"&mora=ann&rcp=rcp85&decade="+str(decade)+"s&sector="
        #webbrowser.open(url,new=2,autoraise=False)
'''
#TODO: allow for multiple resource URLs
#TODO: Improve this closing guidance.

print(clear)
print("\n")
print("STEP 6: NEXT STEPS")
print("\n")

print("\n")
input("Let's summarize what you've done here - AND - what you still need to do to ensure your building's climate resiliency! (press ENTER to continue)\n")
input("1) You described your building's basics, including expected lifetime and major components... (press ENTER to continue)\n")
input("2) You identified some key present and future climate hazards for your region... (press ENTER to continue)\n")
input("3) You thought about which climate hazards could impact each of your building's components... (press ENTER to continue)\n")
input("4) You developed a summary that prioritized major hazards and identified some promising climate information for each one... (ENTER to continue)\n")
input("Your next tasks are: (ENTER to continue)\n")
input("5) Get this climate information and develop a tailored climate change summary report for your building... (ENTER to continue)\n")
input("6) Use this report to understand how the likelihood and severity of each hazard will change in the future... (ENTER to continue)\n")
input("7) Undertake risk assessments for present and future conditions to understand how risks will change for each of your components over time... (ENTER to continue)\n")
input("8) If any risk profiles risk to unacceptable levels due to climate change, consider developing risk reduction (adaptation) actions! (ENTER to continue)\n")

# %%
# GAUGE USER'S RISK TOLERANCE - suggested change: make this about training and guidance?
# TODO - improve this langauge and approach to describing future uncertainty in terms of risk.
print(clear)
draw_stuff("books")

print ("UNLIKE HISTORICAL CLIMATE NORMALS, FUTURE CLIMATE CONDITIONS CAN'T BE BOILED DOWN TO A SINGLE NUMBER.")
print ("IN FACT, THE FUTURE IS FAR FROM CERTAIN. THE AMOUNT OF FUTURE CLIMATE CHANGE ONE NEEDS TO PLAN FOR DEPENDS LARGELY ON FUTURE GREENHOUSE EMISSIONS.")
print ("\n")
print ("YOU COULD ALWAYS 'PLAN FOR THE WORST AND HOPE FOR THE BEST,' BUT IT ISN'T ALWAYS FINANCIALLY POSSIBLE TO PLAN FOR ALL POSSIBLE FUTURE HAZARDS.")
print ("\n")
print ("BEGIN PRE-FLIGHT CHECK LIST:")
print ("\n")
if yes_or_no("Have you watched our short training video on future climate scenarios?\n >") is False:
    print("OK, I'll wait here while you go watch that video. It won't take long.")
    url="https://climatedata.ca/resource/introduction-to-decision-making-using-climate-scenarios/"
    webbrowser.open(url,new=2,autoraise=False)

if yes_or_no("Have you watched our short training video on understanding ranges in climate projections?\n >") is False:
    url="https://climatedata.ca/resource/understanding-ranges-in-climate-projections/"
    webbrowser.open(url,new=2,autoraise=False)
    
if yes_or_no("Have you used ClimateData.ca before, and are comfortable with navigating the map?\n>") is False:
    url="https://climatedata.ca/resource/how-to-navigate-variable-maps/"
    webbrowser.open(url,new=2,autoraise=False)
    
print("\n")
print("Well done, and good luck with using this climate information and training to increase your building's resilience to climate change!")
email_address=input("Enter your email address to receive a brief report that summarizes the results of this decision support tool!")
input("When you're ready to say goodbye to me, press ENTER!")


draw_stuff('wizard_end')
print ("POOF! ALL DONE")


#%%


    
