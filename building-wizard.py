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
print("   GOAL 1 - Gain a better sense of how to select useful climate change information for building-specific climate change considerations, including risk assessments and long term planning.")
print("   GOAL 2 - Help find some  useful climate change information for your building")
print("\n")
print("You will be guided through the following 5 Steps:\n")
print("   STEP 1 - Provide basic information about your building")
print("   STEP 2 - Develop an inventory of building components and systems")
print("   STEP 3 - Identify the local weather and climate hazards that may matter for your building")
print("   STEP 4 - Explore the impacts of weather and climate hazards on building components and systems")
print("   STEP 5 - Summary report and next steps")
print("\nThis tool helps you select and source relevant climate change information for your building planning process.")
print("At the end of this tool's process, you will receive some important next steps to consider.\n")
print("\nThis process should take around 20 minutes to complete.")
input("Press Enter to continue...")

print(screen_clear)

print("CLIMATE DECISION SUPPORT TOOL DISCLAIMER AND RELEASE OF LIABILITY")
print('This tool supports users in learning how to identify a subset of appropriate climate change information for building planning.  However, it is not an offical engineering design tool.  Users of this tool accept full responsibilty for expert judgement and professional standard of care in applying this and other climate change information to detailed project planning and engineering.  The authors of this tool accept no responsibilty for damage resulting from misuse of the datasets provided by this tool during project planning or execution.')
print('This tool endeavours to summarize a selection of important building hazards and describe changes to these hazards resulting from climate change.  However, some hazards do not have reliable future information available, to the best knowledge of the authors of this tool, at this time.  The authors take no responsibility for negligent omission of consideration of such hazards in project planning or execution.')
print('This tool is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and non infringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the tool.')
print("")
print('In short, please combine the use of this tool with personal judgement, and full acceptance of liability and professional standard of care.')
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
    if int(construction_date) < 2000:
        old_construction=True
        #TODO: based on old_construction flag, add a comment in final report generator.
        print("It looks like your building is at least 20 years old already!  Climate has changed significantly since then - you should assess whether your building is already at risk from change climate conditions!")
else:
    building_stage=input("OK, so what stage of the building process are you in? (design stage, construction stage, retrofitting, etc.) \n >")
    construction_date=input("And what's the anticipated final year of construction? \n >")

#TODO: see if possible to auto-specify standard design lives from NBCC or CSA S478 Building Durability

print("\nWhat is your "+building_type+"'s intended design life in years (intended service life before a major intervention is required (retrofit, modernize, demolish, etc.)?")
print("\nType 'help' if you are unsure how to determine your building's approximately design life.")
design_life=input(">")
while design_life=='help':
    print("You can find a description of standard building design lives in CSA S478. I'll open that resource for you now.")
    url="https://www.csagroup.org/store/product/CSA%20S478%3A19/?gclid=CjwKCAiAmrOBBhA0EiwArn3mfGwIl8Ll8Oa0BkkEPJgzrITQ8GeDn3M1tHu4inRLTxvgtjy3DHzkfRoCfeMQAvD_BwE"
    webbrowser.open(url,new=2,autoraise=False)
    print("\nWhat is your "+building_type+"'s intended design life in years (intended service life before a major intervention is required (retrofit, modernize, demolish, etc.)?")
    print("\nType 'help' if you are unsure how to determine your building's approximately design life.")
    design_life=input(">")
design_year=int(construction_date) + int(design_life)
decade=int(round(design_year,-1))
if decade <2030:
    print("Looks like your "+building_type+"'s expected design life is relatively short!\n")
    print("For relatively short-term design lives, you may want to consider applying recent observational weather and climate information, instead of future projections from climate models.\n")
    print("However, be careful using only past observations – some impacts are already quite different due to ongoing climate change. You may need expert opinion for this or use of climate model simulation resuts centred on the present day.\n")
    print("Keep these thoughts in mind in the context of your building's design life, as you continue with this exercise.\n")
if decade > 2070:
    if decade > 2100:
        print("NOTE: Just a heads up, I only have climate data that goes until the year 2100. Your building's design life exceeds this time frame. I'll just stick to showing you data from the 30-year period spanning 2071-2100.")
    decade=2070
    
# %%
## Get location

