import { useState, useEffect } from "react";
import "./Car.css";

function Car() {
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
    <div>
    
      <h2>Available Spaces: {availableSpaces !== null ? availableSpaces : "Loading..."}</h2>
    </div>
  );
}

export default Car;