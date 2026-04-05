import WeeklyGrid from './WeeklyGrid'

export default function ScheduleNax({ schedule, onSelect }) {

    const inputdf = schedule.sections.map(s => ({
        crn: s.course_reg_num,
        code: s.course_code
    }))

    const sectiondf = schedule.sections.map(s => ({
        crn: s.course_reg_num,
        section_id: s.section_id,
        timeblock_id: s.time_blocks.map((_, i) => `${s.course_reg_num}-${i}`)
    }))

    const timeblockdf = schedule.sections.flatMap(s =>
        s.time_blocks.map((tb, i) => ({
            timeblock_id: `${s.course_reg_num}-${i}`,
            day: tb.day,
            start: tb.start,
            end: tb.end
        }))
    )

    const coursedf = []

    return (
        <div onClick={() => onSelect(schedule)} style={{ cursor: 'pointer' }}>
            
            <div>
                <span>Rank #{schedule.rank}</span>
                <span>Score: {schedule.score}</span>
            </div>

            <WeeklyGrid
                inputdf={inputdf}
                coursedf={coursedf}
                sectiondf={sectiondf}
                timeblockdf={timeblockdf}
                onBlockClick={() => {}}
            />

        </div>
    )

}
