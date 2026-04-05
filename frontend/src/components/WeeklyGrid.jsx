const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

// 7am is where the calendar starts visually
const GRID_START = 7 * 60;

// How many pixels represent one minute on the calendar
const PIXELS_PER_MINUTE = 1.2;

// Converts start/end minutes into CSS top and height for absolute positioning
const getPositionStyles = (start, end) => ({
  position: 'absolute',
  top: `${(start - GRID_START) * PIXELS_PER_MINUTE}px`,
  height: `${(end - start) * PIXELS_PER_MINUTE}px`,
  left: '4px',
  right: '4px',
  backgroundColor: '#6366f1',
  borderRadius: '4px',
  padding: '4px',
  cursor: 'pointer',
  overflow: 'hidden',
  boxSizing: 'border-box',
});

const columnStyle = {
  position: 'relative',
  flex: 1,
  borderLeft: '1px solid #e5e7eb',
  // Total height = (10pm - 7am) = 15 hours = 900 min * 1.2px
  height: `${15 * 60 * PIXELS_PER_MINUTE}px`,
};

const wrapperStyle = {
  display: 'flex',
  flexDirection: 'row',
  width: '100%',
};

const headerStyle = {
  textAlign: 'center',
  padding: '8px 0',
  fontWeight: '600',
  fontSize: '14px',
  borderBottom: '1px solid #e5e7eb',
};

// Props are built by the parent from the raw API response — WeeklyGrid just renders
const WeeklyGrid = ({ inputdf, coursedf, sectiondf, timeblockdf, onBlockClick }) => {
  return (
    <div style={wrapperStyle}>
      {DAYS.map((dayName, dayIndex) => (
        <div key={dayName} style={{ flex: 1 }}>
          <div style={headerStyle}>{dayName}</div>
          <div style={columnStyle}>

            {inputdf.map(input => {
              // Find the section for this input by CRN
              const section = sectiondf.find(s => s.crn === input.crn);
              if (!section) return null;

              // Find the course info — allowed to be undefined, falls back to input.code
              const course = coursedf.find(c => c.course_code === input.code);

              // Find all timeblocks for this section on the current day
              const blocksForDay = timeblockdf.filter(t =>
                section.timeblock_id.includes(t.timeblock_id) && t.day === dayIndex
              );
              if (blocksForDay.length === 0) return null;

              return blocksForDay.map(block => (
                <div
                  key={`${input.crn}-${block.timeblock_id}`}
                  style={getPositionStyles(block.start, block.end)}
                  onClick={() => onBlockClick({ input, section, course, block })}
                >
                  <strong style={{ fontSize: '11px', color: 'white' }}>
                    {course ? `${course.department} ${course.course_code}` : input.code}
                  </strong>
                  <div style={{ fontSize: '10px', color: 'white' }}>{section.section_id}</div>
                </div>
              ));
            })}

          </div>
        </div>
      ))}
    </div>
  );
};

export default WeeklyGrid;
