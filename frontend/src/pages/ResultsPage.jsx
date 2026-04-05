import React, { useState } from 'react';
import WeeklyGrid from '../components/WeeklyGrid';
import './ResultsPage.css';

//const ResultsPage = ({ generatedSchedules, coursedf, sectiondf, timeblockdf }) => {
const ResultsPage = ({ schedule, onBack }) => {

  // 1. Navigation State
  //const [currentIndex, setCurrentIndex] = useState(0);
  
  // 2. Sidebar State (The "Halving" Trigger)
  const [selectedData, setSelectedData] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

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
              <h2>{selectedData.course?.name || "Course Details"}</h2>
              <p><strong>Code:</strong> {selectedData.input.code}</p>
              <p><strong>CRN:</strong> {selectedData.input.crn}</p>
              <p><strong>Section:</strong> {selectedData.section.section_id}</p>
              <hr />
              <p>Start: {selectedData.block.start} mins</p>
              <p>End: {selectedData.block.end} mins</p>
            </div>
          ) : (
            <p>Select a course to see details</p>
          )}
          <button onClick={() => setIsSidebarOpen(false)}>Close</button>
        </aside>
      </div>
    </div>
  );
};

export default ResultsPage;