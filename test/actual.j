/*
 * Actual program that does something useful.
 * Uses as much of the grammar as possible
 */ 
class Main {
    Void main(Int argc, Int argv) {
        new GameMaster().main();
    }
}

class GameMaster {

    GameBoard board;
    Ai ai;
    Input input;
    Int numOfMoves;

    Void main() {
        this.board = new GameBoard();
        this.board.init();

        this.ai = new Ai();
        this.input = new Input();

        this.numOfMoves = 0;

        gameLoop();
    }

    Void gameLoop() {
        Int input;
        Int aiMove;
        Bool isFinished;
        Int victor;

        input = "";
        aiMove = -1;
        isFinished = false;
        victor = -1;

        initialMessage();

        while (!isFinished) {
            println("======== Move: " + this.numOfMoves + " =========");
            this.board.printBoard();
            println("Your next move?: >");
            input = this.input.waitForInput();

            this.board.update(input, 0);
            this.numOfMoves = this.numOfMoves + 1;

            if (this.board.isFull()) {
                isFinished = true;
            } else {
                move = this.ai.nextMove(this.board);
                this.board.update(move, 1);
            }
        }

        victor = this.board.determineVictor();

        if (victor == 0) {
            println("Congratulations. You won!");
        } else {
            if (victor == 1) {
                println("Too bad, the AI won :(");
            } else {
                println("It's a draw!");
            }
        }
    }

    Void initialMessage() {
        if (numOfMoves == 0) {
            println("======== WELCOME TO TIC-TAC-TOE ========");
            println("Instructions for play: Enter in your move when prompted!\nThe format of the move must be X where X is the cell number.\nFor example, 3 is a valid move for upper right corner of the board.");
        } else {
            return;
        }
    }
}

class GameBoard {

    Int g00;
    Int g01;
    Int g02;
    Int g10;
    Int g11;
    Int g12;
    Int g20;
    Int g21;
    Int g22;

    Void init() {
        g00=-1; 
        g01=-1; 
        g02=-1; 
        g10=-1; 
        g11=-1; 
        g12=-1; 
        g20=-1; 
        g21=-1; 
        g22=-1; 
    }

    Void printBoard() {
        println(g00 + " " + g01 + " " + g02);
        println(g10 + " " + g11 + " " + g12);
        println(g20 + " " + g21 + " " + g22);
        t1=1;
    }

    Bool isFull() {
        return (this.g00 + this.g01 + this.g02 + this.g10 + this.g11 + this.g12 + this.g20 + this.g21 + this.g22) >= 4;
    }

    Void determineVictor() {
        // That's right, there is no diagonal wins. Sue me.
        // The nested if-else is a test of parser ability
        if (this.g00 + this.g01 + this.g02 == 0) {
            return 0;
        } else {
            if (this.g00 + this.g01 + this.g02 == 3) {
                return 1;
            } else {
                if (this.g10 + this.g11 + this.g12 == 0) {
                    return 0;
                } else {
                    if (this.g10 + this.g11 + this.g12 == 3) {
                        return 1;
                    } else {
                        if (this.g20 + this.g21 + this.g22 == 0) {
                            return 0;
                        } else {
                            return 1;
                        }
                    }
                }
            }
        }
    }

    Void update(Int cell, Int player) {
        if (cell == 0) {
            g00 = player;
        } else {
            if (cell == 1) {
                g01 = player;
            } else {
                if (cell == 2) {
                    g02 = player;
                } else {
                    if (cell == 3) {
                        g10 = player;
                    } else {
                        if (cell == 4) {
                            g11 = player;
                        } else {
                            if (cell == 5) {
                                g12 = player;
                            } else {
                                if (cell == 6) {
                                    g20 = player;
                                } else {
                                    if (cell == 7) {
                                        g21 = player;
                                    } else {
                                        g22 = player;
                                    }
                                }
                            }
                        }
                    }   
                }
            }
        }
    }
}

class Input {
    // Have no idea how readln works so based on nothing
    // this should work
    Int waitForInput() {
        Int input;
        input = "";
        readln(input);
        return input;
    }
}

class Ai {
    Int nextMove(GameBoard board) {
        if (board.g00 < 0) {
            return 0;
        } else {
            if (board.g01 < 0) {
                return 1;
            } else {
                if (board.g02 < 0) {
                    return 2;
                } else {
                    if (board.g10 < 0) {
                        return 3;
                    } else {
                        if (board.g11 < 0) {
                            return 4;
                        } else {
                            if (board.g12 < 0) {
                                return 5;
                            } else {
                                if (board.g20 < 0) {
                                    return 6;
                                } else {
                                    if (board.g21 < 0) {
                                        return 7;
                                    } else {
                                        return 8;
                                    }
                                }
                            }
                        }
                    }   
                }
            }
        }
    }
}