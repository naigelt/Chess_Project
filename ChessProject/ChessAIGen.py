import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knightScores = [[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
                [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
                [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]

bishopScores = [[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]

rookScores = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
              [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
              [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
              [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
              [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
              [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
              [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
              [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]]

queenScores = [[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
               [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
               [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
               [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
               [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
               [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
               [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
               [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]

pawnScores = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
              [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
              [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
              [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
              [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
              [0.5, -0.5, -1.0, 0, 2, 1.0, -0.5, 0.5],
              [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
              [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]



piecePositionScores = {"wN": knightScores,
                         "bN": knightScores[::-1],
                         "wB": bishopScores,
                         "bB": bishopScores[::-1],
                         "wQ": queenScores,
                         "bQ": queenScores[::-1],
                         "wR": rookScores,
                         "bR": rookScores[::-1],
                         "wp": pawnScores,
                         "bp": pawnScores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3


def findBestMove(gameState, valid_moves, returnQueue):
    global nextMove
    nextMove = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(gameState, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if gameState.whiteToMove else -1)
    returnQueue.put(nextMove)


def findMoveNegaMaxAlphaBeta(gameState, valid_moves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gameState)
    maxScore = -CHECKMATE
    for move in valid_moves:
        gameState.makeMove(move)
        nextMoves = gameState.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gameState, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gameState.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def scoreBoard(gameState):
    if gameState.checkmate:
        if gameState.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gameState.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(gameState.board)):
        for col in range(len(gameState.board[row])):
            piece = gameState.board[row][col]
            if piece != "--":
                piecePositionScore = 0
                if piece[1] != "K":
                    piecePositionScore = piecePositionScores[piece][row][col]
                if piece[0] == "w":
                    score += pieceScore[piece[1]] + piecePositionScore
                if piece[0] == "b":
                    score -= pieceScore[piece[1]] + piecePositionScore

    return score


def findRandomMove(valid_moves):
    return random.choice(valid_moves)