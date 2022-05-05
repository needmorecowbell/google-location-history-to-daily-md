from typing import Dict, List, Tuple
#import pytz # for timezone conversions, may not be needed
import os
import datetime
import json


DAILY_PATH= "output/" # directory where Daily MD notes with timelines are stored (ie /home/user/Notes/Daily/)
LOCATION_DIR="Takeout/Location History/Semantic Location History/" # Download using takeout: https://takeout.google.com/ (only select location history)


def get_event_time_range(event: Dict) -> Tuple[datetime.datetime, datetime.datetime]:
    """
    Returns the start and end time of the given event. Supports a range of time formats.
    """

    start=None
    end=None
    try:
        start= datetime.datetime.strptime(event["placeVisit"]["duration"]["startTimestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        start= datetime.datetime.strptime(event["placeVisit"]["duration"]["startTimestamp"], "%Y-%m-%dT%H:%M:%SZ")
    
    try:
        end= datetime.datetime.strptime(event["placeVisit"]["duration"]["endTimestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        end= datetime.datetime.strptime(event["placeVisit"]["duration"]["endTimestamp"], "%Y-%m-%dT%H:%M:%SZ")
    
    return start, end

def load_daily_map(timeline: List[Dict])-> Dict:
    """
    Loads the daily map of the given timeline.

    :param timeline: list of event Dicts
    :return: dict of events organized by day
    """

    day_map= {}
    for event in timeline:
        if(event.get("placeVisit",None)):
            if(event["placeVisit"]["visitConfidence"] > 60):
                start, _ = get_event_time_range(event)
                if(day_map.get(start.strftime("%m-%d-$Y"),None)):
                    day_map[start.date().strftime("%m-%d-%Y")].append(event)
                else:
                    day_map[start.date().strftime("%m-%d-%Y")]= [event]

    return day_map

def has_timeline(fp: str) -> bool:
    """
    Checks if the timeline exists.

    :param fp: file path to the timeline
    :return: True if the timeline exists, False otherwise
    """
    if(os.path.exists(fp)): # check for existing file
        with open(fp, "r") as f:
            daily_md = f.readlines()
            return any("## Timeline" in line for line in daily_md)
    else:
        return False


def get_base_daily_md(day: str) -> str:
    """
    Returns the base daily markdown file.

    :param day: the day of the timeline
    :return: the barebones daily markdown file
    """
    return f"""
---
tags: ['notes/daily']
---

# {day} Daily Notes

## Associations
- 

-------
## Notes
- 

----- 
## References
1.

"""

def generate_timeline(timeline: List[Dict]) -> str:
    """
    Generates the timeline markdown.

    :param timeline: list of event Dicts
    :return: the markdown for the timeline
    """

    contents=""
    for event in timeline:
        start, end = get_event_time_range(event)
        hours, remainder = divmod((end-start).total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        contents+=f"""
----
**Arrival**:: {start.strftime('%I:%M %P')}
**Departure**:: {end.strftime('%I:%M %P')}
**Duration**:: {hours} hours, {minutes} minutes
       
**Place**:: {event["placeVisit"]["location"].get("name","unknown")} 
**Address**:: {event["placeVisit"]['location'].get("address","No address")} 
**Lat/Lon**:: {event["placeVisit"]['location'].get("latitudeE7",0)}, {event["placeVisit"]['location'].get("longitudeE7",0)}

"""



    return f"""
## Timeline
{contents}

"""

def add_timeline_to_md(timeline: List[Dict], day: str, fp: str) -> None:
    """
    Adds the timeline to the given file path.

    :param timeline: list of event Dicts
    :param fp: file path to the timeline
    :return: None
    """

    if(not os.path.exists(fp)): # if path doesn't exist, start with a new patterned file before adding timeline
        with open(fp, "w") as f:
            f.write(get_base_daily_md(day))

    timeline_block= generate_timeline(timeline)

    with open(fp, "a") as f:
        f.write(timeline_block)


if __name__ == "__main__":
    # iterate through all the files and directories in the location history folder
    for root, dirs, files in os.walk(LOCATION_DIR):
        for file in files:
            if(file.endswith(".json")):
                with open(os.path.join(root, file), "r") as f:
                    month_data = json.load(f)
                    day_map= load_daily_map(month_data["timelineObjects"]) # organize events by day
                    for day in sorted(day_map):
                        timeline_exists= has_timeline(DAILY_PATH+str(day)+".md")
                                    
                        if(not timeline_exists):
                            add_timeline_to_md(day_map[day], str(day), DAILY_PATH+str(day)+".md")
                            