import pandas as pd 


# cleaned csv

file = pd.read_csv('./results/log_data.csv')

#top 10 ips 
rhost = file["rhost"].value_counts().head(10)
print (rhost)

#top 10 users
user = file["user"].value_counts().head(10)
print (user)

# Hours with the most attack occourrencies 
