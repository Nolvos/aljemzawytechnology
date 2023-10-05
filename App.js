import React, { useState } from 'react';
import ReactDOM from 'react-dom';

const App = () => {
  const [codeContent, setCodeContent] = useState('');

  const handleClick = async () => {
    try {
      // Fetch the content of your GitHub repository
      const response = await fetch('https://raw.githubusercontent.com/Nolvos/aljemzawytechnology/main/task4.py');
      
      if (!response.ok) {
        throw new Error('Failed to fetch code content.');
      }

      // Get the response body as text
      const codeText = await response.text();

      // Set the code content state
      setCodeContent(codeText);
    } catch (error) {
      console.error('Error fetching code:', error);
    }
  };

  return (
    <div>
      <pre>{codeContent}</pre>
      <button onClick={handleClick}>Display Python Code</button>
    </div>
  );
};

ReactDOM.render(<App />, document.getElementById('root'));
