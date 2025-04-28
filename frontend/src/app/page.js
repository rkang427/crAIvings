'use client';
import { useState } from 'react';

async function fetchRestaurantData(query) {
  const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000' || 'http://localhost:3001';
  try {
    const response = await fetch(`${apiUrl}/recommendations/?query=${query}`);
    if (!response.ok) throw new Error('Failed to fetch data');
    return await response.json();
  } catch (error) {
    console.error('Error fetching data:', error);
    return null;
  }
}

export default function Home() {
  const [restaurantData, setRestaurantData] = useState(null);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);

  const formatData = (data) => {
    if (!data) {
      return 'No data found';
    }
    return data.map((item, index) => (
      <div key={index}>
        <strong>{index + 1}: </strong>{item.name}
        <br />
        <strong>Address: </strong>{item.address}
        <br />
        <strong>Rating: </strong>{item.stars}
      </div>
    ));
  };

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!inputValue) {
      alert('Please enter a cuisine');
      return;
    }

    try {
      setLoading(true);
      const data = await fetchRestaurantData(inputValue);
      setRestaurantData(data);
    } catch (error) {
      console.error('Error submitting data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">

        <h1 className="text-2xl font-bold">What food would you like to eat?</h1>

        <form onSubmit={handleSubmit}>
          <label htmlFor="inputBox">Enter cuisine:</label>
          <input
            id="inputBox"
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Thai, Mexican, .."
            className="border p-2 rounded"
          />
          <button type="submit" className="mt-2 bg-blue-500 text-white p-2 rounded">
            Submit
          </button>
        </form>

        {loading ? (
          <p>Loading restaurant data...</p>
        ) : (
          restaurantData && (
            <div>
              <h2>Our Recommendations:</h2>
              <div className="pretty-json">{formatData(restaurantData)}</div>
            </div>
          )
        )}
      </main>
    </div>
  );
}
