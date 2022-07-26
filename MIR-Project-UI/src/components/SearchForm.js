import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import React, {Component} from "react";
import * as queryString from "query-string";
import {SERVER_IP_ADDRESS} from "../constants";

class SearchForm extends Component {
    constructor(props) {
        super(props);
        let mode = queryString.parse(window.location.search).mode;
        if (!mode)
            mode = "0";
        this.state = {
            searchModes: [],
            searchMode: parseInt(mode)
        };
        SearchForm.submit = SearchForm.submit.bind(this);
        this.searchInput = this.searchInput.bind(this);
        this.handleChangeSearchMode = this.handleChangeSearchMode.bind(this)
    }


    static submit(e) {
        e.preventDefault();
        let input = document.getElementById("queryInput");
        let params = queryString.parse(window.location.search);
        params.query = input.value;
        let url = "/search?" + queryString.stringify(params);
        console.log("url: " + url);
        window.location = url;
    }

    render() {
        const {small} = this.props;
        let searchInput = this.searchInput();
        return (
            <form className={small ? "" : "container-fluid"} action={"/search"} method="GET"
                  onSubmit={SearchForm.submit}>
                <div className={small ? "row" : ""}>
                    {searchInput}
                    <div className={small ? "col-3" : ""}>
                        <div className={small ? "col-10" : "d-flex justify-content-center mt-5"}>
                            <input className={"btn btn-light ml-2 rounded-pill " + (small ? "" : "col-lg-4 col-auto")}
                                   type="submit"
                                   value="Search"/>
                        </div>
                    </div>
                </div>
            </form>
        )
    }

    componentDidMount() {
        fetch(SERVER_IP_ADDRESS + "/hw3/models").then(value => {
            console.log(value);
            value.json().then(r => this.setState({searchModes: r}))
        })
    }

    searchInput() {
        let searchModes = this.state.searchModes
        let searchMode = this.state.searchMode;
        const {small} = this.props;
        return <div className={small ? "col-sm col-md col-lg-6" : ""}>
            <div className="input-group">
                <div className="input-group-prepend ">
                    <DropdownButton
                        id="dropdown-basic-button"
                        className="input-group-text p-0 m-0 dropdown-input"
                        title={searchModes[searchMode]}                        >
                        {
                            searchModes.map((value, index) =>
                                <Dropdown.Item
                                    onClick={() => this.handleChangeSearchMode(index)}
                                    key={index}>
                                    {value}
                                </Dropdown.Item>)
                        }
                    </DropdownButton>
                </div>
                <input id="queryInput"
                       style={{borderRadius: "0% 2.25rem 2.25rem 0%"}}
                       className={(small ? "form-control d-flex justify-content-center p-0 m-0" : "p-0 m-0 form-control d-flex")}
                       type="text"
                       placeholder="Search"
                       name="query"
                       defaultValue={this.props.defaultValue}/>
            </div>
        </div>
    }

    handleChangeSearchMode(searchMode) {
        let params = queryString.parse(window.location.search);
        params.mode = searchMode;
        let url = (this.props.small ? "/search?" : "?") + queryString.stringify(params);
        console.log("url: " + url);
        window.location = url;
    }
}

export default SearchForm;
