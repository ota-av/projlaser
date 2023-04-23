import React from 'react';
import { Programmer } from './components/Programmer';

function App() {
  return (
    <div className="w-full h-full flex flex-col">
      <div className='flex-1'>Playbacks</div>
      <Programmer className=''></Programmer>
    </div>
  );
}

export default App;
