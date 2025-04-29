'use client';
import {useState} from 'react';
import Navbar from './navbar';
const NEXT_PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL;
import Head from 'next/head';

async function fetchRestaurantData(query) {
//'https://craivings.vercel.app' || 'http://127.0.0.1:8000' || 'http://localhost:3001';

  try {
    const response = await fetch(`${NEXT_PUBLIC_API_URL}/recommendations/?query=${query}`);
    console.log(response);
    if (!response.ok) {
      throw new Error(`Failed to fetch data: ${response.statusText}`);
    }
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
    if (data.length === 0) {
      return 'Sorry, recommendations coming soon!';
    }
    return data.map((item, index) => (
      <div key={index} className="p-4 border-b">
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


    <div className="flex items-center justify-center min-h-screen p-8 gap-16 sm:p-20">
      <main className="flex flex-col gap-8 items-center sm:items-start w-full max-w-xl">
        <Head>
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <Navbar/>
        <h1 className="text-3xl font-bold text-center">What food would you like to eat?</h1>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full">
          <label htmlFor="inputBox" className="text-lg">Enter cuisine:</label>
          <input
              id="inputBox"
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              placeholder="e.g., Thai, Mexican"
              className="border p-2 rounded"
          />
          <button type="submit" className="mt-2 bg-blue-500 text-white p-2 rounded">Submit</button>
        </form>

        {loading ? (
            <p>Loading restaurant data...</p>
        ) : (
            restaurantData && (
                <div className="mt-8 w-full">
                  <h2 className="text-xl font-semibold">Our Recommendations:</h2>
                  <div className="mt-4">{formatData(restaurantData)}</div>
                </div>
            )
        )}
      </main>
    </div>
  );
}
