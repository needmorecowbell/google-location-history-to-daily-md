# Google Takeout Location History: Create Daily Markdown Timeline



## Usage
- Enter in your output and location history directory in the top of the script, then run the file: `python create_daily_timeline.py`


## Requirements
- A google takeout export including location history
- python3

## Example output

**Filename:** 01-01-2022.md 

```markdown
---
tags: ['notes/daily']
---

# 01-01-2022 Daily Notes

## Associations
- 

-------
## Notes
- 

----- 
## References
1.


## Timeline

----
**Arrival**:: 8:01 am
**Departure**:: 10:01 am
**Duration**:: 2.0 hours, 0.0 minutes
       
**Place**:: Fake Shopping Center 
**Address**:: 123 Address St, Town, MI ZIPCODE, COUNTRY 
**Lat/Lon**:: xxxxxxxx, xxxxxxxx

----
**Arrival**:: 11:00 am
**Departure**:: 07:00 pm
**Duration**:: 8.0 hours, 0.0 minutes
       
**Place**:: 321 Address St
**Address**:: 321 Address St, Town, MI ZIPCODE, COUNTRY 
**Lat/Lon**:: xxxxxxxx, xxxxxxxx


```