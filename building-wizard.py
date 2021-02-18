import json
from geopy.geocoders import Nominatim
import webbrowser
from textart import draw_stuff
import requests
import numpy as np
from sklearn.neighbors import BallTree
import pandas as pd
from collections import Counter

dT_levels=['+0.5C','+1.0C','+1.5C','+2.0C','+2.5C','+3.0C','+3.5C']

CRBCPI_data={dT_levels[0]:pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+0.5C_NBCC.xls"),
             dT_levels[1]:pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+1.0C_NBCC.xls"),
             dT_levels[2]:pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+1.5C_NBCC.xls"),
             dT_levels[3]:pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+2.0C_NBCC.xls"),
             dT_levels[4]:pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+2.5C_NBCC.xls"),
             dT_levels[5]:pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+3.0C_NBCC.xls"),
             dT_levels[6]:pd.read_excel("https://climate-scenarios.canada.ca/files/buildings_report/Appendix_1.2_NBCC/Appendix1.2_+3.5C_NBCC.xls")}

CRBCPI_dT_to_time=pd.DataFrame([[2023,2023,2023,2023],
                                [2035,2046,2046,np.nan],
                                [2047,2070,2070,np.nan],
                                [2059,2087,np.nan,np.nan],
                                [2069,np.nan,np.nan,np.nan],
                                [2080,np.nan,np.nan,np.nan],
                                [2090,np.nan,np.nan,np.nan]],
                                index=dT_levels,columns=['RCP8.5','RCP6.0','RCP4.5','RCP2.6'])

#SETUP FUNCTIONS

# Quick function to error-catch non-standard y/n responses
def yes_or_no(question):
    while True:
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply != "":
            if reply[0] == 'y':
                return True
            if reply[0] == 'n':
                return False
            else:
                print("Whoops - please enter 'y' or 'n'.")

#%%
          
screen_clear="\033[H\033[J"

print(screen_clear)
print("WELCOME TO CLIMATEDATA.CA's INTERACTIVE BUILDING SECTOR CLIMATE DECISION SUPPORT TOOL")
print("\n")
print("This interactive tool is designed for engineers, architects, planners, and other professionals in the buildings sector.\n")
print("\nThe tool has two main goals:\n")
print("   GOAL 1 - Gain a better sense of how to select useful climate change information for biulding-specific climate change risk assessments")
print("   GOAL 2 - Help find some  useful climate change information for your building")
print("\n")
print("You will be guided through the following 5 Steps:\n")
print("   STEP 1 - Provide basic information about your building")
print("   STEP 2 - Develop an inventory of building components and systems")
print("   STEP 3 - Identify the local weather and climate hazards that may matter for your building")
print("   STEP 4 - Explore the impacts of weather and climate hazards on building components and systems")
print("   STEP 5 - Summary report and next steps")

print("\nThis tool helps you select and source relevant climate change information for your building's climate change risk assessment.")
print("However, it cannot undertake a full risk analysis or identify climate adaptation options for your building.")
print("At the end of this tool's process, you will receive some important next risk assessment and adaptation planning steps to consider.\n")
print("\nThis process should take around 20 minutes to complete.")
input("Press Enter to begin...")

#%%
# CHECK USER'S BACKGROUND KNOWLEDGE
print(screen_clear)
draw_stuff("books")
print("\nCORE KNOWLEDGE CHECK-LIST\n")
print("Before we begin, it is important that you are comfortable with certain definitions and concepts related to climate models and future climate data.")

if yes_or_no("The amount of climate change we experience in the future depends on many factors, most notably future global emissions of greenhouse gases. Are you familiar with future climate scenarios, including the difference between RCP2.6, RCP4.5, and RCP8.5?\n >") is False:
    print("Here is a very short video that will quickly bring you up to speed. It is hightly recommended that you watch it before conitnuing.")
    url="https://climatedata.ca/resource/introduction-to-decision-making-using-climate-scenarios/"
    webbrowser.open(url,new=2,autoraise=False)

if yes_or_no("Climate data is best represented using a range of values, rather than a single number. Do you understand why this is the case?\n >") is False:
    print("Here is a very short video explaining why users should look at a range of model projections, rather than focus on a single value. It is highly recommeded that you take the time to watch it.")
    url="https://climatedata.ca/resource/understanding-ranges-in-climate-projections/"
    webbrowser.open(url,new=2,autoraise=False)
    
