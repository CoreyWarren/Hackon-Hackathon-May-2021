#Data Cleansing Code
#Corey Warren II
#Team Basketball

#Why datacleansing2.py?
#Why the "2"?
#In v1, I ignored sub0, sub1, sub2, and sub3 labels in the HTML table data
#It turns out that these are actually very essential
#I need to find a way to organize this data into a way that is useful
# as well as meaningful.

#Resources:
#BeautifulSoup: Open local and http html files
# https://stackoverflow.com/questions/48935514/beautifulsoup-open-local-and-http-html-files
#Extracting "span" within a "div" of certain "class"
# https://stackoverflow.com/questions/41687476/using-beautiful-soup-to-find-specific-class


#////////CODE BEGIN/////////#

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
#sub0 and sub1 positions are 100% "job category" rather than "job title"
sub0_positions = []
sub1_positions = []
sub2_cat_positions = []
all_cat_positions = []


# parent id list, in order
# "Who is my parent?"
#initialize
#first sub0 = parent
#if find sub1, sub2, or sub3, WITHOUT
    #another same sub in front of it



    #if sub1: check for sub 0 parent position, record.
    #if sub2: check for sub 1 parent position, record.
    #if sub3: check for sub 2 parent position, record.
    




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
        if(i in sub0_positions or i in sub1_positions or i in sub2_cat_positions):
            #only collecting the p elements within a certain range
            #(only these p elements are actual job titles)
            
            el = element.get_text()
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


#write it all to file
filename = 'bravejob.txt'       #this is the filename of written file
f = open(filename, 'w')         #write mode
