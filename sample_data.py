from models import TimeBlock, Section, Course

math458 = Course(
    name="ABSTRACT ALGEBRA",
    course_code="458",
    department="MATH",
    sections=[
        Section(
            course_reg_num="82321",
            section_id="A",
            course_code="458",
            department="MATH",
            time_blocks=[
                TimeBlock(day=0, start=9*60, end=9*60+50),
                TimeBlock(day=2, start=9*60, end=9*60+50),
                TimeBlock(day=4, start=9*60, end=9*60+50),
            ]
        ),
    ]
)

math408 = Course(
    name="",
    course_code="COMPUTATIONAL METHODS FOR DIFFERENTIAL EQUATIONS",
    department="MATH",
    sections=[
        Section(
            course_reg_num="80643",
            section_id="A",
            course_code="408",
            department="MATH",
            time_blocks=[
                TimeBlock(day=0, start=12*60, end=12*60+50),
                TimeBlock(day=2, start=12*60, end=12*60+50),
                TimeBlock(day=4, start=12*60, end=12*60+50),
            ]
        ),
    ]
)
math431 = Course(
    name="MATHMATICAL BIOLOGY",
    course_code="431",
    department="MATH",
    sections=[
        Section(
            course_reg_num="81233",
            section_id="A",
            course_code="431",
            department="MATH",
            time_blocks=[
                TimeBlock(day=0, start=13*60, end=13*60+50),
                TimeBlock(day=2, start=13*60, end=13*60+50),
                TimeBlock(day=4, start=13*60, end=13*60+50),
            ]
        ),
    ]
)

math498 = Course(
    name="SPECIAL TOPICS",
    course_code="498B",
    department="MATH",
    sections=[
        Section(
            course_reg_num="82397",
            section_id="A",
            course_code="498",
            department="MATH",
            time_blocks=[
                TimeBlock(day=1, start=9*60+30, end=10*60+45),
                TimeBlock(day=3, start=9*60+30, end=10*60+45),
            ]
        ),
    ]
)

math324 = Course(
    name="STATISTICAL MODELING",
    course_code="324",
    department="MATH",
    sections=[
        Section(
            course_reg_num="81577",
            section_id="A",
            course_code="324",
            department="MATH",
            time_blocks=[
                TimeBlock(day=1, start=11*60, end=12*60+15),
                TimeBlock(day=3, start=11*60, end=12*60+15),
            ]
        ),
    ]
)

math455 = Course(
    name="PARTIAL DIFFERENTIAL EQUATIONS",
    course_code="455",
    department="MATH",
    sections=[
        Section(
            course_reg_num="80138",
            section_id="A",
            course_code="324",
            department="MATH",
            time_blocks=[
                TimeBlock(day=1, start=14*60, end=15*60+15),
                TimeBlock(day=3, start=14*60, end=15*60+15),
            ]
        ),
    ]
)

math324_alt = Course(
    name="STATISTICAL MODELING",
    course_code="324",
    department="MATH",
    sections=[
        Section(
            course_reg_num="81577",
            section_id="B",
            course_code="324",
            department="MATH",
            time_blocks=[
                TimeBlock(day=1, start=14*60, end=15*60+15),
                TimeBlock(day=3, start=14*60, end=15*60+15),
            ]
        ),
    ]
)

math500_alt = Course(
    name="LINEAR VECTOR SPACES",
    course_code="500",
    department="MATH",
    sections=[
        Section(
            course_reg_num="81004",
            section_id="A",
            course_code="500",
            department="MATH",
            time_blocks=[
                TimeBlock(day=1, start=11*60, end=12*60+15),
                TimeBlock(day=3, start=11*60, end=12*60+15),
            ]
        ),
    ]
)
COURSES = [math458, math408, math431, math498, math324, math455, math324_alt, math500_alt]
