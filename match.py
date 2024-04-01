import json, os
from datetime import datetime

events_json = ""
match_json = ""
players_died_before_meeting = None
players_died_before_vote = None

def load_events_from_json(json):
    events = []
    for event in json:
        events.append(event)
    return events

def find_first_event_after_death(events, death_time, event_types):
    earliest_time = None
    for event in events:
        event_time = datetime.strptime(event['Time'], "%m/%d/%Y %H:%M:%S")
        if event_time > death_time and event['Event'] in event_types:
            if earliest_time is None or event_time < earliest_time:
                earliest_time = event_time
    return earliest_time

def find_players_died_before_time(events, time):
    deaths = set()
    for event in events:
        if event['Event'] == "Death" and datetime.strptime(event["Time"], "%m/%d/%Y %H:%M:%S") < time:
            deaths.add(event['Name'])
    return deaths