#if yes_or_no("Would you like me to look up your location from your latitude and longitude for you?\n >"):
geolocator = Nominatim(user_agent="example")
loc_address=str(input("Location of building site (full or partial address)? \n >"))
location = geolocator.geocode(loc_address)
latitude = location.latitude
longitude = location.longitude  

#else:
#    latitude=float(input("Enter your Latitude (in decimals): \n >"))
#    longitude=float(input("Enter your Longitude (in negative degrees west, in decimals): \n >"))

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


print("Your latitude is..." + str(latitude))
print("Your longitude is..." + str(longitude))

elev=float(input("\nHow far above sea level is your building (in meters)? \n >"))

## User's profession
professions=['Engineer','Architect','Owner/operator','Regulator','OTHER']
print("\nAnd finally, which of the following best describes your profession?\n")
counter=1
for p in professions:
    print("  " + str(counter) + ". " + p)
    counter+=1
userprof=input("Enter a number from 1 to " + str(counter-1) + " >")
users_profession=professions[int(userprof)-1]
if users_profession == "OTHER":
    users_profession=input("Please type in your profession >")


# %%
### PIEVC Step 2: DATA GATHERING ###

# TODO: 

print(screen_clear)
print("\n")
print("STEP 2: INVENTORY OF BUILDING SYSTEMS AND COMPONENTS")
print("\n")
print("Understanding climate change impacts to your building requires first developing a high-level catalog of your building's systems and components.")
print("\nWe'll use this catalog to assess how climate change could impact important aspects of your building in different ways.")
print("\nAnswer 'yes' to include any of the following Level 1 Major Group Elements in the analysis.")
print("\nYou will then be asked to identify Level 2 Components you wish to include in the analysis. Note, you'll need about 2 minutes of thinking per component, later in the process: ")

# Initialize a list of building components that the user will grow interactively.
# This list will store component-specific hazards.
building_component_dict={}

# Load the master list of building components, from which a subset of user-specific building hazards is built.
with open('master_building_component_database.json', 'r') as j:
    master_building_component_dict = json.loads(j.read())

for c in master_building_component_dict:
    if yes_or_no(c + " - " + master_building_component_dict[c]["description"]):
        for g in master_building_component_dict[c]["group"]:
            if yes_or_no("   " + g):
                building_component_dict[g]=g #master_building_component_dict[c][g]

# Prompt the user to define the components of their building.  This list can be as long as needed.
print("\nAre there any other major structural or system components of your building and property that you'd like to include?\n")
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

# Initialize a blank list of weather hazards that the user will grow following a series of y/n questions:
hazard_dict={}

# Load the master list of climate hazards, from which a subset of user-specific building hazards is built,
with open('master_hazard_database.json', 'r') as j:
    master_hazard_dict = json.loads(j.read())

