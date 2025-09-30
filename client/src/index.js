import {createContext} from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App.js';
import UserChat from "./store/userChat";

export const Context = createContext(null)

const root = ReactDOM.createRoot(document.getElementById('root'))

root.render(
    <Context.Provider value={{
        user: new UserChat()
    }}>
        <App />
    </Context.Provider>
);
