import os
import json
import pandas as pd
import botometer


p_in="/home/rproot/botometer/data/"
p_out="/home/rproot/botometer/data/boto_out/"

all_users=pd.read_csv(p_in+"k2_users_screennames.csv")


rapidapi_key = "3028a43109msh5fa8623a499002dp14b73cjsnd68607e9d83f"
twitter_app_auth = {
    'consumer_key': '1w9kQ5nBaPbYLb7euUsCprAhU',
    'consumer_secret': 'Toa2Zq9girGmtPpnNbYegn9k4uYEeoV3yMf5LNFLobyh2bpVc9',
    'access_token': '443619917-XLzauvkNiYwMhZcug3bbQ2RGXTvyqvQ2JbYq6qxz',
    'access_token_secret': 'TTqGTLFhWpY8ItCx0hJr2ZEdd8qypMfmmkbFgYKmVMcVX',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)


count=0
errors=[]
R=[]
for userid in list(all_users['id']):
    count+=1
    if len(R)%1000==0:
        print(len(R))
    if count%5000==0:
        print(count)
        json_object = json.dumps(R)
        with open(p_out+"missing_sampled_bots_botometer_"+str(count)+".json", "w") as outfile:
            outfile.write(json_object)
            R=[]
    try:
        result = bom.check_account(userid)
        R.append(result)
    except:
        errors.append(userid)
json_object = json.dumps(R)
with open(p_out+"missing_sampled_bots_botometer_"+str(count)+".json", "w") as outfile:
    outfile.write(json_object)
pd.DataFrame(errors).to_csv(p_out+'k2_users.csv')