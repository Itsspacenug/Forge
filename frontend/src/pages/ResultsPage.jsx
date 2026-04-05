import React, { useState } from 'react';
import WeeklyGrid from '../components/WeeklyGrid';
import './ResultsPage.css';
import { useCourses } from '../hooks/useCourses'


const formatMinutesToTime = (totalMinutes) => {
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  
  const period = hours >= 12 ? 'PM' : 'AM';
  const displayHours = hours % 12 || 12; // Converts 0 to 12 for AM/PM
  const displayMinutes = minutes.toString().padStart(2, '0'); // Adds leading zero

  return `${displayHours}:${displayMinutes} ${period}`;
};

//const ResultsPage = ({ generatedSchedules, coursedf, sectiondf, timeblockdf }) => {
const ResultsPage = ({ schedule, onBack }) => {
   const { data: courses = [] } = useCourses()

  const [currentSchedule, setCurrentSchedule] = useState(schedule)
  // 2. Sidebar State (The "Halving" Trigger)
  const [selectedData, setSelectedData] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  


    const inputdf = currentSchedule.sections.map(s => ({
        crn: s.course_reg_num,
        code: s.course_code
    }))

    const sectiondf = currentSchedule.sections.map(s => ({
        crn: s.course_reg_num,
        section_id: s.section_id,
        timeblock_id: s.time_blocks.map((_, i) => `${s.course_reg_num}-${i}`)
    }))

    const timeblockdf = currentSchedule.sections.flatMap(s =>
        s.time_blocks.map((tb, i) => ({
            timeblock_id: `${s.course_reg_num}-${i}`,
            day: tb.day,
            start: tb.start,
            end: tb.end
        }))
    )
   
    const coursedf = []

/*
  // 3. Current Schedule Logic
  // Assuming generatedSchedules is an array of CRN lists: [ ["82321", "81100"], ["82322", "81105"] ]
  const currentCrns = generatedSchedules[currentIndex] || [];
  
  // Reconstruct the 'inputdf' format that your WeeklyGrid expects
  const currentInputDf = currentCrns.map(crn => {
    const sec = sectiondf.find(s => s.crn === crn);
    return { crn: crn, code: sec ? sec.course_code : '' };
  });

*/

  const handleBlockClick = (allData) => {
    setSelectedData(allData); // Contains { input, section, course, block }
    setIsSidebarOpen(true);
  };

  const handleSwap = (sec) => {
    const newSection = {
        course_reg_num: sec.course_reg_num,
        course_code: selectedData.input.code,
        section_id: sec.section_id,
        time_blocks: sec.time_blocks
    }

    const newSections = currentSchedule.sections.map(s =>
        s.course_code === selectedData.input.code ? newSection : s
    )

    setCurrentSchedule({ ...currentSchedule, sections: newSections })
    setIsSidebarOpen(false)
    setSelectedData(null)
}


  return (
    <div className={`results-container ${isSidebarOpen ? 'sidebar-open' : ''}`}>
        <button onClick={onBack}>Back</button>
        
        {/* Top Bar for Schedule Switching 
        <div className="results-nav">
        <button onClick={() => setCurrentIndex(i => Math.max(0, i - 1))}>Prev</button>
        <span>Schedule {currentIndex + 1} / {generatedSchedules.length}</span>
        <button onClick={() => setCurrentIndex(i => Math.min(generatedSchedules.length - 1, i + 1))}>Next</button>
        </div>
        */}

      <div className="view-view">
        <main className="grid-area">
          <WeeklyGrid 
            inputdf={inputdf}
            coursedf={coursedf}
            sectiondf={sectiondf}
            timeblockdf={timeblockdf}
            onBlockClick={handleBlockClick}
          />
        </main>

        {/* The Detail Panel */}
        <aside className="details-sidebar">
        {selectedData ? (
        <div className="sidebar-content">
            <h2>{selectedData.course?.name || selectedData.input.code}</h2>
            <p><strong>Code:</strong> {selectedData.input.code}</p>
            <p><strong>CRN:</strong> {selectedData.input.crn}</p>
            <p><strong>Section:</strong> {selectedData.section.section_id}</p>
            <hr />
            <p>Start: {formatMinutesToTime(selectedData.block.start)}</p>
            <p>End: {formatMinutesToTime(selectedData.block.end)}</p>

            <hr />
            <p><strong>Other Sections</strong></p>
            <div className="section-list">
            {courses
                .find(c => c.course_code === selectedData.input.code)
                ?.sections.map(sec => (
                <button
                    key={sec.section_id}
                    className={`section-btn ${sec.section_id === selectedData.section.section_id ? 'active' : ''}`}
                    onClick={() => handleSwap(sec)}
                >
                    Section {sec.section_id}
                </button>
                ))
            }
            </div>
        </div>
        ) : (
        <p style={{ color: '#9ca3af', fontSize: '14px' }}>Click a course block to see details</p>
        )}
        <button className="close-btn" onClick={() => setIsSidebarOpen(false)}>✕ Close</button>
        </aside>
      </div>
    </div>
  );
};

export default ResultsPage;