import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import Layout from './pages/Layout';
import Home from './pages/Home';
import AddPlan from './pages/AddPlan';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path='/addplan' element={<AddPlan />} />
          {/* <Route path="blogs" element={<Blogs />} /> */}
          {/* <Route path="contact" element={<Contact />} /> */}
          {/* <Route path="*" element={<NoPage />} /> */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;