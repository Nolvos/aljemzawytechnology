import React, { useState } from 'react';
import ReactDOM from 'react-dom';

const App = () => {
  const [result, setResult] = useState('');

  const handleClick = async () => {
    // Make a request to the Vercel URL
    const response = await fetch('https://vercel.com/houssams-projects/aljemzawy');

    // Get the response body
    const body = await response.json();

    // Set the result state
    setResult(body.result);
  };

  return (
    <div>
      <input type="text" value={result} />
      <button onClick={handleClick}>What is ?</button>
    </div>
  );
};

ReactDOM.render(<App />, document.getElementById('root'));
