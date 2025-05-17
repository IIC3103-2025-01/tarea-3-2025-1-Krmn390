import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import WikipediaQueryForm from './components/WikipediaQueryForm';

function App() {
  return (
    <div className="min-h-screen bg-white">
      <WikipediaQueryForm />
    </div>
  );
}

export default App;

