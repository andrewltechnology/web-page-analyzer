#Automatic Feature Detection For Web Page Analytics Bouce Rate Evaluation
#This is a script that automatically detects features with AI NLP algorithm
#and analyzes website visitor data to detect underperforming pages


import spacy
import pandas as pd

#Load spaCy English md modeed
ai_word =spacy.load('en_core_web_md')

#Initialize variables for script for feature extraction and dataframes
location=''
time=''
url=''
region_token=ai_word('region')
city_token=ai_word('city')
page_url_token=ai_word('page url')
visit_url=ai_word('vist url') 
time=ai_word('time')
df =''

#Define a function to take in the csv file
def csv_input(file):
    visits = pd.read_csv(file)
    extract(visits)


#Define a function to detect and extract features
'''
    AI Similarity feature detection:
    
    If one of the features is city/region, spaCy is used to detect correct feature fitting 80% similarity
    threshold

    If one of the features is page url or visit url, spaCy is used to detect correct feature fitting 80% similarity
    threshold


    If one of the features is time, spaCy is used to detect correct feature fitting 80% similarity
    threshold

'''
def extract(visits):
#automatically detect features corresponding to visior locatio, page visited, and time spent on page
    for header in visits.columns:
        if 'region' in header or 'city' in header:
            location = header
        else:
            if region_token.similarity(header) >= .80 or  city_token.similarity(header) >= .80:
                #Use spaCy to find word that has atleast 80% word similarity to location variables
                location=header
                
        if 'page url' in header or 'visit url' in header:
            url = header
        else:
            if page_url_token.similarity(header) >= .80 or  visit_url.similarity(header) >= .80:
                #Use spaCy to find word that has atleast 80% word similarity to url variable
                location=header
                
        if 'time' in header:
            time=header
        else:
            if time.similarity(header) >= .80:  
                #Use spaCy to find word that has atleast 80% word similarity to time on page variable
                time=header
                
    
    #Place extracted features in new dataframe
    df = pd.concat([location, time, url], axis=1)
    average(df)
    
   
#Define a function get the average time spent from the data frame
def average(df):
    average_time_spent = df[time].mean()
    performance(average_time_spent)

#Define a function to determine if each visited page is under performing 
def performance(average_time_spent):
    check['average_performance'] = average_time_spent

    #Define a dictionary to hold lists of under performing page urls
    check = { 'under_performing': [],
              'average_performance': '', 
              'good_performance': [], 
             }
    
    for index, row in df.iterrows():
        if row['time'] < average_time_spent:
            check['under_performing']=row['url']
        else:
            if row['time'] > average_time_spent:
                    check['good_performance']=row['url']

    #Print the results
    print("Under performing pages: " + check['under_performing'] + " \n Good performing pages: " + check['good_performance'])


