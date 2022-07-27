import React from "react";
import '../App.css';
import Badge from 'react-bootstrap/Badge';

export class ResultItem extends React.Component {
    render() {
        let index, text, score, words;
        ({index, text, Score: score, words} = this.props.data);
        console.log(words)
        if (words.length > 0){
            words = JSON.parse(words.replaceAll("'", '"'))
        } else {
            words = []
        }
        console.log(words)
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
                        {words.map((item)=> <Badge className="m-1" bg="primary">{item}</Badge>)}
                    </h6>
                </p>
                <hr/>
            </div>
        );
    }
}