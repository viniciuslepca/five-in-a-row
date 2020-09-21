import React from 'react';
import ReactDOM from 'react-dom';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Image from "react-bootstrap/Image";

import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const gameImage = require('./images/game.jpg');

class App extends React.Component {
    constructor(props) {
        super(props);

        const pages = {
            'PLAY': 'Play',
            'RULES': 'Rules'
        };

        this.state = {
            activePage: pages.PLAY,
            pages: pages
        };
    }

    setActivePage = (page) => {
        this.setState({activePage: page});
    };

    renderActivePage = () => {
        switch (this.state.activePage) {
            case this.state.pages.PLAY:
                return <Game/>
            case this.state.pages.RULES:
                return <Rules/>;
            default:
                return null
        }
    }

    render() {
        return (
            <div>
                <Header pages={this.state.pages}
                        setActivePage={this.setActivePage}/>
                {this.renderActivePage()}
            </div>
        );
    }
}

class Game extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            height: 19,
            width: 19,
            baseUrl: "http://localhost:5000"
        }
    }

    render() {
        return (
            <div className="game">
                <Board height={this.state.height} width={this.state.width}
                       baseUrl={this.state.baseUrl}/>
            </div>
        )
    }
}

class Board extends React.Component {
    constructor(props) {
        super(props);

        const cellStates = {
            NULL: null,
            BLACK: "⚫",
            WHITE: "⚪"
        }

        this.state = {
            boardData: null,
            cellStates: cellStates,
            blackTurn: true,
            winner: null
        }
    }

    getBoardFromServer = async () => {
        const response = await fetch(this.props.baseUrl + '/game').then(response => response.json())
        this.setState({boardData: response['board_data']})
    }

    componentDidMount() {
        this.getBoardFromServer();
    }

    handleCellClick = async (x, y) => {
        if (this.state.boardData[x][y].cellState === this.state.cellStates.NULL) {
            const val = this.state.blackTurn ? this.state.cellStates.BLACK : this.state.cellStates.WHITE;
            const response = await fetch(this.props.baseUrl + "/game", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    x: x,
                    y: y,
                    val: val
                })
            }).then(response => response.json())
            this.setState({
                boardData: response['board_data'],
                blackTurn: !this.state.blackTurn,
                winner: response['winner']
            }, () => {
                if (this.state.winner !== null) alert("Winner: " + this.state.winner)
            });
        }
    }

    renderBoard = (data) => {
        if (this.state.boardData === null) return null;

        return data.map((row) => {
            return row.map((item) => {
                return (
                    <div
                        key={item.x * row.length + item.y}>
                        <Cell
                            onClick={() => this.handleCellClick(item.x, item.y)}
                            value={item}
                        />
                        {(row[row.length - 1] === item) ?
                            <div className="clear"/> : ""}
                    </div>
                );
            })
        });
    }

    render() {
        return (
            this.renderBoard(this.state.boardData)
        );
    }
}

class Cell extends React.Component {
    render() {
        return (
            <div
                className={"cell" + (this.props.value.cellState === null ? " active" : "")}
                onClick={this.props.onClick}>
                {this.props.value.cellState}
            </div>
        )
    }
}

function Rules(props) {
    return (
        <div id="rules-body">
            <Image src={gameImage} style={{height: 400}}/>
            <p>
                Gomoku, also called Five in a Row, is an abstract strategy board
                game. It is traditionally played with Go pieces (black and white
                stones) on a Go board.

                Players alternate turns placing a stone of their color on an
                empty intersection. The winner is the first player to form an
                unbroken chain of five stones horizontally, vertically, or
                diagonally.
            </p>
        </div>
    )
}

function Header(props) {
    return (
        <Navbar bg="light" variant="light">
            <Navbar.Brand href="#home">Five in a Row</Navbar.Brand>
            <Nav className="mr-auto" defaultActiveKey={props.pages.PLAY}
                 onSelect={(selectedKey) => props.setActivePage(selectedKey)}>
                {Object.keys(props.pages).map(pageName => {
                    const page = props.pages[pageName];
                    return <Nav.Link key={page}
                                     eventKey={page}>{page}</Nav.Link>
                })}
            </Nav>
        </Navbar>
    )
}

ReactDOM.render(<App/>, document.getElementById('root'));
