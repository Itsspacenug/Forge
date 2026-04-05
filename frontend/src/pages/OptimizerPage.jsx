import { useState } from 'react'
import CourseSearch from '../components/CourseSearch'
import CourseChips from '../components/CourseChips'

export default function OptimizerPage() {
    const [selectedCourse, setSelectedCourses] = useState([])

    const handleAdd = (course) => {
        if (selectedCourses.find(c => c.code === course.code)) return
        setSelectedCourses(prev => [...prev, course])
    }

    const handleRemove = (course) => {
        setSelectedCourses(prev => prev.filter(c => c.code !== course.code))
    }

    return (
        <div style={{ maxWidth: '600px', margin: '0 auto', padding: '32px' }}>
            <h1>Build your schedule</h1>

            <CourseSearch
                selectedCourses={selectdeCourses}
                onAdd={handleAdd}
            />

            <CourseChips
                course={selectedCourses}
                onRemove={handleRemove}
            />
        </div>
    )
}

const [selectedCourses, setSelectedCourses] = useState([])

const handleAdd = (course) => {
    if (selectedCourses.find(c => c.code === course.code)) return
    setSelectedCourses(prev => [...prev, course])
}

const handleRemove = (course) => {
    setSelectedCourses(prev => prev.filter(c => c.code !== course.code))
}