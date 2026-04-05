import React, { useState, useRef } from 'react';
import { useClickOutside } from '../hooks/useClickOutside';
import './DepartmentDropdown.css';

const DepartmentDropdown = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedDept, setSelectedDept] = useState('');
  const dropdownRef = useRef(null);
  
  const itemRefs = useRef({}); 
  const departments = ['AFGN', 'AMFG', 'BIOL', 'CBEN', 'CEEN', 'CHGC', 'CHGN', 'CSCI', 'CSM', 'DSCI', 'EBGN', 'EDNS', 'EENG', 'ENGY', 'FEGN', 'GEGN', 'GEGX', 'GEOL', 'GEOC', 'GOGN', 'GPGN', 'HASS', 'HNRS', 'LICM', 'LIFL', 'LIMU', 'MAED', 'MATH', 'MEGN', 'MLGN', 'MNGN', 'MSGN', 'MTGN', 'NUGN', 'ORWE', 'PAGN', 'PEGN', 'PHGN', 'ROBO', 'SCED', 'SPRS', 'SYGN'];

  useClickOutside(dropdownRef, () => setIsOpen(false));
  const handleKeyDown = (e) => {
    // Only trigger if the menu is open and a single letter is pressed
    if (isOpen && e.key.length === 1 && e.key.match(/[a-z]/i)) {
      const char = e.key.toUpperCase();
      
      // Find the first department starting with that letter
      const firstMatch = departments.find(dept => dept.toUpperCase().startsWith(char));

      if (firstMatch && itemRefs.current[firstMatch]) {
        // Scroll the matching element into view inside the dropdown panel
        itemRefs.current[firstMatch].scrollIntoView({
          behavior: 'smooth',
          block: 'nearest' 
        });
        setSelectedDept(firstMatch); 
      }
    }
  };

  return (
    <div className="desktop-dropdown" ref={dropdownRef} onKeyDown={handleKeyDown}>
      <button 
        className="dropdown-trigger" 
        onClick={() => setIsOpen(!isOpen)}
        tabIndex="0" 
      >
        <span>{selectedDept || "Select Department"}</span>
        <span>▼</span>
      </button>

      {isOpen && (
        <div className="dropdown-panel">
          <div className="options-grid">
            {departments.map((dept) => (
              <div 
                key={dept}
                ref={el => itemRefs.current[dept] = el}
                className={`option-item ${selectedDept === dept ? 'active' : ''}`}
                onClick={() => {
                  setSelectedDept(dept);
                  setIsOpen(false);
                }}
              >
                {dept}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DepartmentDropdown;