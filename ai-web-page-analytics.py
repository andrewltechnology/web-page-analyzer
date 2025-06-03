#Automatic Feature Detection For Web Page Analytics Bouce Rate Evaluation
#This is a script that automatically detects features with AI NLP
#and analyzes website visitor data to detect underperforming pages


import spacy
import pandas as pd
import pprint
import sys

#Load spaCy md model
ai_word =spacy.load('en_core_web_md')



#intitialize tokens 
region_token=ai_word('region')
city_token=ai_word('city')
page_url_token=ai_word('page url')
visit_url=ai_word('vist url') 
time_token=ai_word('time')

#Define a function to take in the csv file
def csv_input(file):
    visits = pd.read_csv(file)
    return visits





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

    
    time_header_found = 0
    for header in visits.columns:
        # #organize each header into a list of tokens 
        header_token=ai_word(header.lower())
        if 'region' in header.lower() or 'city' in header.lower():
            region=visits[header]
           
        else:
            if region_token.similarity(header_token) >= .80 or  city_token.similarity(header_token) >= .80:
                #Check spaCy for 80% similarity in header and add to location variable 
                region=visits[header]
         
        if 'page url' in header.lower() or 'visit url' in header.lower() :
            url=visits[header]
            
        else:
            if page_url_token.similarity(header_token) >= .80 or  visit_url.similarity(header_token) >= .80:
                #Check spaCy for  80% similarity in header and add to url variable
                url=visits[header]
                
        if 'time' in header.lower():
            time=visits[header]
            

        else:
            split_words=header.split(" ")
            for i in split_words:
                iterable_token =ai_word(i.lower())[0]
                #Check spaCy for  80% similarity in header and add to time variable 
                if time_token.similarity(iterable_token) >= .80:
                    time_header_found+=1
            if time_header_found>1:
                time=visits[header]

                
                    
    transformed = pd.concat([time, url,region], axis=1)
    avg_time = time.mean()
    return (avg_time, transformed)
  
                
    

#Define a function to determine if each visited page is under performing 
def performance(ave,perform):

    #get average of time on page
    average_time_spent = ave

    #Define a dictionary to hold lists of under performing page urls
    check = { 'Under Performing': [],
        'Average performance time': average_time_spent, 
        'Good Performance': [], 
        }
    
    


    for index, row in perform.iterrows():
        if row.iloc[0] < check['Average performance time']:
            check['Under Performing'].append(row.iloc[1])
        else:
            if row.iloc[0] > check['Average performance time']:
                    check['Good Performance'].append(row.iloc[1])
    pprint.pprint(check)
    



if __name__ == "__main__":
    import sys
    if len(sys.argv)< 2:
        print("Use this format: python file.py fullfile_path")
        sys.exit(1)


file_path= sys.argv[1]
visits = csv_input(file_path)
ave,perform = extract(visits)
page_results=performance(ave,perform)
print(performance(page_results))