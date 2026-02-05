import pandas as pd 


# cleaned csv

file = pd.read_csv('./results/log_data.csv')

# ==========================================
# SECTION : Findings  
# ==========================================

#top 10 ips 
rhost = file["rhost"].value_counts().head(10)


#top 10 users
user = file["user"].value_counts().head(10)



# ==========================================
# SECTION : Brute-force attack detection
# ==========================================

# Brute-force attack detection
 
 # Get the rhost collum and filter out the null values   
filtered = file.dropna(subset=["rhost"])

# New column with floor minutes 
time = "2026 " + filtered["time"]
formated_date = pd.to_datetime(time, format="%Y %b %d %H:%M:%S")
floor_minutes =(formated_date.dt.floor('min'))

filtered.insert(1, 'floor_minutes', floor_minutes)

print(filtered.head(3)) 
