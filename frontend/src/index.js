import React from 'react';
import ReactDOM from 'react-dom/client';
import Scraper from './scrape'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Scraper />
  </React.StrictMode>
);

