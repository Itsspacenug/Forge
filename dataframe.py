import pandas as pd
import numpy as np
import json
import duckdb
from sample_data import COURSES 


with open('mines_catalog.json', 'r') as f:
    data = json.load(f)
df = pd.DataFrame(data)


# Uses a lambda to remove the specific name from each corresponding row
df['name'] = df.apply(lambda x: x['name'].replace(x['code'] + '.', '').strip(), axis=1)
df['name'] = df.apply(lambda x: x['name'].replace(x['code'] + '.', '').strip(), axis=1)


query = """
SELECT
    CONCAT(SUBSTRING(code, 1, 4), ' ', SUBSTRING(code, 5)) as code,
    split_part(name, '.', 1) AS title,
    regexp_extract(name, '(\d+[.-]\d+)') AS credithours,
    prereqs,
    coreqs

FROM df
"""

df_split = duckdb.query(query).to_df()

df_split = df_split.replace('None', np.nan, inplace=True)

coursedf = df_split
#print(coursedf)

course_rows = []
section_rows = []
timeblock_rows = []

# Using a set to keep track of unique time patterns to avoid duplicates
seen_timeblocks = {}

for course in COURSES:
    for section in course.sections:
        # 1. df_courses: Info about the class itself
        course_rows.append({
            "crn": section.course_reg_num,
            "course_code": f"{course.department} {course.course_code}",
            "course_name": course.name
        })

        for block in section.time_blocks:
            # Create a unique key based on the day/start/end
            tb_key = (block.day, block.start, block.end)
            
            # Generate a consistent ID for this specific time slot
            if tb_key not in seen_timeblocks:
                tb_id = len(seen_timeblocks) + 1 # Simple integer ID
                seen_timeblocks[tb_key] = tb_id
                
                # 2. df_timeblocks: Purely time data (No course info!)
                timeblock_rows.append({
                    "timeblock_id": tb_id,
                    "day": block.day,
                    "start": block.start,
                    "end": block.end
                })
            
            # 3. df_sections: The bridge linking CRN to TimeBlock IDs
            section_rows.append({
                "crn": section.course_reg_num,
                "section_id": section.section_id,
                "timeblock_id": seen_timeblocks[tb_key]
            })


# Convert to DataFrames
inputdf = pd.DataFrame(course_rows).drop_duplicates()
sectiondf = pd.DataFrame(section_rows)
timeblockdf = pd.DataFrame(timeblock_rows)


# Manual error cleanup
inputdf.loc[inputdf['crn'] == '80643', 'course_name'] = 'COMPUTATIONAL METHODS FOR DIFFERENTIAL EQUATIONS'
inputdf.loc[inputdf['crn'] == '80643', 'course_code'] = 'MATH 408'

# query = "SELECT * 
# FROM inputdf
# JOIN coursedf ON inputdf.course_code = coursedf.code
# JOIN sectiondf ON inputdf.crn = sectiondf.crn
# JOIN timeblockdf ON sectiondf.timeblock_id = timeblockdf.timeblock_id"


# query = "SELECT * 
# FROM coursedf
# JOIN sectiondf ON CONCAT(SUBSTRING(coursedf.code, 1, 3), ' ', SUBSTRING(coursedf.code, 4)) = sectiondf.course_code
# JOIN timeblockdf ON sectiondf.timeblock_id = timeblockdf.timeblock_id"


sectiondf.info()
timeblockdf.info()
inputdf.info()


