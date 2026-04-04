from models import Section

def section_conflicts_with_schedule(section: Section, schedule: list[Section]) -> bool:
    """
    Checks if a section conflicts with any section in the schedule.
    Returns True if a conflict is found, False otherwise.
    """
    
    for scheduled_section in schedule:
        for existing_tb in scheduled_section.time_blocks:
            for new_tb in section.time_blocks:
                if new_tb.overlaps_with(existing_tb):
                    return True
    return False

def is_valid(section: Section) -> bool:
    DAY_START = 7*60
    DAY_END = 21*60
    
    for tb in section.time_blocks:
        if tb.start < DAY_START or tb.end > DAY_END:
            return False
        
    return True