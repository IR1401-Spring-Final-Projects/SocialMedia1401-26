import {BrowserRouter, Route, Switch} from "react-router-dom";
import React from "react";
import App from "./App";
import {ResultsContainer} from "./ResultsContainer";

function NotFound() {
    return (<div>
            404 NOT FOUND
        </div>
    )
}

export function Router() {
    return (
        <BrowserRouter>
            <Switch>
                <Route path="/" exact component={App}/>
                <Route path="/search" component={ResultsContainer}/>
                <Route component={NotFound}/>
            </Switch>
        </BrowserRouter>
    );
}
