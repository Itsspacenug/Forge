import { useState } from 'react'
import { useCourses } from '../hooks/useCourses'

export default function CourseSearch({ selectedCourses, onAdd }) {
    const [query, setQuery] = useState('') // what's typed in the input
    const [isOpen, setIsOpen] = useState(false) // whether dropdown is visible
    const { data, isLoading } = useCourses()

    const results = (data ?? [])
        .filter(c => !selectedCourses.find(s => s.code === c.code))
        .filter(c =>
            c.code.toLowerCase().includes(query.toLowerCase()) ||
            c.title.toLowerCase().includes(query.toLowerCase())
        )
        .slice(0,10)

    const handleSelect = (course) => {
        onAdd(course)
        setQuery('')
        setIsOpen(false)
    }

    return (
        <div style={{ position: 'relative'}}>
            <input 
                value={query}
                onChange={e => { setQuery(e.target.value); setIsOpen(true) }}
                onFocus={() => setIsOpen(true)}
                onBlur={() => setTimeout(() => setIsOpen(false), 150)}
                placeholder="Search courses..."
            />

            {isOpen && query.length > 0 && results.length > 0 && (
                <ul style={{
                    position: 'absolute',
                    top: '100%',
                    left: 0,
                    right: 0,
                    background: 'white',
                    border: '1px solid #ccc',
                    listStyle: 'none',
                    margin: 0,
                    padding: 0,
                    zIndex: 10,
                }}>
                    {results.map(course => (
                        <li
                            key={course.code}
                            onMouseDown={() => handleSelect(course)}
                            style={{ padding: '8px 12px', cursor: 'pointer' }}
                        >
                            {course.code} - {course.title}
                        </li>
                    ))}
                </ul>
            )}

            {isLoading && <p>Loading courses...</p>}
        </div>
    )
}



const results = (data ?? []).filter(course =>
    course.code.toLowerCase().includes(query.toLowerCase()) ||
    course.title.toLowerCase().includes(query.toLowerCase())
).slice(0,10)

const handleSelect = (course) => {
    onAdd(course)
    setQuery('')
    setIsOpen(false)
}

