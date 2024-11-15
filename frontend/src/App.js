import React from 'react';
import ImmigrationAdvisorUI from './ImmigrationAdvisorUI';
import { ThemeProvider } from './ThemeContext';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <ImmigrationAdvisorUI />
    </ThemeProvider>
  );
}
export default App;
