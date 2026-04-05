from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from fake_data import load_courses
from generator import find_all_schedules
from optimizer import calculate_total_score
import re

COURSES = load_courses()

# Create the FastAPI app instance
app = FastAPI()

#Allows the frontend on port 5173 to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defines the format of the data that we expect to in the POST request body
# Pydantic validates it automatically and if frontend sends wrong data, Pydantic errors cleanly
class OptimizeRequests(BaseModel):
    course_codes: list[str] = Field(..., min_items = 1, max_items=10)
    preferences: dict[str, float]
    
    @field_validator('course_codes')
    @classmethod
    def validate_and_format(cls, v: list[str]) -> list[str]:
        pattern = re.compile(r"^[a-zA-Z]{3,4}\d{3}$")
        return [code.upper() for code in v if pattern.match(code) or exec('raise ValueError(...)')]

@app.get("/courses")
def get_courses():
    return[
        {
            "course_code": classes.course_code,
            "name": classes.name,
            "sections": [
                {
                "section_id": section.section_id,
                "time_blocks": [
                    {
                        "day": tb.day,
                        "start": tb.start,
                        "end": tb.end
                    }
                    for tb in section.time_blocks
                ]
            }
            for section in classes.sections
            ],
            "department": classes.department,


        }
        for classes in COURSES
    ]

@app.post("/optimize")
def run_optimize(request: OptimizeRequests):
    valid_codes = {c.course_code for c in COURSES}
    
    invalid_requests = [code for code in request.course_codes if code not in valid_codes]
    
    if invalid_requests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Some course codes were not found in the system.",
                "invalid_codes": invalid_requests
            }
        )
    
    filtered_courses = [c for c in COURSES if c.course_code in request.course_codes] #Filter all coursese that the user has chosen from requests
    
    if not filtered_courses:
        return {"results": [], "message": "No matching courses found."}
    
    all_possible_schedules = find_all_schedules(filtered_courses) # finds all permiatations from the filtered courses
    #calculates the score of each possible schedule based on the users request of preferences and ranks it from highest to lowest score
    
    if not all_possible_schedules:
        return {
            "results": [],
            "message": "No valid schedules found due to time conflicts. Try removing a course."
        }
    
    scored_schedules = [
        (calculate_total_score(s, request.preferences), s)
        for s in all_possible_schedules
    ]
    
    scored_schedules.sort(key=lambda x: x[0], reverse=True)
    
    results = []
    for rank, (score, schedule) in enumerate(scored_schedules[:3], start=1):
        formatted_section = [
            {
                "course_reg_num": s.course_reg_num,
                "course_code": s.course_code,
                "section_id": s.section_id,
                "time_blocks": [
                    {"day": tb.day, "start": tb.start, "end": tb.end}
                    for tb in s.time_blocks
                ]
            }
            for s in schedule
        ]
        
        results.append({
            "rank": rank,
            "score": score,
            "sections": formatted_section
        })
    return {
        "results": results,
        "message": "Success"
    }

