from collections import defaultdict
from models import Section, TimeBlock

def get_all_time_block(schedule: list[Section]) -> list[TimeBlock]:
    blocks = []
    for section in schedule:
        blocks.extend(section.time_blocks)
    return blocks

def compactness_score(schedule: list[Section]) -> int:
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
                
    return -total_gap_time

def early_class_penalty(schedule: list[Section]) -> int:
    EARLY_THRESHOLD = 540
    total_penalty = 0
    
    blocks = get_all_time_block(schedule)
    for tb in blocks:
        if tb.start < EARLY_THRESHOLD:
            total_penalty += (EARLY_THRESHOLD - tb.start)
    
    return -total_penalty
