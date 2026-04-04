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

if __name__ == "__main__":
    from models import TimeBlock
 
    tb1 = TimeBlock(day=0, start=780, end=840)
    tb2 = TimeBlock(day=0, start=825, end=900)
    
    sec_a = Section("CRN1", "S1", "CSCI128", "CS", [tb1])
    sec_b = Section("CRN2", "S2", "MATH111", "MATH", [tb2])
    
    my_schedule = [sec_a]
    has_conflict = section_conflicts_with_schedule(sec_b, my_schedule)
    if has_conflict:
        print("Conflict detected between sec_b and my_schedule.")
    else:
        print("No conflict detected between sec_b and my_schedule.")
        
def is_valid(section: Section) -> bool:
    DAY_START = 7*60
    DAY_END = 14*60
    
    for tb in section.time_blocks:
        if tb.start < DAY_START or tb.end > DAY_END:
            return False
        
    return True