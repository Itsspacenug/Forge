export default function CourseChips({ courses, onRemove }) {
    if (courses.length === 0) return null

    return (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {courses.map(course => (
                <div key={courses.code} style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '4px 10px',
                    background: '#e0e7ff',
                    borderRadius: '999px',
                }}>
                    <span>{courses.code} - {courses.title}</span>
                    <button
                        onMouseDown={() => onRemove(course)}
                        style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                    >
                        X
                        </button>
                        </div>
                        ))}
        </div>
    )
}