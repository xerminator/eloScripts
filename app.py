# import json
# import os
# from datetime import datetime

# def find_dead_players_before_event(events, event_type):
#     deaths = set()
#     first_event_time = None
#     death_found = False

#     for event in events:
#         if event["Event"] == "Death":
#             dead_player = event["Name"]
#             if dead_player not in deaths:
#                 deaths.add(dead_player)
#                 death_found = True
#         elif death_found:
#             if event["Event"] == event_type:
#                 first_event_time = datetime.strptime(event["Time"], "%m/%d/%Y %H:%M:%S")
#                 break

#     return list(deaths), first_event_time

# def process_json_file(file_path):
#     with open(file_path, 'r') as file:
#         json_data = json.load(file)
#         deaths_before_meeting, meeting_time = find_dead_players_before_event(json_data, "MeetingStart")
#         deaths_before_vote, vote_time = find_dead_players_before_event(json_data, "PlayerVote")

#         if meeting_time and (not vote_time or meeting_time < vote_time):
#             print(f"Players who died before the first MeetingStart in {file_path}: {deaths_before_meeting}")
#         elif vote_time and (not meeting_time or vote_time < meeting_time):
#             print(f"Players who died before the first PlayerVote in {file_path}: {deaths_before_vote}")
#         else:
#             if deaths_before_meeting or deaths_before_vote:
#                 print(f"Players who died before the end of events in {file_path}: {list(set(deaths_before_meeting + deaths_before_vote))}")
#             else:
#                 print(f"No players died before the end of events in {file_path}")

# def process_json_files(folder_path):
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".json"):
#             file_path = os.path.join(folder_path, filename)
#             print(f"Processing file: {file_path}")
#             process_json_file(file_path)
#             print()

# # Folder path containing JSON files
# folder_path = './events'

# # Process JSON files in the folder
# process_json_files(folder_path)

import json
import os
from datetime import datetime

def find_dead_players_before_event(events, event_type):
    deaths = set()
    first_event_time = None
    death_found = False

    for event in events:
        if event["Event"] == "Death":
            dead_player = event["Name"]
            if dead_player not in deaths:
                deaths.add(dead_player)
                death_found = True
        elif death_found:
            if event["Event"] == event_type:
                first_event_time = datetime.strptime(event["Time"], "%m/%d/%Y %H:%M:%S")
                break

    return list(deaths), first_event_time

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        deaths_before_meeting, meeting_time = find_dead_players_before_event(json_data, "MeetingStart")
        deaths_before_vote, vote_time = find_dead_players_before_event(json_data, "PlayerVote")
        deaths_before_report, report_time = find_dead_players_before_event(json_data, "BodyReport")

        if meeting_time and (not vote_time or meeting_time < vote_time):
            print(f"Players who died before the first MeetingStart in {file_path}: {deaths_before_meeting}")
        elif vote_time and (not meeting_time or vote_time < meeting_time):
            print(f"Players who died before the first PlayerVote in {file_path}: {deaths_before_vote}")
        elif report_time:
            print(f"Players who died before the first report in {file_path}: {deaths_before_report}")
        else:
            if deaths_before_meeting or deaths_before_vote or deaths_before_report:
                print(f"Players who died before the end of events in {file_path}: {list(set(deaths_before_meeting + deaths_before_vote + deaths_before_report))}")
            else:
                print(f"No players died before the end of events in {file_path}")
        return list(set(deaths_before_meeting + deaths_before_vote + deaths_before_report))

def process_json_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")
            process_json_file(file_path)
            #print()

# Folder path containing JSON files
folder_path = './events'

# Process JSON files in the folder
process_json_files(folder_path)
