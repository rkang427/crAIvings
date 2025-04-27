import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [restaurantData, setRestaurantData] = useState(null);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000' || 'http://localhost:3001';

  useEffect(() => {
    async function fetchRestaurantData() {
      try {
        setLoading(true);
        const response = await axios.get(`${apiUrl}/restaurant/recommendations?query=`);
        console.log(response.data);
        setRestaurantData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchRestaurantData();
  }, []);

  const formatData = (data) => {
    if (!data) {
      return "No data found";
    }
    return Object.keys(data).map((key) => (
        <div key={key}>
          <strong>{parseInt(key) + 1}:<span>   </span>
            {typeof data[key] === 'object' ? data[key].name : data[key]}</strong>
          <br/> <strong> address: </strong>
          {typeof data[key] === 'object' ? data[key].address : data[key]}
          <br/> <strong> rating: </strong>
          {typeof data[key] === 'object' ? data[key].stars : data[key]}
        </div>
    ));
  }

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!inputValue) {
      alert("Please enter some input");
      return;
    }

    try {
      const response = await axios.get(`${apiUrl}/restaurant/recommendations`, {
        params: { query: inputValue }
      });
      setRestaurantData(response.data);
    } catch (error) {
      console.error('Error submitting data:', error);
    }
  };

  return (
    <div className="App">
      <h1>What food would you like to eat?</h1>

      <form onSubmit={handleSubmit}>
        <label htmlFor="inputBox">Enter cuisine:</label>
        <input
          id="inputBox"
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="thai, mexican,.."
        />
        <button type="submit">Submit</button>
      </form>

      {loading ? (
        <p>Loading restaurant data...</p>
      ) : (
        restaurantData && (
          <div>
            <h2>Our Recommendations:</h2>
            <div className="pretty-json">
              {formatData(restaurantData)}
            </div>
          </div>
        )
      )}
    </div>
  );
}

export default App;
