from collections import defaultdict
from models import Section, TimeBlock

def get_all_time_block(schedule: list[Section]) -> list[TimeBlock]:
    blocks = []
    for section in schedule:
        blocks.extend(section.time_blocks)
    return blocks

def compactness_preference(schedule: list[Section]) -> int:
    blocks = get_all_time_block(schedule)
    day_map = defaultdict(list)
    for tb in blocks:
        day_map[tb.day].append(tb)
        
    total_gap_time = 0
    
    for day in day_map:
        day_blocks = sorted(day_map[day], key = lambda x: x.start)
        for i in range(len(day_blocks) - 1):
            current_end = day_blocks[i].end
            next_start = day_blocks[i+1].start
            
            gap = next_start - current_end
            if gap > 0:
                total_gap_time += gap
                
    return total_gap_time

def early_class_penalty(schedule: list[Section]) -> int:
    EARLY_THRESHOLD = 540
    total_penalty = 0
    
    blocks = get_all_time_block(schedule)
    for tb in blocks:
        if tb.start < EARLY_THRESHOLD:
            total_penalty += (EARLY_THRESHOLD - tb.start)
    
    return total_penalty

def late_class_penalty(schedule: list[Section]) -> int:
    LATE_THRESHOLD = 1200
    total_penalty = 0
    
    blocks = get_all_time_block(schedule)
    for tb in blocks:
        if tb.end > LATE_THRESHOLD:
            total_penalty += (tb.end - LATE_THRESHOLD)
    
    return total_penalty

def few_days_penalty(schedule: list[Section]) -> int:
    MAXIMUM_DAYS = 5
    days = []
    
    blocks = get_all_time_block(schedule)
    for tb in blocks:
        if tb.day not in days:
            days.append(tb.day)
            
    return MAXIMUM_DAYS-len(days)

def more_days_penalty(schedule: list[Section]) -> int:
    MINIMUM_DAYS = 2
    days = []
    
    blocks = get_all_time_block(schedule)
    for tb in blocks:
        if tb.day not in days:
            days.append(tb.day)
            
    return max(0, len(days)-MINIMUM_DAYS)


# Long days
# short days
# lunch break preservation
# Gaps between classes (different from lunch break?)
# Back-to-back classes

def calculate_total_score(schedule : list[Section], weights: dict) -> int:
    compact = compactness_preference(schedule)
    early = early_class_penalty(schedule)
    late = late_class_penalty(schedule)
    few = few_days_penalty(schedule)
    many = more_days_penalty(schedule)

    score = (weights.get("compactness",1.0)*compact)+(weights.get("early_morning", 1.0)*early)+(weights.get("late_evening", 1.0)*late)+(weights.get("more_days",1.0)*few)+(weights.get("few_days",1.0)*many)

    return score

