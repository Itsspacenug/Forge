from collections import defaultdict
from models import Section, TimeBlock

def get_all_time_block(schedule: list[Section]) -> list[TimeBlock]:
    blocks = []
    for section in schedule:
        blocks.extend(section.time_blocks)
    return blocks

def compactness_score(schedule: list[Section]) -> float:
    WORST_CASE = 480
    blocks = get_all_time_block(schedule)
    day_map = defaultdict(list)
    for tb in blocks:
        day_map[tb.day].append(tb)
        
    total_gap = 0
    for day in day_map:
        day_blocks = sorted(day_map[day], key=lambda x: x.start)
        for i in range(len(day_blocks) - 1):
            gap = day_blocks[i+1].start - day_blocks[i].end
            if gap > 0:
                total_gap += gap
        
    return 1 - min(total_gap/WORST_CASE, 1.0)

def time_of_day_score(schedule: list[Section]) -> float:
    EARLY_THRESHOLD = 540
    LATE_THRESHOLD = 1200
    WORST_CASE = 600
    
    early_penalty = 0
    late_penalty = 0
    for tb in get_all_time_block(schedule):
        if tb.start < EARLY_THRESHOLD:
            early_penalty += EARLY_THRESHOLD - tb.start
        if tb.end > LATE_THRESHOLD:
            late_penalty += tb.end - LATE_THRESHOLD
    
    combined = (early_penalty + late_penalty) / 2
    return 1 - min(combined / WORST_CASE, 1.0)

def day_spread_score(schedule: list[Section]) -> float:
    TARGET_DAYS = 3
    days = {tb.day for tb in get_all_time_block(schedule)}
    deviation = abs(len(days) - TARGET_DAYS)
    return 1 - min(deviation / 2, 1.0)

def day_length_score(schedule: list[Section]) -> float:
    TARGET = 210
    WORST_CASE = 180
    blocks = get_all_time_block(schedule)
    day_map = defaultdict(list)
    for tb in blocks:
        day_map[tb.day].append(tb)
        
    penalty = 0
    for day in day_map:
        day_blocks = sorted(day_map[day], key=lambda x: x.start)
        length = day_blocks[-1].end - day_blocks[0].start
        penalty += abs(length - TARGET)
    
    avg_penalty = penalty / len(day_map) if day_map else 0
    return 1 - min(avg_penalty / WORST_CASE, 1.0)

def lunch_score(schedule: list[Section]) -> float:
    LUNCH_START = 660
    LUNCH_END = 810
    WORST_CASE = 300
    blocks = get_all_time_block(schedule)
    day_map = defaultdict(list)
    for tb in blocks:
        day_map[tb.day].append(tb)
        
    penalty = 0
    for day, day_blocks in day_map.items():
        lunch_blocked = any(
            tb.start < LUNCH_END and tb.end > LUNCH_START
            for tb in day_blocks
        )
        if lunch_blocked:
            penalty += 60
            
    return 1 - min(penalty / WORST_CASE, 1.0)


def calculate_total_score(schedule : list[Section], weights: dict) -> int:
    
    return (
        weights.get("compactness", 0.0)*compactness_score(schedule)+
        weights.get("time_of_day", 0.0)*time_of_day_score(schedule)+
        weights.get("day_spread", 0.0)*day_spread_score(schedule)+
        weights.get("day_length", 0.0)*day_length_score(schedule)+
        weights.get("lunch_breaks", 0.0)*lunch_score(schedule)
    )
