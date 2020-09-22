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
const localUrl = "http://localhost:5000";
const deployedUrl = "https://five-in-a-row-game.herokuapp.com";
// Set up socket.io, first try deployed url
let socket = io(deployedUrl);
// If deployed url doesn't work, try local url
if (socket.disconnected) socket = io(localUrl);

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
    _isMounted = false;

    constructor(props) {
        super(props);

        this.state = {
            boardData: null,
            winner: null,
            userTurn: null,
            userStone: null,
            numPlayers: null
        }
    }

    restartGame = async () => {
        socket.emit('reset_game');
    }

    updateState = (data) => {
        if (this._isMounted) {
            const response = JSON.parse(data);
            this.setState({
                boardData: response['board_data'],
                winner: response['winner'],
                userTurn: response['user_turn'],
                userStone: response['user_stone'],
                numPlayers: response['num_players']
            });
        }
    }

    componentDidMount() {
        this._isMounted = true;

        // If connection fails, set boardData to undefined and display error
        socket.on('connect_error', () => {
            if (this._isMounted) this.setState({boardData: undefined})
        })

        // Receive board updates
        socket.on('update_board', this.updateState)

        // Request data
        socket.emit('get_board', this.updateState)
    }

    componentWillUnmount() {
        this._isMounted = false;
    }

    handleCellClick = async (x, y) => {
        if (this.state.winner === null && this.state.boardData[x][y].cellState === null) {
            socket.emit('make_play', x, y)
        }
    }

    renderBoard = (data, isPlayerTurn, isGameOver) => {
        return (
            <div id="board" className="center-content">
                {
                    data.map((row) => {
                        return row.map((item) => {
                            return (
                                <div key={item.x * row.length + item.y}>
                                    <Cell
                                        onClick={() => this.handleCellClick(item.x, item.y)}
                                        value={item}
                                        isPlayerTurn={isPlayerTurn}
                                        isGameOver={isGameOver}
                                    />
                                    {(row[row.length - 1] === item) ?
                                        <div className="clear"/> : ""}
                                </div>
                            );
                        })
                    })
                }
            </div>
        )
    }

    renderMessage = (isGameOver, isPlayerTurn) => {
        let message = "";
        if (isGameOver) {
            if (this.state.winner === socket.id) {
                message = "Congratulations, you won the game!";
            } else {
                message = "You lost the game :(";
            }
        } else if (isPlayerTurn) {
            message = "It's your turn! Playing " + this.state.userStone;
        } else {
            message = "Waiting for the other player...";
        }

        return (
            <div className="center-content">
                <p>{message}</p>
            </div>
        );
    }

    renderRestartButton = (isGameOver) => {
        if (isGameOver) {
            return (
                <div className="center-content">
                    <Button onClick={this.restartGame}>Restart Game</Button>
                </div>
            )
        }
        return null;
    }

    render() {
        if (this.state.boardData === null) return null;

        if (this.state.boardData === undefined) {
            // Case where connection failed
            return (
                <div className="center-content">
                    <p>It seems like there already are 2 players connected.</p>
                </div>
            )
        }

        if (this.state.numPlayers === 1) {
            return (
                <div className="center-content">
                    <p>Waiting for a second player to connect.</p>
                </div>
            )
        }

        const isGameOver = (this.state.winner !== null);
        const isPlayerTurn = (socket.id === this.state.userTurn);
        return (
            <div>
                {this.renderMessage(isGameOver, isPlayerTurn)}
                {this.renderRestartButton(isGameOver)}
                {this.renderBoard(this.state.boardData, isPlayerTurn, isGameOver)}
            </div>
        );
    }
}

class Cell extends React.Component {
    render() {
        const isActive = (!this.props.isGameOver && this.props.isPlayerTurn
            && this.props.value.cellState === null);
        return (
            <div
                className={"cell" + (isActive ? " active" : "")}
                onClick={this.props.onClick}>
                {this.props.value.cellState}
            </div>
        )
    }
}

function Rules() {
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
