#Data Cleansing Code

#BeautifulSoup: Open local and http html files
# https://stackoverflow.com/questions/48935514/beautifulsoup-open-local-and-http-html-files

from bs4 import BeautifulSoup as bs


link = open("./html.html")
soup = bs(link.read(), "html.parser")

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

jobtitles = []

i = 0

for element in paragraphs:
    if(i > 5 and i < 500):
        #only collecting the p elements within a certain range
        #(only these p elements are actual job titles)
        el = element.get_text()
        jobtitles.append(el)
        
    i = i + 1 
    
print(jobtitles)

print("\n")