#Dynamically generate a customized hazard_dict based on user prompts.
hazard_list=["extreme rain","high winds","extreme heat","extreme cold","extreme snow","wildfire","river/lake flooding"] #TODO: get this from JSON file
for h in hazard_list:
    print(screen_clear)
    draw_stuff(h)
    print(h.upper())
    print(master_hazard_dict[h]["impact_statement"])
    if master_hazard_dict[h]["type"]=="threshold":

        while True:      
            if h=='extreme cold':
                options=[-15,-25]
                threshold=input("\nWhat temperature threshold should I use for "+h+" days, in your experience?\n(Choose one: -15 or -25)\n >")
            if h=='extreme heat':
                options=[25, 27, 29, 30, 32]
                threshold=input("\nWhat temperature threshold should I use for "+h+" days, in your experience?\n(Choose one: 25, 27, 29, 30, or 32)\n >")
            if threshold.strip('-').isnumeric():
                threshold=int(threshold)
                if threshold in options:
                    master_hazard_dict[h]["var"]=str(str(master_hazard_dict[h]["var"])+"_"+str(threshold))
                    master_hazard_dict[h]["var_en"]=str(str(master_hazard_dict[h]["var_en"])+" "+str(threshold)+" °C")
                    break
                else:
                    print("Whoops - please enter a valid temperature threshold")  
            else:
                print("Whoops - please enter a valid temperature threshold")        
        
    if master_hazard_dict[h]["resource"]=="climatedata.ca":
                #url containing line chart data
        data_url="https://data.climatedata.ca/generate-charts/"+str(latitude)+"/"+str(longitude)+"/"+str(master_hazard_dict[h]["var"])+"/ann"
        r = requests.get(data_url)
        data=r.json()
        #note: the year 1970 is the 'zero' year for the chart data.
        #note: times are given in miliseconds from/since 1970.

        #TODO: make the start and end periods both align with the project life.  
        #TODO: add direction of change statements to all source versions.  add 'not much change' statement based on releativre change
        time = np.array([i[0] for i in data['modeled_historical_median']])/31536000000.
        val = np.array([i[1] for i in data['modeled_historical_median']])
        baseline_mean=np.mean(val[time<=2000-1970])
        time = np.array([i[0] for i in data['rcp85_median']])/31536000000.
        val = np.array([i[1] for i in data['rcp85_median']])
        future_mean=np.mean(val[(decade-1970<=time) & (time<=decade+30-1970)])
        dv=future_mean-baseline_mean
        if float(dv) >= 0:
            direction_statement="increase"
        else:
            direction_statement="decrease"    
        print("\nI've found some information from climatedata.ca for "+h.upper()+ " at your location")
        print("\n                         "+master_hazard_dict[h]["var_en"])
        print("------------------------------------------------------------------")
        print("\t1970-2000 Baseline\t"+str(decade)+"-"+str(decade+30)+" Future (RCP8.5)")
        print("\t" + str(round((baseline_mean),0)) + " " + master_hazard_dict[h]["units"]+"         \t"+str(round((future_mean),0)) + " " + master_hazard_dict[h]["units"]+" (a change of " + str(round(((future_mean-baseline_mean)/baseline_mean*100),0))+"%)")
        
    elif master_hazard_dict[h]["resource"]=="CRBCPI":
        #TODO: get updated historical info, so we can report absolute change (and not just delta)
        url=master_hazard_dict[h]["URL"]
        location=CRBCPI_data["+0.5C"]["Location"][np.squeeze(CRBCPI_i)]
        proximity="{x:.0f}".format(x=np.squeeze(CRBCPI_distance)*6378.) # convert distance from radians to kilometers, format for rounded-value printing
        
        # Convert from dT-based scaling to scenario/year scaling using interpolation in time.
        x=CRBCPI_dT_to_time['RCP8.5'] 
        var=master_hazard_dict[h]["var"]
        y=[]
        for dT in dT_levels:
            y.append(CRBCPI_data[dT][var+"_"+dT][CRBCPI_i])
        dv=np.interp(decade,x,y) 
        #TODO: consider if we can change the decade value - CRBCPI data can go with shorter climatological periods. 
        dv="{x:.0f}".format(x=dv)
        print("\nI've found some information from the Climate-Resilient Buildings and Core Public Infrastructure (RCBCPI) project for "+h.upper()+" near your location, specifically, "+master_hazard_dict[h]["var_en"]+".")
        print("This information is from "+location+", around "+proximity+"km from your building site.\n")
        if float(dv) >= 0:
            direction_statement="increase"
        else:
            direction_statement="decrease"            
        print(master_hazard_dict[h]["var_en"]+" looks set to "+direction_statement+" (for example, by around "+dv+master_hazard_dict[h]["units"]+", by the end of your building's design life, for the high-end RCP 8.5 climate change scenario).")
        print(master_hazard_dict[h]["direction_confidence"])
        print(master_hazard_dict[h]["magnitude_confidence"])
    else:
        print("")
    if yes_or_no("Based on this general information, and considering your region's and building's possible vulnerabilities to "+h.upper()+" now or in the future, should I include "+h.upper()+" in this assessment?\n"):
        hazard_dict[h]=master_hazard_dict[h] 
   
print(screen_clear)
draw_stuff('sea level rise')       
if yes_or_no("Is your region near the ocean?\n"):
    if elev > 50.:
        h="sea level rise"
        print(h.upper())
        print(master_hazard_dict[h]["impact_statement"])
        if yes_or_no("Based on your elevation, even though your region is near the ocean, it sounds like you may not have to worry about sea level rise.  Is it OK to skip an assessment of sea level rise on your building?\n") is False:
            hazard_dict[h]=master_hazard_dict[h]
    else:
        h="sea level rise"
        hazard_dict[h]=master_hazard_dict[h]            

if latitude > 55.: #This threshold was quickly set - should re-evaluate based on CRBCPI or other, Canadian permafrost map.
    draw_stuff('extreme cold')
    h="permafrost loss"
    print(h.upper())
    print(master_hazard_dict[h]["impact_statement"])
    if yes_or_no("Does any permafrost occur in your region?\n"):
        hazard_dict[h]=master_hazard_dict[h]
    print(screen_clear)


