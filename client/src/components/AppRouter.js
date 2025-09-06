import {Context} from "../index.js";
import { useContext } from "react";
import { Route, Routes } from "react-router-dom";
import { authRoutes, publickRoutes } from "../Routes.js";
import { observer } from "mobx-react-lite";
import Chat from "../pages/Chat.js";

const AppRouter = observer(() => {
    return (
        <Routes>
            <Route path="*" element={<Chat></Chat>}></Route>
        </Routes>

    );
});

export default AppRouter;