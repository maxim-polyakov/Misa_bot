import {createContext} from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { applyTheme } from './utils/theme.js';
import App from './App.js';

applyTheme();
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
