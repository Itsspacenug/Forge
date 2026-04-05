from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fake_data import load_courses
from generator import find_all_schedules
from optimizer import calculate_total_score

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
    course_codes: list[str]
    preferences: dict[str, float]

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
        
    sorted_schedules_score = sorted(
        all_possible_schedules,
        key=lambda schedule: calculate_total_score(schedule, request.preferences),
        reverse=True
    )

    return {
    "results": [
        {
            "rank": rank,
            "score": calculate_total_score(schedule, request.preferences),
            "sections": [
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
        }
        for rank, schedule in enumerate(sorted_schedules_score[:3], start=1)
    ],
    "message": "Success"
}