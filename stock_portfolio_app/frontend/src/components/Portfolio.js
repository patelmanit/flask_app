import React, { useState, useEffect } from 'react';

const Portfolio = () => {
  const [stocks, setStocks] = useState([]);
  const [symbol, setSymbol] = useState('');
  const [shares, setShares] = useState('');
  const [error, setError] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    try {
      const response = await fetch('http://localhost:5001/get-stocks', {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setStocks(data);
      } else {
        throw new Error('Failed to fetch stocks');
      }
    } catch (err) {
      setError('Failed to load portfolio');
    }
  };

  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:5001/logout', {
        credentials: 'include',
      });
      if (response.ok) {
        window.location.href = '/login';
      }
    } catch (err) {
      setError('Failed to logout');
    }
  };

  // Updated stock search to match backend API
  // ... (previous imports and start of component remain the same)

  useEffect(() => {
    if (!symbol) {
      setSearchResults(null);
      return;
    }

    const searchTimeout = setTimeout(async () => {
      setLoading(true);
      setError('');

      try {
        const encodedQuery = encodeURIComponent(symbol.trim());
        const url = `http://localhost:5001/search-stock?query=${encodedQuery}`;
        console.log('Fetching URL:', url);
        
        const response = await fetch(url, {
          credentials: 'include'
        });

        if (!response.ok) {
          console.error('Search response status:', response.status);
          const errorText = await response.text();
          console.error('Error response:', errorText);
          throw new Error('Search failed');
        }

        const data = await response.json();
        console.log('Raw search results:', data);
        
        if (data && data.length > 0) {
          setSearchResults({
            symbol: data[0].symbol,
            name: data[0].name,
            currentPrice: data[0].currentPrice
          });
        } else {
          setSearchResults(null);
          setError('Stock not found');
        }
      } catch (err) {
        console.error('Search error:', err);
        setError('Failed to search stock');
        setSearchResults(null);
      } finally {
        setLoading(false);
      }
    }, 500);

    return () => clearTimeout(searchTimeout);
  }, [symbol]);

  const handleSymbolChange = (e) => {
    const value = e.target.value.toUpperCase();
    setSymbol(value);
  };

  const handleAddStock = async () => {
    setError('');

    if (!symbol || !shares) {
      setError('Please enter both symbol and number of shares');
      return;
    }

    if (!searchResults) {
      setError('Please enter a valid stock symbol');
      return;
    }

    const sharesNum = parseFloat(shares);
    if (isNaN(sharesNum) || sharesNum <= 0) {
      setError('Please enter a valid number of shares');
      return;
    }

    try {
      const stockData = {
        symbol: searchResults.symbol,
        shares: sharesNum,
        price: searchResults.currentPrice
      };

      console.log('Sending stock data:', stockData);

      const response = await fetch('http://localhost:5001/add-stock', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(stockData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to add stock');
      }

      const newStock = await response.json();
      setStocks((prevStocks) => [...prevStocks, newStock]);
      setSymbol('');
      setShares('');
      setSearchResults(null);
    } catch (err) {
      console.error('Add stock error:', err);
      setError(err.message || 'Failed to add stock');
    }
  };

  const handleDeleteStock = async (id) => {
    try {
      const response = await fetch(`http://localhost:5001/delete-stock/${id}`, {
        method: 'POST',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to delete stock');
      }

      setStocks((prevStocks) => prevStocks.filter((stock) => stock.id !== id));
    } catch (err) {
      console.error('Delete error:', err);
      setError('Failed to delete stock');
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Your Portfolio</h2>
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
        >
          Logout
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      <div className="mb-8">
        <h3 className="text-xl font-semibold mb-4">Add Stock</h3>
        <div className="flex gap-4 flex-wrap">
          <div className="flex-1">
            <input
              type="text"
              value={symbol}
              onChange={handleSymbolChange}
              placeholder="Stock symbol (e.g., AAPL)"
              className="w-full px-3 py-2 border rounded"
            />
            {loading && (
              <div className="mt-2 text-gray-600">Searching...</div>
            )}
            {searchResults && (
              <div className="mt-2 p-2 border rounded bg-gray-50">
                <div className="font-bold">{searchResults.name}</div>
                <div className="text-gray-600">
                  Current Price: ${searchResults.currentPrice.toFixed(2)}
                </div>
              </div>
            )}
          </div>
          <div className="flex-1">
            <input
              type="number"
              value={shares}
              onChange={(e) => setShares(e.target.value)}
              placeholder="Number of shares"
              className="w-full px-3 py-2 border rounded"
              min="0.01"
              step="0.01"
            />
          </div>
          <button
            type="button"
            onClick={handleAddStock}
            disabled={!shares || !searchResults || loading || shares <= 0}
            className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            Add Stock
          </button>
        </div>
      </div>

      <div>
        <h3 className="text-xl font-semibold mb-4">Your Stocks</h3>
        {stocks.length === 0 ? (
          <p className="text-gray-500 text-center py-4">
            No stocks in your portfolio yet. Add some stocks to get started!
          </p>
        ) : (
          <div className="grid gap-4">
            {stocks.map((stock) => (
              <div
                key={stock.id}
                className="flex justify-between items-center p-4 border rounded hover:bg-gray-50"
              >
                <div className="flex gap-6">
                  <span className="font-bold">{stock.symbol}</span>
                  <span>{stock.shares} shares</span>
                  <span>${stock.price.toFixed(2)}</span>
                  <span className="text-gray-600">
                    Total: ${(stock.shares * stock.price).toFixed(2)}
                  </span>
                </div>
                <button
                  onClick={() => handleDeleteStock(stock.id)}
                  className="text-red-500 hover:text-red-700 transition-colors"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Portfolio;