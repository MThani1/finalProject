import React from "react";
import { useState, useEffect } from "react";
import "./Splm.css"; // Import the CSS

const SmartParkingApp = () => {

    const [availableSpaces, setAvailableSpaces] = useState(null);

    useEffect(() => {
      const fetchSpaces = async () => {
        const response = await fetch("http://127.0.0.1:8000/available_spaces");
        const data = await response.json();
        console.log('response',response ,' data', data)
        setAvailableSpaces(data.available_spaces);
  
      };
  
      fetchSpaces();
      const interval = setInterval(fetchSpaces, 10000); // Update every 10 seconds
      return () => clearInterval(interval);
    }, []);
  
    useEffect(() => {
      console.log('availableSpaces', availableSpaces)
      
       
    }, [availableSpaces]);
  

  return (
    <div className="app-container">
      <div className="overlay" />
      <div className="card">
        <div className="top-bar">
          <div className="logo">P</div>
          <h1 className="app-title">SMART PARKING</h1>
          <div className="menu-icon"><img src="/Logo-Nile-University-of-Nigeria.svg" width={100} /></div>
        </div>
        <div className="count">{availableSpaces !== null ? availableSpaces : "Loading..."
            }</div>
        <div className="label">SPOTS AVAILABLE</div>
      </div>
    </div>
  );
};

export default SmartParkingApp;
