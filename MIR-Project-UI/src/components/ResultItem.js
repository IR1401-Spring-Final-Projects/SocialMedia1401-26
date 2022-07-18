import React from "react";
import '../App.css';

export class ResultItem extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let index, text, score, words;
        ({index, text, Score: score, words} = this.props.data);
        return (
            <div className="page container p-1 col-10">
                <div className="row">
                    Doc-{index}:
                    <p className="text-success pl-2">  {score}</p>
                </div>
                <p className="result-content p-3">
                    {text}
                    <br/>
                    <h6 className="text-secondary">
                        {words}
                    </h6>
                </p>
                <hr/>
            </div>
        );
    }
}