# %%
# And allow for 'other' entries
print(screen_clear)
token=[]
print("Any other weather hazards you want to tell me about before we continue?  Please enter these hazards below (or type 'done' if you are done)")
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

print("Now, let's consider the interactions of climate hazards you identified, with each of your building's components!\n")
do_vulnerability_ranking = yes_or_no("As part of this step, would you like to consider the relative level of concern you have for each of these interactions on a 1-10 scale?  This well help me prioritize what climate information may be most important to you.")
    
input("Press Enter to continue...")
for component in building_component_dict:
    per_component_hazard_dict = {} #initialize an empty list, to be populated with per-component hazards
    for hazard, tmp in hazard_dict.items():
        print(screen_clear)
        print("Let's consider\n    "+hazard.upper() +
              "\nin the context of your building's\n    "+component.upper()+".\n")
        print(hazard_dict[hazard]["direction_statement"]+"\nReflecting on this, might you be concerned that "+hazard+" could impact your " +
              component.upper()+" now, or could emerge as a potential impactor to your "+component.upper()+", in the future?")
        if yes_or_no("") is True:
            # add a new component-specific hazard to list. Leave value empty for now - will fill in subsequent loop.
            per_component_hazard_dict[hazard] = np.nan #set vulnerability ranking to nan here as placeholder.
    print(screen_clear)
    if do_vulnerability_ranking:
        if per_component_hazard_dict != []:
            #print("You've identified a number of hazards that could impact your building's "+component+".\n")
            print(
                "Please identify from 1-10, how concerned you are about impacts to the "+component+".\n")
            print("\nUse the following qualitative scale:\n")
            print("    <1----------------------------------------------------------------10>")
            print("not very concerned                                           extremely concerned\n")
            for pc_hazard, tmp in per_component_hazard_dict.items():
                while True:
                    rankval = input(pc_hazard+" (1-10):")
                    if rankval.isnumeric():
                        rankval = int(rankval)
                        if 1 <= rankval <= 10:
                            # set dictionary value for hazard, to non-nan rankval value.
                            per_component_hazard_dict[pc_hazard] = int(rankval)
                            break
                        else:
                            print("Whoops - please enter a number from 1-10")
                    else:
                        print("Whoops - please enter a number from 1-10")

    print(screen_clear)
    building_component_dict[component] = per_component_hazard_dict

# %% 

print(screen_clear)
print("\n")
print("STEP 5: SUMMARY REPORT")
print("\n")

print("GOOD JOB!  IN CONSIDERING POTENTIAL CLIMATE HAZARDS FOR EACH COMPONENT OF YOUR BUILDING, YOU HAVE STARTED ON YOUR WAY TO INTEGRATE CLIMATE CHANGE CONSIDERATIONS INTO BUILDING PLANNING!\n")
print("LET ME SUMMARIZE YOUR RESULTS, AND TRY TO POINT YOU TO SOME POTENTIAL SOURCES OF GOOD PAST AND FUTURE CLIMATE INFORMATION THAT IS RELEVANT TO YOUR BUILDING!\n")

sep="\n->"

# Estimate component(s) with most/least vulnerabilities by summing up numerical rankings for all hazards for each component.
aggregate_hazard_list=[]
for component,per_component_hazard_dict in building_component_dict.items():
    sumval=0
    for hazard,rankval in per_component_hazard_dict.items():
        sumval=sumval+rankval #This just adds 'NaNs' to the sum, if do_vulnerability_ranking == False
        aggregate_hazard_list.append(hazard)
    building_component_dict[component]["total_hazard_sum"]=sumval #record the final sum value in dictionary entry

ranks=[]
for component in building_component_dict:
    ranks.append(building_component_dict[component]["total_hazard_sum"])
    
sortrank=sorted(ranks, reverse=True)
# %%
if do_vulnerability_ranking:
    print("\n")
    print("\nBased on your entries, I have tried to rank your building's components from MOST to LEAST vulnerable:\n")
    j = 0
    for i in range(len(sortrank)):
        if i+j < len(sortrank):
            flag = 0
            for component in building_component_dict:
                if building_component_dict[component]["total_hazard_sum"] == sortrank[i+j]:
                    if flag != 1:
                        print("  "+str(i+j+1)+".  "+component)
                    else:
                        print("  "+str(i+j+1)+". (tie)  " + component)
                        j += 1
                    flag = 1
    print("\nIt might make sense to focus most on the components nearer the top of this list during your building planning work.")

