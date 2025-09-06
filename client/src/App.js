import React  from 'react';
import { BrowserRouter } from "react-router-dom";

import { observer } from "mobx-react-lite";

import { Spinner, Container } from "react-bootstrap";

const App = observer(() => {
    return (
        <BrowserRouter>
        </BrowserRouter>
    );
});

export default App;