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

def long_day_penalty(schedule: list[Section]) -> int:
    MAX_LENGTH_THRESHOLD = 240
    total_penalty = 0
    day_map = defaultdict(list)
    day_lengths = []

    blocks = get_all_time_block(schedule)
    for tb in blocks:
        day_map[tb.day].append(tb)
        
    for day in day_map:
        day_blocks = sorted(day_map[day], key = lambda x: x.start)
        day_lengths.append(day_blocks[-1].end - day_blocks[0].start)
        
    for length in day_lengths:
        total_penalty += max(0, length-MAX_LENGTH_THRESHOLD)
        
    return total_penalty

def short_day_penalty(schedule: list[Section]) -> int:
    MIN_LENGTH_THRESHOLD = 180
    total_penalty = 0
    day_map = defaultdict(list)
    day_lengths = []
    
    blocks = get_all_time_block(schedule)
    for tb in blocks:
        day_map[tb.day].append(tb)
        
    for day in day_map:
        day_blocks = sorted(day_map[day], key=lambda x: x.start)
        day_lengths.append(day_blocks[-1].end - day_blocks[0].start)
        
    for length in day_lengths:
        total_penalty += max(0, MIN_LENGTH_THRESHOLD-length)
        
    return total_penalty

def lunch_penalty(schedule: list[Section]) -> int:
    penalty = 0
    blocks_by_day = {}
    blocks = get_all_time_block(schedule)
    
    for tb in blocks:
        if tb.day not in blocks_by_day:
            blocks_by_day[tb.day] = []
        blocks_by_day[tb.day].append(tb)
    for day, day_blocks in blocks_by_day.items():
        for i in range(len(day_blocks)):
            block = day_blocks[i]
            if block.start > 660:
                penalty += block.start - 660
            if block.end < 810:
                penalty += 810 - block.end
    return -(penalty//5)


# Gaps between classes (different from lunch break?)
# Back-to-back classes

def calculate_total_score(schedule : list[Section], weights: dict) -> int:
    compact = compactness_preference(schedule)
    early = early_class_penalty(schedule)
    late = late_class_penalty(schedule)
    few = few_days_penalty(schedule)
    many = more_days_penalty(schedule)
    short = long_day_penalty(schedule)
    long = short_day_penalty(schedule)
    lunch = lunch_penalty(schedule)

    score = (weights.get("compactness",1.0)*compact)+(weights.get("early_morning", 1.0)*early)+(weights.get("late_evening", 1.0)*late)+(weights.get("more_days",1.0)*few)+(weights.get("few_days",1.0)*many)+(weights.get("short_days", 1.0)*short)+(weights.get("long_days",1.0)*long)+(weights.get("lunch_breaks",1.0)*lunch)
    

    return score

