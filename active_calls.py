from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import pandas as pd

#loading and parsing webpage data
page = urlopen('https://www1.cityoforlando.net/opd/activecalls/activecadpolice.xml')
bsObj = BeautifulSoup(page, "xml")

#identifying the XML tags holding the desired values 
dates = bsObj.findAll("DATE")
descriptions = bsObj.findAll("DESC")
locations = bsObj.findAll("LOCATION")

#creating empty lists to hold string values of the XML data
allDates = []
allDescs = []
allLocs = []

#parsing data from the XML tags and populating the empty lists
def extract(tag, empty_list):
    for x in tag:
        string = x.get_text()
        empty_list.append(string)
        

extract(dates, allDates)
extract(descriptions, allDescs)
extract(locations, allLocs)


#creating a dictionary from the lists; converting the dictionary to a dataframe
data = {'Date': allDates, 'Description': allDescs, 'Location': allLocs}
df = pd.DataFrame(data)

#export the dataframe to a csv file
df.to_csv('pdcalls.csv')

####### Everything beyond this point is for adding and filtering new data to the existing csv #######

edit = pd.read_csv('pdcalls.csv')

#drop index number column; index will be added back when final dataframe is exported
edit = edit.drop(columns = [edit.columns[0]])

#combining new and existing data into one dataframe
edit = edit.append(df, ignore_index = True)

#filtering to drop duplicate entries
final = edit.drop_duplicates()

#overwrite the original csv file
final.to_csv('pdcalls.csv')