if yes_or_no("Have you used ClimateData.ca before, and are comfortable with navigating the map?\n>") is False:
    url="https://climatedata.ca/resource/how-to-navigate-variable-maps/"
    webbrowser.open(url,new=2,autoraise=False)
    
if yes_or_no("Are you familiar with the Government of Canada Climate-Resilience Buildings and Core Public Infrastructure program?") is False:
    url="https://www.infrastructure.gc.ca/plan/crbcpi-irccipb-eng.html"
    webbrowser.open(url,new=2,autoraise=False)

if yes_or_no("Are you familiar with the Government of Canada Climate Lens program?") is False:
    url="https://www.infrastructure.gc.ca/pub/other-autre/cl-occ-eng.html"
    webbrowser.open(url,new=2,autoraise=False)
    
if yes_or_no("Are you familiar with the Federation of Canadian Municipalities for Climate Innovation program?") is False:
    url="https://fcm.ca/en/programs/municipalities-climate-innovation-program/climate-change-adaptation"
    webbrowser.open(url,new=2,autoraise=False)    
    
if yes_or_no("Are you familiar with Monty Python's Architect Sketch?") is False:
    url="https://www.youtube.com/watch?v=QfArEGCm7yM"
    webbrowser.open(url,new=2,autoraise=False)     

input ("Press ENTER to continue...")
#%%
### PIEVC Step 1: PROJECT DEFINITION ###
print(screen_clear)
print("\n")
print("STEP 1: BASIC PROJECT DEFINITION")
print("\n")
draw_stuff('house')
print("\n")

print("What type of building are you designing, building, or operating?\n") # FYI
building_type=input(">")

if yes_or_no("Is this an existing building?\n >"):
    building_stage="existing"
    construction_date=input("When was your "+building_type+" constructed?\n >")
else:
    building_stage=input("OK, so what stage of the building process are you in? (design stage, construction stage, retrofitting, etc.) \n >")
    construction_date=input("And what's the anticipated final year of construction? \n >")

#TODO: see if possible to auto-specify standard design lives from NBCC or CSA S478 Building Durability

print("What is your "+building_type+"'s intended design life in years (intended service life before a major intervention is required (retrofit, modernize, demolish, etc.)?")
if yes_or_no("If you're unsure of your building's design lives, you can find a description of standard building design lives in CSA S478.  Would you like to see this?") is True:
    url="https://www.csagroup.org/store/product/CSA%20S478%3A19/?gclid=CjwKCAiAmrOBBhA0EiwArn3mfGwIl8Ll8Oa0BkkEPJgzrITQ8GeDn3M1tHu4inRLTxvgtjy3DHzkfRoCfeMQAvD_BwE"
    webbrowser.open(url,new=2,autoraise=False)
design_life=input(">")
design_year=int(construction_date) + int(design_life)
decade=int(round(design_year,-1))
if decade <2030:
    raise TypeError("Looks like your "+building_type+"'s design life is relatively short!  You may not need to worry about using future climate information!  Stick to good historical observations instead!\n")

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
    longitude=float(input("Enter your Longitude (in negative degrees west, in decimals): \n >"))

if not 41. <= latitude <= 84.:
    raise TypeError("Looks like your latitude is outside of Canada.  Can you re-check this?\n")
if not -142. <= longitude <= -.52:
    raise TypeError("Looks like your longitude is outside of Canada.  Can you re-check this?\n")

#find nearest CPI point (use CRBCPI_i to index climate data for this point, from CRBCPI data dictionary)
#Set up nearest neighbour search on the sphere
lat=np.deg2rad(CRBCPI_data["+0.5C"]["Latitude"].values)
lon=np.deg2rad(CRBCPI_data["+0.5C"]["Longitude"].values)
ball=BallTree(np.vstack((lat,lon)).swapaxes(1,0),metric="haversine")
CRBCPI_distance,CRBCPI_i=ball.query(np.deg2rad([[latitude,longitude]]),k=1)
CRBCPI_i=CRBCPI_i[0][0]

elev=float(input("How far above sea level is your building (in meters)? \n >"))

# %%
### PIEVC Step 2: DATA GATHERING ###

# TODO: 

