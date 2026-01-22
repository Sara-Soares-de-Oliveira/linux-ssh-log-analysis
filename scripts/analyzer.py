import re
from datetime import datetime
import csv

# Read the file 
file = open('./data/cleaned_logs.log', 'r') 

# Idea: use patterns to extract the infos (regex)

data_list= []

date_pattern = r'\b[A-Z][a-z]{2}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}\b' 
rhost_pattern = r'(?<=rhost=)\S+'
user_pattern = r'(?<=user[ ]|user=)\S+'

for key in file: 
        
        match = re.search (date_pattern, key)
        rhost_match = re.search (rhost_pattern, key)
        user_match = re.search (user_pattern, key)
        
        if match: 
                timestamp = match.group()
        else:
                timestamp = None
        if rhost_match: 
                rhost = rhost_match.group()        
        else: 
                rhost = None   
                     
        if user_match: 
                user = user_match.group()
        else: 
                user = None
        
        data_dict = {
                'time': timestamp,
            'rhost': rhost,
            'user': user,
            'raw_line': key.rstrip()
            }
        data_list.append(data_dict)       
                        
#Putting all into a csv file

with open ('results/log_data.csv', 'w',encoding='utf-8', newline='') as csvfile: 
        fieldnames = ['time','rhost','user','raw_line']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(data_list)    



