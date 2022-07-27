import * as React from "react";
import {ResultItem} from "./ResultItem";
import logo from "../logo.svg";
import SearchForm from "./SearchForm";
import {SERVER_IP_ADDRESS} from "../constants";
import * as queryString from "query-string";

export class ResultsContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {pages: [], isLoaded: false, cluster_label: 0, cluster_keywords: []};
        let query = this.props.location.search;
        this.getPages = this.getPages.bind(this);
        let url = SERVER_IP_ADDRESS + '/hw3/query' + decodeURIComponent(query);
        console.log("sending request to: ", url);
        fetch(url).then(res => res.json()).then(results => {
            console.log("results")
            console.log(results);
            return this.setState({results: results, isLoaded: true});
        });
        let cluster_url = SERVER_IP_ADDRESS + '/clustering' + decodeURIComponent(query);
        fetch(cluster_url).then(res => res.json()).then(result => {
            console.log("cluster")
            console.log(result)
            return this.setState({cluster_label: result.cluster, cluster_keywords: result.keywords})
        })
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
        let cluster_label = this.state.cluster_label;
        let cluster_keywords = this.state.cluster_keywords;
        return (
            <div className="row mt-3">
                <div className="col-8">
                    {pages.map((value, index) => <ResultItem key={index} data={value}/>)}
                </div>
                <div className="col-4">
                    <p className="m-0 p-0 text-success">Cluster-{cluster_label}:</p>
                    <div className="ml-4">
                        {cluster_keywords.map((value, index) => <li>{value}</li>)}
                    </div>

                </div>
            </div>
        )
    }
}
