# Getting timeline and save them as .json files. param 1: .csv file of user info to collect. param 2: path to save .json file to without the .json suffix. e.g. this code save matching user timelines to  /home/linda/matching/matching_BOTOMETER[uid].json for each uid accordingly.
python3 get_sample_and_matching_timeline.py xr2019_user_matched_seconds.csv /home/linda/matching/matching_BOTOMETER
python3 get_sample_and_matching_timeline.py matching_user_data_collection_xr2019.csv /home/linda/user/user_BOTOMETER

# Aggregating .json files to .csv. param 1: path of .json files. param 2: path to save .csv file to.
python3 second_stage_aggregation.py /home/linda/matching/matching_BOTOMETER/ /home/linda/user_aggregated_BOTOMETER.csv
python3 second_stage_aggregation_matching.py /home/linda/user/user_BOTOMETER/ /home/linda/matching_BOTOMETER.csv

