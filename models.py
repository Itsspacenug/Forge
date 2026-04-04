from dataclasses import dataclass

@dataclass
class TimeBlock:
    day: str
    start: int  # minutes from midnight
    end: int    # minutes from midnight

    def overlaps_with(self, other: 'TimeBlock') -> bool:
        """
        Check if this time block overlaps with another.
        Two blocks overlap if they are on the same day and their time ranges intersect.
        """
        if self.day != other.day:
            return False
        # Overlap occurs if the start of one is before the end of the other, and vice versa.
        return self.start < other.end and other.start < self.end


@dataclass
class Section:
    course_reg_num: str
    section_id: str
    course_code: str
    department: str
    time_blocks: list[TimeBlock]


@dataclass
class Course:
    name: str
    course_code: str
    department: str
    sections: list[Section]