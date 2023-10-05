import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import { ThemeProvider } from 'styled-components';
import theme from './Theme';
import App from './App';

const Root = () => {
  const [result, setResult] = useState('');

  const handleClick = async () => {
    // Make a request to the Python function
    const response = await fetch('http://localhost:5000/predict');

    // Get the response body
    const body = await response.json();

    // Set the result state
    setResult(body.result);
  };

  return (
    <ThemeProvider theme={theme}>
      <App />
      <input type="text" value={result} />
      <button onClick={handleClick}>What is ?</button>
    </ThemeProvider>
  );
};

ReactDOM.render(<Root />, document.getElementById('root'));