# %% 
# Rank hazards by # of times they are mentioned as component hazards.  Display top hazards.
l_sorted=Counter(aggregate_hazard_list).most_common()
max_len=min(3,len(l_sorted))
print("Based on these lists, the top climate hazards that impact the most components of building appear to be:\n")
for h in range(max_len):
    print("->"+l_sorted[h][0])
print("\nIt might make sense to focus most on these hazards during data gathering for your building planning work.\n")

input ("Press ENTER to continue")
print(screen_clear)


# %%

print("Based on the hazards that you identified as important to your building components, I've found some specific climate data resources for you.")
for h,r in l_sorted:
    if hazard_dict[h]["resource"]=="climatedata.ca":
        print("\nI've found some "+master_hazard_dict[h]["var_en"]+" information on ClimateData.ca for "+h.upper()+" at your location.")
        if yes_or_no("Would you like me to open a map in your web browser, where you can read more about "+master_hazard_dict[h]["var_en"]+ " and access data for your location for different future scenarios?"):
            url="https://climatedata.ca/explore/variable/?coords="+str(latitude)+","+str(longitude)+",12&geo-select=&var="+str(hazard_dict[h]["var"])+"&var-group="+str(hazard_dict[h]["group"])+"&mora=ann&rcp=rcp85&decade="+str(decade)+"s&sector="
            webbrowser.open(url,new=0,autoraise=False)
    if hazard_dict[h]["resource"]=="CRBCPI":
        print("\nI've found some information from the Climate-Resilient Buildings and Core Public Infrastructure (CRBCPI) project for "+h.upper()+", near your location, specifically, "+master_hazard_dict[h]["var_en"]+", for "+location+", around "+proximity+"km from your building site.")
        if yes_or_no("Would you like me to open the CRBCPI report section on "+master_hazard_dict[h]["var_en"]+", where you can read more about "+master_hazard_dict[h]["var_en"]+" projections, and get links to the actual data)?"):
            url=master_hazard_dict[h]["URL"]
            webbrowser.open(url,new=0,autoraise=False)
    elif hazard_dict[h]["resource"]=="":
        print("\nI've found some information for you to consider when assessing climate change impacts to "+h+" to your building.")
        if yes_or_no("Would you like me to open this material in a browser tab?"):
            url=master_hazard_dict[h]["URL"]
            webbrowser.open(url,new=0,autoraise=False       )     

        
#TODO: allow for multiple resource URLs
#TODO: Improve this closing guidance.

# %%

input("Press ENTER to continue")
print(screen_clear)

print("\n")
print("STEP 6: NEXT STEPS")
print("\n")

print("\n")
input("Let's summarize what you've done here - AND - what you still need to do to ensure your building's climate resiliency! (press ENTER to continue)\n")
input("1) You described your building's basics, including expected lifetime and major components... (press ENTER to continue)\n")
input("2) You identified some h present and future climate hazards for your region... (press ENTER to continue)\n")
input("3) You thought about which climate hazards could impact each of your building's components... (press ENTER to continue)\n")
input("4) You developed a summary that prioritized major hazards and identified some promising climate information for each one... (ENTER to continue)\n")
input("Your next tasks are: (ENTER to continue)\n")
input("5) Get this climate information and develop a tailored climate change summary report for your building... (ENTER to continue)\n")
input("6) Use this report to understand how the likelihood and severity of each hazard will change in the future... (ENTER to continue)\n")
input("7) Undertake impact, vulnerability or risk assessments for present and future conditions if you want to understand how these will change for each of your components over time due to climate change... (ENTER to continue)\n")
input("8) Consider developing adaptation plans and actions to ensure your building's resilience, now and in the future! (ENTER to continue)\n")

print("\n")
print("Well done, and good luck with using this climate information and training to increase your building's resilience to climate change!")
email_address=input("Enter your email address to receive a brief report that summarizes the results of this decision support tool!") #FYI
#TODO: generate an email or PDF-based send-out report.
input("When you're ready to say goodbye, press ENTER!")

print(screen_clear)
draw_stuff('wizard_end')
print ("POOF! ALL DONE")


#%%


    
