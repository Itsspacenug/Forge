import { useState, useEffect } from 'react'; // Added useEffect
import CourseSearch from '../components/CourseSearch';
import CourseChips from '../components/CourseChips';
import PreferenceSliders from '../components/PreferenceSliders';
import { useOptimizer } from '../hooks/useOptimizer';
import WeeklyGrid from '../components/WeeklyGrid';

const DEFAULT_WEIGHTS = {
    compactness: 0.5,
    time_of_day: 0.5,
    day_spread: 0.5,
    day_length: 0.5,
    lunch_breaks: 0.5
};

function toGridProps(sections) {
        if (!sections) return { inputdf: [], sectiondf: [], timeblockdf: [] };

        const inputdf = sections.map(s => ({
            crn: `${s.course_code}-${s.section_id}`,
            code: s.course_code,
        }));

        const sectiondf = sections.map(s => ({
            crn: `${s.course_code}-${s.section_id}`,
            section_id: s.section_id,
            timeblock_id: s.time_blocks.map((_, i) => `${s.course_code}-${s.section_id}-${i}`),
        }));

    const timeblockdf = sections.flatMap(s =>
        s.time_blocks.map((tb, i) => ({
            timeblock_id: `${s.course_code}-${s.section_id}-${i}`,
            day: tb.day,
            start: tb.start,
            end: tb.end,
        }))
    )

    return { inputdf, sectiondf, timeblockdf }
}

export default function OptimizerPage({ onSelectSchedule }) {  

    const [selectedCourses, setSelectedCourses] = useState([])
    const [weights, setWeights] = useState(DEFAULT_WEIGHTS)
    const [results, setResults] = useState([])
    const [currentIndex, setCurrentIndex] = useState(0)

    const { mutate, isPending, isError, error } = useOptimizer()

    const[message, setMessage] = useState("")

    // 3. Handlers
    const handleAdd = (course) => {
        if (selectedCourses.find(c => c.code === course.code)) return;
        setSelectedCourses(prev => [...prev, course]);
    };

    const handleRemove = (course) => {
        setSelectedCourses(prev => prev.filter(c => c.code !== course.code));
    };

    const handleWeightChange = (key, value) => {
        setWeights(prev => ({ ...prev, [key]: value }));
    };

    const handleGenerate = () => {
        mutate(
            { courses: selectedCourses, preferences: weights },
            {
                onSuccess: (data) => {
                    // Assuming FastAPI returns { results: [...] }
                    setResults(data.results || [])
                    setCurrentIndex(0)
                    if (data.results.length === 0) {
                        setMessage(data.message || "No valid schedules found.")
                    }
                },
                onError: (err) => {
                    console.error('Optimize failed:', err)
                },
            }
        );
    };

    return (
        <div style={{ maxWidth: '600px', margin: '0 auto', padding: '32px' }}>
            <h1>Build your schedule</h1>

            <CourseSearch selectedCourses={selectedCourses} onAdd={handleAdd} />
            <CourseChips courses={selectedCourses} onRemove={handleRemove} />

            <hr style={{ margin: '32px 0', borderColor: '#e5e7eb' }} />

            <h2 style={{ marginBottom: '24px' }}>Preferences</h2>
            <PreferenceSliders weights={weights} onChange={handleWeightChange} />

            {isError && (
                <div style={{ color: 'red', marginTop: '12px', padding: '10px', background: '#fee2e2', borderRadius: '4px'}}>
                    <strong>Optimization Error:</strong>
                    {/* Check if it's a validation error with details */}
                    {error.response?.data?.invalid_codes ? (
                        <p> The following codes are invalid: {error.response.data.detail.invalid_codes.join(', ')}</p>
                    ) : (
                        <p>{error.message}</p>
                    )}
                </div>
            )}

            <button
                onClick={handleGenerate}
                disabled={selectedCourses.length === 0 || isPending}
                style={{
                    marginTop: '32px',
                    width: '100%',
                    padding: '12px',
                    background: selectedCourses.length === 0 || isPending ? '#d1d5db' : '#4f46e5',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '16px',
                    cursor: selectedCourses.length === 0 || isPending ? 'not-allowed' : 'pointer',
                }}
            >
                {isPending ? 'Generating...' : 'Generate schedules'}
            </button>

            {/* Display "No Results" Message */}
            {!isPending && results.length === 0 && message && (
                <div style={{ 
                    marginTop: '20px', 
                    padding: '16px', 
                    backgroundColor: '#fffbeb', 
                    border: '1px solid #f59e0b', 
                    borderRadius: '8px',
                    color: '#b45309' 
                }}>
                    <p><strong>Heads up:</strong> {message}</p>
                </div>
            )}

            {results.length > 0 && (
                <div style={{ marginTop: '40px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                        <button
                            onClick={() => setCurrentIndex(i => Math.max(0, i - 1))}
                            disabled={currentIndex === 0}
                        >
                            ← Prev
                        </button>
                        <button
                            onClick={() => setCurrentIndex(i => Math.min(results.length - 1, i + 1))}
                            disabled={currentIndex === results.length - 1}
                        >
                            Next →
                        </button>
                        <span>
                            Schedule {currentIndex + 1} of {results.length} 
                            — Score: {results[currentIndex].score?.toFixed(2)}
                        </span>
                    </div>

                <WeeklyGrid
                    {...toGridProps(results[currentIndex]?.sections)}
                    coursedf={[]}
                    onBlockClick={() => {}}
                />
                <button onClick={() => onSelectSchedule(results[currentIndex])}>
                    View Full Schedule
                </button>

            </div>
        )}
    </div>
)
}