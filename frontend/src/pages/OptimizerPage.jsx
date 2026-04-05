import { useState } from 'react'
import CourseSearch from '../components/CourseSearch'
import CourseChips from '../components/CourseChips'
import PreferenceSliders from '../components/PreferenceSliders'
import { useOptimizer } from '../hooks/useOptimizer'

const DEFAULT_WEIGHTS = {
    compactness: 0.5,
    time_of_day: 0.5,
    day_spread: 0.5,
    day_length: 0.5,
    lunch_breaks: 0.5
}

export default function OptimizerPage() {
    const [selectedCourses, setSelectedCourses] = useState([])
    const [weights, setWeights] = useState(DEFAULT_WEIGHTS)

    const { mutate, isPending, isError, error } = useOptimizer()

    const handleAdd = (course) => {
        if (selectedCourses.find(c => c.code === course.code)) return
        setSelectedCourses(prev => [...prev, course])
    }

    const handleRemove = (course) => {
        setSelectedCourses(prev => prev.filter(c => c.code !== course.code))
    }

    const handleWeightChange = (key, value) => {
        setWeights(prev => ({ ...prev, [key]: value}))
    }

    const handleGenerate = () => {
        mutate(
            { courses: selectedCourses, preferences: weights },
            {
                onSuccess: (data) => {
                    console.log('Schedules recieved:', data.results)
                },
                onError: (err) => {
                    console.error('Optimize failed:',err)
                },
            }
        )
    }

    return (
        <div style={{ maxWidth: '600px', margin: '0 auto', padding: '32px' }}>
            <h1>Build your schedule</h1>

            <CourseSearch
                selectedCourses={selectedCourses}
                onAdd={handleAdd}
            />

            <CourseChips
                courses={selectedCourses}
                onRemove={handleRemove}
            />

            <hr style={{ margin: '32px 0', borderColor: '#e5e7eb' }} />

            <h2 style={{ marginBottom: '24px' }}>Preferences</h2>

            <PreferenceSliders
                weights={weights}
                onChange={handleWeightChange}
            />

            {isError && (
                <p style={{ color: 'red', marginTop: '12px' }}>
                    Something went wrong: {error.message}
                </p>
            )}

            <button
                onClick={handleGenerate}
                disabled={selectedCourses.length === 0 || isPending}
                style={{
                    marginTop: '32px',
                    width: '100%',
                    padding: '12px',
                    background: selectedCourses.length == 0 || isPending ? '#d1d5db' : '#4f46e5',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '16px',
                    cursor: selectedCourses.length === 0 || isPending ? 'not-allowed' : 'pointer',
                }}
            >
                {isPending ? 'Generating...' : 'Generate schedules'}
            </button>
        </div>
    )
}

/*const [selectedCourses, setSelectedCourses] = useState([])

const handleAdd = (course) => {
    if (selectedCourses.find(c => c.code === course.code)) return
    setSelectedCourses(prev => [...prev, course])
}

const handleRemove = (course) => {
    setSelectedCourses(prev => prev.filter(c => c.code !== course.code))
}
    */