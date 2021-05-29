#Data Cleansing Code
#v3

#Corey Warren II
#Team Basketball

#Resources:
#BeautifulSoup: Open local and http html files
# https://stackoverflow.com/questions/48935514/beautifulsoup-open-local-and-http-html-files
#Extracting "span" within a "div" of certain "class"
# https://stackoverflow.com/questions/41687476/using-beautiful-soup-to-find-specific-class


#////////CODE BEGIN/////////#

import csv
from bs4 import BeautifulSoup as bs

#the HTML file is from 
# https://www.bls.gov/cps/cpsaat11.htm
#I saved it as "only HTML" into the same folder
# as the .py code.


str1 = "hell"
int1 = 0
str1 = str1 + str(int1)
print(str1) #should print "hell0"


link = open("./html.html")
soup = bs(link.read(), "html.parser")

#make the html read-in nicer for data cleansing
soup.prettify()

#every occupation has 5 span values.

dataset = soup.find_all('span', class_="datavalue")

#initialize the value set
dataset_values = []

#grab the text data from the span elements from HTML, and put it into the value set.
for element in dataset:
    el = element.get_text()
    if(el == "-"):
        el = "-1"
    #remove commas
    if ',' in el:
        el = el.replace(',', '')
    float(el)
    dataset_values.append(el) 
    
print("\n")

print(dataset_values)
    
#get job titles
#p element type
#some p elements are not relevant
#can conditionally delete some p elements if:
# ->they do not contain sub0, sub1, sub2, or sub3 as class_ type

paragraphs = soup.find_all('p')

paragraphs_strings = []
jobtitles = []
job_categories = []
alljobs = []
parentID = []
#sub0 and sub1 positions are 100% "job category" rather than "job title"
sub0_positions = []
sub1_positions = []
sub2_cat_positions = []
all_cat_positions = []



    




i = 0
for element in paragraphs:
    if(i >= 6 and i < 600):
        #print(element)
        paragraphs_strings.append(str(element))
        #print("paragraphs_strings[i]=", paragraphs_strings[i])
        mypos = paragraphs_strings[i].find('"sub"')
        #print("mypos = ", mypos)
        #cut out the subX value from the string.
        paragraphs_strings[i] = paragraphs_strings[i][mypos+11:]
        paragraphs_strings[i] = paragraphs_strings[i][:4]
        if(i % 12 != 0):
            print(paragraphs_strings[i], ",", end = '')
        else:
            print(paragraphs_strings[i], ",")
    else:
        paragraphs_strings.append(str(0))
    i = i + 1
print("\n")

#now record the positions of any job categories.
i = 0
for element in paragraphs_strings:
    if(paragraphs_strings[i] == "sub0"):
        sub0_positions.append(i)
    elif(paragraphs_strings[i] == "sub1"):
        sub1_positions.append(i)
    elif(paragraphs_strings[i] == "sub2" and paragraphs_strings[i+1] == "sub3"):
        sub2_cat_positions.append(i)
    i = i + 1

#Now record the actual job categories
# and job titles into a list.
i=0
for element in paragraphs:
    if(i >= 6 and i < 600):
        el = element.get_text()
        alljobs.append(el)
        if(i in sub0_positions or i in sub1_positions or i in sub2_cat_positions):
            #only collecting the p elements within a certain range
            #(only these p elements are actual job titles)
            
            
            job_categories.append(el)
            
            if(i in sub0_positions):
                print("Sub0 case.")
                
            if(i in sub1_positions):
                print("Sub1 case.")
                
            if(i in sub2_cat_positions):
                print("Sub2 category case.")
                
            print(i)
                
        else:
            el = element.get_text()
            jobtitles.append(el)
    i = i + 1 

for el in sub0_positions:
    all_cat_positions.append(el)
for el in sub1_positions:
    all_cat_positions.append(el)
for el in sub2_cat_positions:
    all_cat_positions.append(el)
    
all_cat_positions.sort()

#new possible solution:
#very complex problem, actually:
# all sub0, sub1, sub2, and sub3 data should be relatively neatly organized.
# all of these data collections should be uniform so a single function
#   can load each of them in without needing further accomodation
# all sub1, sub2, and sub3 data should know which category they are a part of.
#   this is the most difficult part on top of everything!