print(screen_clear)
print("\n")
print("STEP 2: INVENTORY OF BUILDING SYSTEMS AND COMPONENTS")
print("\n")
print("Understanding climate change impacts to your building requires first developing a high-level catalog of your building's systems and components.")
print("We'll use this catalog to assess how climate change could impact important aspects of your building in different ways.")
print("Please enter 'yes' for all the building systems you'd like to consider in this assessment (note, you'll need about 2 minutes of thinking per component, later in the process):")


# Initialize a list of building components that the user will grow interactively.
# This list will store component-specific hazards.
building_component_dict={}

# Load the master list of building components, from which a subset of user-specific building hazards is built.
with open('master_building_component_database.json', 'r') as j:
    master_building_component_dict = json.loads(j.read())

for c in master_building_component_dict:
    if yes_or_no(c):
        building_component_dict[c]=master_building_component_dict[c]

# Prompt the user to define the components of their building.  This list can be as long as needed.
print("Are there any other key, major structural or system components of your building and property that you'd like to include?\n")
print("For this exercise, let's try to keep to a high level here (12-15 components, maximum!).   Type 'done' when done.\n")

while True:
    token=input("->")
    if token != "done":
        building_component_dict[token]=[]
    else:
        break 

#%%

#NEXT STEP: UNDERSTAND HISTORICAL CLIMATE HAZARDS IN REGION
print(screen_clear)
print("\n")
print("STEP 3: WEATHER HAZARDS AND CLIMATE DATA")
print("\n")
draw_stuff("clouds")
print("\nNext, we need to identify the kinds of weather hazards your building's region is susceptible to.")
print("\nYou will be asked whether a particular weather hazard occurs in your region. Using some very basic climate model projections, you will also be asked to consider whether a particular weather hazard can emerge as a growing issue in a changing climate.")
print("\nYou do not need to be a climate scientist to correctly fill this section out - the goals are to identify likely hazards and to consider, at a very high level, the impacts of climate change.")
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
    print(screen_clear)
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
        url=master_hazard_dict[key]["URL"]
        location=CRBCPI_data["+0.5C"]["Location"][np.squeeze(CRBCPI_i)]
        proximity="{x:.0f}".format(x=np.squeeze(CRBCPI_distance)*6378.) # convert distance from radians to kilometers, format for rounded-value printing
        
        # Convert from dT-based scaling to scenario/year scaling using interpolation in time.
        x=CRBCPI_dT_to_time['RCP8.5'] 
        var=master_hazard_dict[key]["var"]
        y=[]
        for dT in dT_levels:
            y.append(CRBCPI_data[dT][var+"_"+dT][CRBCPI_i])
        dv=np.interp(decade,x,y) #TODO: consider if we can change the decade value - CRBCPI data can go with shorter climatological periods.
        
        dv="{x:.1f}".format(x=dv)
        print("\nI've found some data from the Government of Canada Climate-Resilient Buildings and Core Public Infrastructure (RCBCPI) for changes to "+key.upper()+".")
        print("Specifically, I think you may be interested in changes in "+master_hazard_dict[key]["var_en"]+", in "+location+", around "+proximity+" km from you.\n")
        print("Under the RCP8.5 scenario, "+master_hazard_dict[key]["var_en"]+" may change by around "+dv+master_hazard_dict[key]["units"]+".\n")
        print("Please carefully judge yourself whether this location is similar enough to your building's site, for this information to be useful!")  
    else:
        print ("\nFor, "+key.upper()+" I found this resource that I think might be of interest to you:")
        url=master_hazard_dict[key]["URL"]
    
    webbrowser.open(url,new=0,autoraise=False)
    
    if yes_or_no("Based on what you see, and without worrying about being too precise at this point in the process, could your region be prone to "+key.upper()+", either now or in the future?\n"):
        hazard_dict[key]=master_hazard_dict[key] 
   
print(screen_clear)
draw_stuff('sea level rise')       
if yes_or_no("Is your region near the ocean?\n"):
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
    print(screen_clear)


# %%
# And allow for 'other' entries
print(screen_clear)
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
print(screen_clear)
print("\n")
print("STEP 4: WEATHER AND CLIMATE IMPACTS ON BUILDING SYSTEMS AND COMPONENTS")
print("\n")

