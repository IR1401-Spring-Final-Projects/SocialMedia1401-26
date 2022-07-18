import * as React from "react";
import {ResultItem} from "./ResultItem";
import logo from "../logo.svg";
import SearchForm from "./SearchForm";
import {SERVER_IP_ADDRESS} from "../constants";
import * as queryString from "query-string";

export class ResultsContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {pages: [], isLoaded: false};
        let query = this.props.location.search;
        this.getPages = this.getPages.bind(this);
        let url = SERVER_IP_ADDRESS + '/hw3/query' + decodeURIComponent(query);
        console.log("sending request to: ", url);
        fetch(url).then(res => res.json()).then(results => {
            console.log(results);
            return this.setState({results: results, isLoaded: true});
        });
    }

    static getSpinner() {
        return (
            <div className="min-vh-100 d-flex justify-content-center align-items-center">
                <div className="row spinner-border" role="status">
                    <span className="sr-only">Loading...</span>
                </div>
            </div>
        );
    }

    render() {
        let content = "";
        if (this.state.isLoaded === false)
            content = ResultsContainer.getSpinner();
        else
            content = this.getPages();
        let params = queryString.parse(this.props.location.search);
        let mode = params.mode;
        let query = params.query;
        return <div>
            <nav className="navbar bg-dark container-fluid">
                <div className="row w-100">
                    <div className="col-sm col-md col-lg-1">
                        <a href="/">
                            <img src={logo} className="img-fluid mr-3 mt-1" alt="logo" style={{"height": "30px"}}/>
                        </a>
                    </div>
                    <div className="col-6-lg col-sm col-md">
                        <SearchForm defaultValue={query} small={true} mode={mode}/>
                    </div>
                </div>
            </nav>
            {content}
        </div>
    };

    getPages() {
        let pages = this.state.results;
        return (
            <div className="mt-1 col-8 p-1">
                {pages.map((value, index) => <ResultItem key={index} data={value}/>)}
            </div>
        )
    }
}
