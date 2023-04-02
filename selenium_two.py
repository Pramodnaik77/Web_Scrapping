# importing all the required modules

from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
import csv
import sqlite3

#chromedriver for selenium
PATH = "D:\Downloads\chromedriver.exe"

#setting the webdriver for Chrome
driver = webdriver.Chrome(PATH)

#link to visit the website-"https://www.theverge.com/"
link = "https://www.theverge.com/"


#Establishing link 
driver.get(link)


#Find all the anchor tags within the website
a_tags = driver.find_elements(By.TAG_NAME,'a')


#Creating Lists to store URL's, HeadLine's , Author-Name's, Date's

Headline_list = []
Author_list = []
URL_list = []
Date_list = []


#Traversing within the anchor tags

for inner_a_tags in a_tags:

    #Finding class of the anchor tags
    a_class = inner_a_tags.get_attribute('class')

    #Matching class_name with the specific name with matched the HeadLine anchor tag Class
    if "group-hover" in a_class and inner_a_tags.text != None:

        #If match found Append it in HeadLine_list
        Headline_list.append(inner_a_tags.text)

        #Take URL from that anchor tag and append it to URL_list
        URL_list.append("https://www.theverge.com/"+inner_a_tags.get_attribute('href'))

    #Matching class_name with the specific name with matched the Author anchor tag class
    if "text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8" in a_class and inner_a_tags.text != None:

        #If match found Append it in Author_list
        Author_list.append(inner_a_tags.text)


#Obtaining all span tag for Date's

span_tags = driver.find_elements(By.TAG_NAME,"span")


#Traversing each sppans
for spans in span_tags:

    #Finding class of the span tags

    s_class = spans.get_attribute('class')

    #Matching class_name with the specific name with matched the Date anchor tag Class
    if "text-gray-63 dark:text-gray-94" in s_class and spans.text != None:

        #If match found Append it in Date_list
        Date_list.append(spans.text)


Date_list = Date_list[:len(Date_list)-2]


#After Scrapping Data from the website we store it in CSV and SQL Databases



# Saving articals in csv file

#Obtaining todays date to save csv file as ddmmyyyy
today = date.today()

d = ""
m = ""
y = ""
y,m,d = str(today).split('-')

#name is in the form ddmmyyyy
name = d+m+y+"_verge.csv"

#creating csv file
file = open(name,'w')


#creating a writer object
writ = csv.writer(file)


#Creating first row as Heading
writ.writerow(['ID','URL','HeadLine','Author','Date'])


#Travesring all 4 list and storing the date in csv as id,url,headline,author,date
for i in range(len(Headline_list)):
    writ.writerow([i,URL_list[i],Headline_list[i],Author_list[i],Date_list[i]])

#closing csv file
file.close()


#Storing data within SQL Database

#Creating Database using .connect()
m = sqlite3.connect('Web_Srcapped_Data.db')

#Creating cursor 
c = m.cursor()

# Create new table or append to already existing table
try:
    #creating new table name Verge_Data
    c.execute("""CREATE TABLE Verge_Data (
                ID INT PRIMARY KEY,
                URL TEXT,    
                HeadLine Text,
                Author Text,
                Date Text
                )
            """)
    

    # Table created and now Data storing initiallly as follows
    for i in range(len(Headline_list)):
        c.execute("INSERT INTO Verge_Data VALUES('{}','{}','{}','{}','{}')".format(i,URL_list[i],Headline_list[i],Author_list[i],Date_list[i]))

    #saving the changes
    m.commit()


except:
    #If table is already created we get data present in table
    c.execute("select * from Verge_Data")

    #find the length of already stored data to give new ID as it is the Primary Key (it should be unique)
    total_articals = len(c.fetchall()) + 1

    #Inserting data into table as id,url,headline,author,date

    for i in range(len(Headline_list)):
        c.execute("INSERT INTO Verge_Data VALUES('{}','{}','{}','{}','{}')".format(i+total_articals,URL_list[i],Headline_list[i],Author_list[i],Date_list[i]))
    m.commit()


#closing Database
m.close()

# print("DONE all")



