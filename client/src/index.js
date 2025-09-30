import {createContext} from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App.js';

export const Context = createContext(null)

const root = ReactDOM.createRoot(document.getElementById('root'))

root.render(
    // Example: Providing a simple value
    <Context.Provider value={{ user: null, setUser: () => {} }}>
        <App />
    </Context.Provider>
);