print("Now, let's consider the climate hazards you identified in the context of each of your building's components!\n")
input("Press Enter to continue...")
for component in building_component_dict:
    per_component_hazard_dict={}
    for h,v in hazard_dict.items():
        print(screen_clear)
        print("Let's consider\n    "+h.upper()+"\nin the context of your building's\n    "+component.upper()+".\n")
        print(hazard_dict[h]["direction_statement"]+"\nReflecting on this, might you be concerned that "+h+" could impact your "+component.upper()+" now, or could emerge as a potential impactor to your "+component.upper()+", in the future?")
        if yes_or_no("") is True:
            per_component_hazard_dict[h]='' #add a new component-specific hazard to list. Leave value empty for now - will fill in subsequent loop.
    print(screen_clear)
    if per_component_hazard_dict != []:
        print("You've identified a number of hazards that could impact your building's "+component+".\n")
        print("For each hazard, identify from 1-10, how concerned you are about impacts to the "+component+".\n")
        print("\nUse the following qualitative scale:\n")
        print("    <1----------------------------------------------------------------10>")
        print("not very concerned                                           extremely concerned\n")
        
        for k,v in per_component_hazard_dict.items():
            while True:
                rankval=input(k+" (1-10):")
                if rankval.isnumeric():
                    rankval=int(rankval)
                    if 1<=rankval<=10:
                        per_component_hazard_dict[k]=int(rankval)
                        break
                    else:
                        print("Whoops - please enter a number from 1-10")  
                else:
                    print("Whoops - please enter a number from 1-10")
    
    print(screen_clear)    
    building_component_dict[component]=per_component_hazard_dict

# %% 

print(screen_clear)
print("\n")
print("STEP 5: SUMMARY REPORT")
print("\n")

print("GOOD JOB!  IN CONSIDERING POTENTIAL CLIMATE HAZARDS FOR EACH COMPONENT OF YOUR BUILDING, YOU HAVE STARTED ON YOUR WAY TO A FULL CLIMATE CHANGE RISK ASSESSMENT!\n")
print("LET ME SUMMARIZE YOUR RESULTS, AND TRY TO POINT YOU TO SOME POTENTIAL SOURCES OF GOOD PAST AND FUTURE CLIMATE INFORMATION THAT IS RELEVANT TO YOUR BUILDING!\n")

sep="\n->"

# %% 
# Estimate component(s) with most/least vulnerabilities by summing up numerical rankings for all hazards for each component.
aggregate_hazard_list=[]
for component,per_component_hazard_dict in building_component_dict.items():
    sumval=0
    for hazard,ranking in per_component_hazard_dict.items():
        sumval=sumval+ranking
        aggregate_hazard_list.append(hazard)
    building_component_dict[component]["total_hazard_sum"]=sumval
    
ranks=[]
for component in building_component_dict:
    ranks.append(building_component_dict[component]["total_hazard_sum"])
    
sortrank=sorted(ranks, reverse=True)
# %%

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

# %% 
# Rank hazards by # of times they are mentioned as component hazards.  Display top hazards.
l_sorted=Counter(aggregate_hazard_list).most_common()
max_len=min(3,len(l_sorted))
print("Based on these lists, the top climate hazards that impact the most components of building appear to be:\n")
for h in range(max_len):
    print("->"+l_sorted[h][0])
print("\nIt might make sense to focus most on these hazards during your climate change risk assessment climate data gathering.\n")

input ("Press ENTER to continue")
print(screen_clear)

print("I've identified some available climate data resources that are specific to the hazards that you indicated your building may be (or become) vulnerable to!")
for h,r in l_sorted:
    print("\nTo better understand changes to "+h+" hazards, you may want to check out: " + hazard_dict[h]["resource"] + ":\n" + hazard_dict[h]["URL"])

#TODO: allow for multiple resource URLs
#TODO: Improve this closing guidance.
input ("Press ENTER to continue")
print(screen_clear)

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

print("\n")
print("Well done, and good luck with using this climate information and training to increase your building's resilience to climate change!")
email_address=input("Enter your email address to receive a brief report that summarizes the results of this decision support tool!") #FYI
input("When you're ready to say goodbye, press ENTER!")

print(screen_clear)
draw_stuff('wizard_end')
print ("POOF! ALL DONE")


#%%


    
