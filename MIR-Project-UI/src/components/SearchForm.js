import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import ListGroup from 'react-bootstrap/ListGroup';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row'
import React, {Component} from "react";
import * as queryString from "query-string";
import {SERVER_IP_ADDRESS} from "../constants";

class SearchForm extends Component {
    constructor(props) {
        super(props);
        let mode = queryString.parse(window.location.search).mode;
        if (!mode)
            mode = "0";
        let query = queryString.parse(window.location.search).query;
        this.state = {
            searchModes: [],
            suggestions: [],
            query,
            searchMode: parseInt(mode)
        };
        this.submit = this.submit.bind(this);
        this.searchInput = this.searchInput.bind(this);
        this.handleChangeSearchMode = this.handleChangeSearchMode.bind(this)
        this.handleSearchInputChange = this.handleSearchInputChange.bind(this)
    }


    submit(e) {
        e.preventDefault();

        let query = this.state.query
        let mode = this.state.searchMode

        let url = "/search?" + queryString.stringify({ query, mode });
        console.log("url: " + url);
        window.location = url;
    }

    render() {
        const {small} = this.props;
        let searchInput = this.searchInput();
        return (
            <Row as={Form} action={"/search"} className="w-100 flex-grow-1"  method="GET"
                  onSubmit={this.submit}>
                    {searchInput}
                    <div className={small ? "col-3" : ""}>
                        <div className={small ? "col-10" : "d-flex justify-content-center mt-5"}>
                            <input className={"btn btn-light ml-2 rounded-pill " + (small ? "" : "col-lg-4 col-auto")}
                                   type="submit"
                                   value="Search"/>
                        </div>
                    </div>
            </Row>
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
        let query = this.state.query
        let suggestions = this.state.suggestions
        const { small } = this.props;
        return (
                <Col md={small ? 4 : 8} className="flex-grow-1">
                    <InputGroup className="">
                        <DropdownButton
                            id="dropdown-basic-button"
                            variant="outline-secondary"
                            title={searchModes[searchMode]}>
                            {
                                searchModes.map((value, index) =>
                                    <Dropdown.Item
                                        onClick={() => this.handleChangeSearchMode(index)}
                                        key={index}>
                                        {value}
                                    </Dropdown.Item>)
                            }
                        </DropdownButton>
                        <Form.Control aria-label="Text input with dropdown button" value={query} onChange={this.handleSearchInputChange} />
                    </InputGroup>
                        <ListGroup>
                            {
                                suggestions.map((suggestion) => (
                                    <ListGroup.Item onClick={(e) => {
                                        e.preventDefault();
                                     this.setState({
                                        query: suggestion
                                    })}} action>
                                        {suggestion}
                                    </ListGroup.Item>
                                ))
                            }
                        </ListGroup>
                </Col>
        )
    }

    handleChangeSearchMode(searchMode) {
        let params = queryString.parse(window.location.search);
        params.mode = searchMode;
        let url = (this.props.small ? "/search?" : "?") + queryString.stringify(params);
        console.log("url: " + url);
        window.location = url;
    }

    handleSearchInputChange(e) {
        let query = e.target.value
        console.log(query)
        this.setState({query})
        fetch(SERVER_IP_ADDRESS + `/qe?query=${encodeURIComponent(query)}`)
            .then(result => result.json())
            .then(result => {
                console.log("Query suggestions");
                console.log(result);
                this.setState({suggestions: result.suggestions})
            })
    }
}

export default SearchForm;
