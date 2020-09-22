import React from 'react';
import ReactDOM from 'react-dom';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Image from 'react-bootstrap/Image';
import Button from 'react-bootstrap/Button';
import io from 'socket.io-client';

import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const gameImage = require('./images/game.jpg');
const baseUrl = "http://localhost:5000";
// Set up socket.io
const socket = io(baseUrl);

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

function Game() {
    return (
        <div className="game">
            <Board/>
        </div>
    )
}

class Board extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            boardData: null,
            winner: null,
            userTurn: null
        }
    }

    resetGame = async () => {
        socket.emit('reset_game');
    }

    componentDidMount() {
        // Get board upon connection
        socket.on('connect', () => {
            socket.emit('get_board', (data) => {
                const parsedData = JSON.parse(data);
                const boardData = parsedData['board_data'];
                const userTurn = parsedData['user_turn'];
                this.setState({boardData: boardData, userTurn: userTurn});
            })
        })

        // If connection fails, set boardData to undefined and display error
        socket.on('connect_error', () => {
            this.setState({boardData: undefined})
        })

        // Receive board updates
        socket.on('update_board', (data) => {
            const response = JSON.parse(data);
            this.setState({
                boardData: response['board_data'],
                winner: response['winner'],
                userTurn: response['user_turn']
            }, () => {
                if (this.state.winner !== null) {
                    alert("Winner: " + this.state.winner)
                }
            })
        })
    }

    handleCellClick = async (x, y) => {
        if (this.state.boardData[x][y].cellState === null) {
            socket.emit('make_play', x, y)
        }
    }

    renderBoard = (data) => {
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
        if (this.state.boardData === null) return null;

        if (this.state.boardData === undefined) {
            // Case where connection failed
            return (
                <div style={{textAlign: "center"}}>
                    <p>It seems like there already are 2 players connected.</p>
                </div>
            )
        }

        return (
            <div>
                <Button onClick={this.resetGame} variant="primary">Reset Game
                </Button>
                {this.renderBoard(this.state.boardData)}
            </div>
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