#solution sketch:
#EVERY 5 DATA POINTS CORRESPONDS TO SOME VALUES IN ANOTHER LIST
#THE OTHER LIST HAS 4 DATA POINTS PER SET OF 5 VALUE POINTS IN THIS LIST
#BY TRAVERSING BOTH LISTS AT ONCE
#YOU CAN GET ALL CATEGORIES RELEVANT TO THE DATA AT HAND
#INCLUDING WHICH CATEGEORIES THE SUBCATEGORIES ARE A PART OF

print("\n")
print("Job Titles:", jobtitles)
print("\n")
print("Job Categories: ", job_categories)
print("\n")
print("Positions where a job category* is in data: ", all_cat_positions)
print("Positions where a job category* is in data: ", sub0_positions, sub1_positions, sub2_cat_positions)
print()
print("*Note: Job Category = 'Service'")
print("Meanwhile: Job Title = 'Clerk,' which is a subcategory of 'Service.'")
print("\n")



# parent id list, in order
# "Who is my parent?"
#initialize
#first sub0 = parent
#if find sub1, sub2, or sub3, WITHOUT


#first parent ever is the sixth node
# we note this manually.
# this stops the code from making node 6
# its own parent.
# (reminder: node 6 is the first real data node.)
last_parent = 6
current_sub = 0
i = 0

for element in paragraphs_strings:
    #another same sub in front of it
    mysub = ""
    prevsub = ""
    if(i>=6 and i <600):
        try:
            mysub = paragraphs_strings[i][3:]
            mysub = mysub.strip()
            #print(mysub, end= '...')
        except:
            print("invalid operation, exception type 1.")
            i = i + 1
            continue
            
        try:
            mysub_int = int(mysub, base = 10)
            #print(mysub_int, end= '...')
        except:
            print("no mysub, exception type 2.")
            i = i + 1
            continue
        
        try:
            prevsub = paragraphs_strings[i-1][3:]
            prevsub = prevsub.strip()
            #print("prevsub:", prevsub, end = '')
        except:
            print("invalid operation, exception type 3. prevsub")
            parentID.append(last_parent)
            i = i + 1
            continue
            
        try:
            prevsub_int = int(prevsub, base = 10)
            #print(prevsub_int, end= '...')
        except:
            print("no prevsub, exception type 4.")
            i = i + 1
            continue
        if(mysub_int == 0):
            #sub0 nodes will have parent -1 (it has no parent!)
            parentID.append(-1)
        elif(mysub_int > prevsub_int):
            #ex: this is sub1 following sub0 last iteration...
            # answer: this node's parent is the last node.
            # do: record position of last node as parent ID
            last_parent = i-1
            parentID.append(i-1)
        elif(mysub_int < prevsub_int):
            #ex: this is sub 1 following sub2 last iteration
            # answer: this is a new parent!
            # do: record this position as parent ID
            last_parent = i
            parentID.append(i)
        else:
            # but if the two values are the same, the parent
            # will not change this round.
            parentID.append(last_parent)
    else:
        #cases with no data will NOT be recorded,
        #we will not even write these nodes down in the csv.
        #do: mark parent as -2 for later removal during file write.
        parentID.append(-2)
    
    i = i + 1

#sanity check on parent IDs
print(parentID)


#write it all to file

filename = 'database.csv'       #this is the filename of written file
f = open(filename, 'w')         #write mode

header = ['myID', 'Occupation', 'Total Employed', 'Women Percent', 'White Percent',\
 'Black Or African American Percent', 'Asian Percent', 'Hispanic Or Latino Percent',\
 'ParentID']

wr = csv.DictWriter(f, fieldnames = fieldnames)

wr.writeheader()




i = 0
cati = 0
titlei = 0
for text in paragraphs:
    
    if(parentID[i] != -2):
        wr.writerow(i)
        if(i in all_cat_positions):
            wr.writerow(job_categories[cati])
            cati = cati + 1
        else:
            wr.writerow(jobtitles[titlei])
            titlei = titlei + 1
        
    
    
    
    
        f.write(parentID[i])
        
    i = i + 1


f.close()

print("Done.")

