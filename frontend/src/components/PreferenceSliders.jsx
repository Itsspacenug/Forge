const SLIDERS = [
    { key: 'compactness', label: 'Compactness', left: 'Not important', right: 'Very Important'},
    { key: 'time_of_day', label: 'Time of day', left: 'Not important', right: 'Very Important'},
    { key: 'day_spread', label: 'Day spread', left: 'Not important', right: 'Very Important'},
    { key: 'day_length', label: 'Day length', left: 'Not important', right: 'Very Important'},
    { key: 'lunch_breaks', label: 'Lunch breaks', left: 'Not important', right: 'Very Important'}
]

const SIZES = [28, 22, 16, 22, 28]

export default function PreferenceSliders({ weights, onChange }) {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {SLIDERS.map(slider => (
                <div key={slider.key}>
                    <p style={{ margin: '0 0 8px', fontWeight: 500}}>{slider.label}</p>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px'}}>
                        <span style={{ fontSize: '13px', color: '#666', minWidth: '80px'}}>
                            {slider.left}
                        </span>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            {[0,1,2,3,4].map(i => {
                                const value = i / 4
                                const size = SIZES[i]
                                const selected = weights[slider.key] === value

                                return (
                                    <button 
                                        key={i}
                                        onClick={() => onChange(slider.key, value)}
                                        style={{
                                            width: `${size}px`,
                                            height: `${size}px`,
                                            borderRadius: `50%`,
                                            border: selected ? '2px solid #406DB4' : '2px solid #d1d5db',
                                            background: selected ? '#406DB4' : 'white',
                                            cursor: 'pointer',
                                            padding: 0,
                                            transition: 'all 0.15s ease',
                                        }}
                                    />
                                )
                            })}
                        </div>

                        <span style={{ fontSize: '13px', color: '#666', minWidth: '80px'}}>
                            {slider.right}
                        </span>
                    </div>
                </div>
            ))}
        </div>
    )
}