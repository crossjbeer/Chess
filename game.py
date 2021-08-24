from termcolor import colored

class piece():
    def __init__(self, name, position, symbol, color):
        self.name = name 
        self.position = position
        self.symbol = symbol
        self.color = color

        self.firstMove = True 
        self.captured  = False 

    def updatePosition(self, newPosition):
        self.position = newPosition

        #if(self.firstMove):
        #    self.updateFirstMove()

    def setCaptured(self):
        self.captured = True

    def calcNewPos(self, position, direction):
        newPosition = (position[0] + direction[0], position[1] + direction[1])
        return(newPosition)

    def updateFirstMove(self):
        self.firstMove = False 

    def makeRay(self, position, direction, board, singlePosition = False):
        nextPos = self.calcNewPos(position, direction)

        color_player = board.getColorPlayer(self.color)
        opposite_player = board.getOppositePlayer(self.color)

        if(not board.positionInBounds(nextPos)):
            return([])

        elif(color_player.pieceAtPosition(nextPos)):
            return([])

        elif(opposite_player.pieceAtPosition(nextPos)):
            return([nextPos])

        elif(singlePosition):
            return([nextPos])

        else:
            return([nextPos] + self.makeRay(nextPos, direction, board))

    def pawnPositions(self, board):
        p = self.position 

        directions = [(1,0)]

        if(self.firstMove):
            directions += [(2,0)]

        if(board.getOppositePlayer(self.color).pieceAtPosition(self.calcNewPos(p, directions[0]))):
            directions = [] 

        elif(self.firstMove and board.getOppositePlayer(self.color).pieceAtPosition(self.calcNewPos(p, directions[1]))):
            directions = [directions[0]]

        if(self.color):
            directions = [(i[0] * -1,0) for i in directions]

        if(not self.color): # WHITE
            diagonalDirections = [(1, -1), (1, 1)]
        else:               # BLACK
            diagonalDirections = [(-1, -1), (-1,1)]

        for diagonal in diagonalDirections:
            if(board.getOppositePlayer(self.color).pieceAtPosition(self.calcNewPos(p, diagonal))):
                directions.append(diagonal)

        positions = []
        for direction in directions:
            ray = self.makeRay(p, direction, board, singlePosition=True)

            positions += ray

        return(positions)

    def rookPositions(self, board):
        p = self.position 

        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        positions = []

        for direction in directions:
            ray = self.makeRay(p, direction, board)
            positions += ray 

        return(positions)

    def knightPositions(self, board):
        p = self.position 

        directions = [(-2,-1), (-2,1), (2,1), (2,-1), (1,2), (-1,2), (-1,2), (-1,-2)]

        positions = []

        for direction in directions:
            ray = self.makeRay(p, direction, board, singlePosition=True)

            positions += ray 

        return(positions)

    def bishopPositions(self, board):
        p = self.position 

        directions = [(1,1), (1,-1), (-1,1), (-1,-1)]

        positions = []
        
        for direction in directions:
            ray = self.makeRay(p, direction, board)

            positions += ray 

        return(positions)

    def queenPositions(self, board):
        positions = self.rookPositions(board)
        positions += self.bishopPositions(board)

        return(positions)

    def kingPositions(self, board):
        p = self.position 

        directions = [(1,1), (1,-1), (-1,1), (-1,-1), (1,0), (-1,0), (0,1), (0,-1)]

        positions = []

        for direction in directions:
            ray = self.makeRay(p, direction, board, singlePosition=True)

            positions += ray 

        return(positions)

    def validPositions(self, board):
        posFunctions = {
            'pawn':self.pawnPositions,
            'rook':self.rookPositions,
            'knight':self.knightPositions,
            'bishop':self.bishopPositions,
            'queen':self.queenPositions,
            'king':self.kingPositions
        }

        positionFunction = posFunctions[self.name]

        validPos = positionFunction(board)

        return(validPos)


class player():
    def __init__(self, color):
        self.color = color
        self.pieces = self.buildInitialPieceList(self.color)

        self.kingCheck = False 

    def makeWhitePieces(self):
        pl = []
        
        pl.append(piece("pawn", (2,1), 'P', self.color))
        pl.append(piece("pawn", (2,2), 'P', self.color))
        pl.append(piece('pawn', (2,3), 'P', self.color))
        pl.append(piece('pawn', (2,4), 'P', self.color))
        pl.append(piece('pawn', (2,5), 'P', self.color))
        pl.append(piece('pawn', (2,6), 'P', self.color))
        pl.append(piece('pawn', (2,7), 'P', self.color))
        pl.append(piece('pawn', (2,8), 'P', self.color))

        pl.append(piece('rook', (1,1), 'R', self.color))
        pl.append(piece('rook', (1,8), 'R', self.color))

        pl.append(piece('knight', (1,2), 'N', self.color))
        pl.append(piece('knight', (1,7), 'N', self.color))

        pl.append(piece('bishop', (1,3), "B", self.color))
        pl.append(piece('bishop', (1,6), "B", self.color))

        pl.append(piece('queen', (1,4), "Q", self.color))
        pl.append(piece('king', (1,5), "K", self.color))

        return(pl)

    def makeBlackPieces(self):
        pl = []

        pl.append(piece("pawn", (7,1), "P", self.color))
        pl.append(piece("pawn", (7,2), "P", self.color))
        pl.append(piece('pawn', (7,3), "P", self.color))
        pl.append(piece('pawn', (7,4), "P", self.color))
        pl.append(piece('pawn', (7,5), "P", self.color))
        pl.append(piece('pawn', (7,6), "P", self.color))
        pl.append(piece('pawn', (7,7), "P", self.color))
        pl.append(piece('pawn', (7,8), "P", self.color))

        pl.append(piece('rook', (8,1), "R", self.color))
        pl.append(piece('rook', (8,8), "R", self.color))

        pl.append(piece('knight', (8,2), "N", self.color))
        pl.append(piece('knight', (8,7), "N", self.color))

        pl.append(piece('bishop', (8,3), "B", self.color))
        pl.append(piece('bishop', (8,6), "B", self.color))

        pl.append(piece('queen', (8,4), "Q", self.color))
        pl.append(piece('king', (8,5), "K", self.color))

        return(pl)

    def buildInitialPieceList(self, color):
        if(not color):
            # Do white pieces
            return(self.makeWhitePieces())

        elif(color):
            # do black pieces
            return(self.makeBlackPieces()) 

        else:
            print("[{}] IS NOT A VALID COLOR".format(color))
            return()

    def getPieceAtPosition(self, position):
        for piece in self.pieces:
            if(not piece.captured and piece.position == position):
                return(piece)

        return(None)

    def getKing(self):
        for piece in self.pieces:
            if(piece.name == 'king'):
                return(piece)

    def commaCount(self, s):
        cc = 0
        for i in s:
            if i == ",":
                cc += 1

        return(cc)

    def convertInputToPosition(self, inp, board):
        if(inp == "q"):
            return(inp)

        if(len(inp) == 2):
            cha = inp[0]
            sint = inp[1]

            try:
                col = board.chaToNum[cha]
                try:
                    row = board.sintToNum[sint]
                except:
                    return(None)
            except:
                return(None)

            position = (row, col)

            return(position)
                    
    def convertPositionToNotation(self, position, board):
        col = position[1]
        row = position[0]

        char = next(key for key, value in board.chaToNum.items() if value == col)
        sint = next(key for key, value in board.sintToNum.items() if value == row)

        notation = char + sint 

        return(notation)
    
    def pieceAtPosition(self, position):
        piece = self.getPieceAtPosition(position)

        if(piece is None):
            return(False)

        return(True)

    def getPositionInput(self, board):
        position = None 

        while position != "q" and position is None: 
            position = input("> ")

            prePosition = position

            position = self.convertInputToPosition(position, board)

            if(position is None):
                print("[{}] Invalid Position".format(prePosition))

        return(position)

    def selectPiece(self, board):
        position = None 

        colorDict = {False:'White', True:'Black'}

        while not self.pieceAtPosition(position):
            print("[{}] Coords of Piece to Move".format(colorDict[self.color]))
            position = self.getPositionInput(board)

            if not board.positionInBounds(position):
                print("Position out of Bounds [{}]".format(position))

            elif not self.pieceAtPosition(position):
                print("No Piece at [{}].".format(position))

            print()
            
        return(position)

    def moveFixesCheck(self, board, position, move):
        if(move is None):
            return(False)

        self.movePiece(position, move)

        isCheck = self.kingInCheck(board)

        self.movePiece(move, position)

        if(not isCheck):
            return(True)

        return(False)

    def hasMoveToFixCheck(self, position, board):
        piece = self.getPieceAtPosition(position)

        if(piece is None):
            return(False)

        moves = piece.validPositions(board)

        for move in moves:
            if(self.moveFixesCheck(board, position, move)):
                return(True)

        return(False)

    def selectPieceToMove(self, board):
        position = None 

        while not self.hasValidSpacesToMove(position, board) or (self.kingCheck and not self.hasMoveToFixCheck(position, board)):
            position = self.selectPiece(board)

            if(not self.hasValidSpacesToMove(position, board)):
                piece = self.getPieceAtPosition(position)
                print("Selected Piece [{}, {}] has no valid sapaces to move. Try Again...\n".format(piece.name, piece.position))

            if(self.pieceAtPosition(position) and self.kingCheck and not self.hasMoveToFixCheck(position, board)):
                piece = self.getPieceAtPosition(position)
                print("KING IN CHECK! {} @ {} CANNOT FIX CHECK".format(piece.name, self.convertPositionToNotation(piece.position, board)))

        return(position)

    def hasValidSpacesToMove(self, position, board):
        piece = self.getPieceAtPosition(position)

        if(piece is None):
            return(False)

        moves = piece.validPositions(board)

        if(piece.name == 'king'):
            to_pop = []

            for piece in board.getOppositePlayer(self.color).pieces:
                piece_moves = piece.validPositions(board)

                for i, move in enumerate(moves):
                    if move in piece_moves:
                        to_pop.append(i)

            new_moves = []
            for i in range(len(moves)):
                if(i not in to_pop):
                    new_moves.append(moves[i])

            moves = new_moves 


        if(len(moves) == 0):
            return(False)

        return(True)

    def selectNewPosition(self, piecePosition, board):
        position = None

        while (not board.positionInBounds(position)) or (position not in self.getPieceAtPosition(piecePosition).validPositions(board)) or (not self.moveFixesCheck(board, piecePosition, position)):
            print("Select space to move piece")
            position = self.getPositionInput(board)

            if position not in self.getPieceAtPosition(piecePosition).validPositions(board):
                print("[{}] Not Valid Position.".format(position))

        return(position)

    def movePiece(self, piecePos, newPos):
        piece = self.getPieceAtPosition(piecePos)
        piece.updatePosition(newPos)

        return

    def step(self, board):
        isCheck = self.kingInCheck(board)

        if(isCheck):
            print("CHECK!")
            self.kingCheck = True 

        piecePos = self.selectPieceToMove(board)

        newPos = self.selectNewPosition(piecePos, board)

        self.movePiece(piecePos, newPos)

        self.getPieceAtPosition(newPos).updateFirstMove()

        if(board.getOppositePlayer(self.color).pieceAtPosition(newPos)):
            board.getOppositePlayer(self.color).getPieceAtPosition(newPos).setCaptured()

        return(self)

    def isKingCaptured(self):
        king = self.getKing()

        return(king.captured)

    def kingInCheck(self, board):
        king = self.getKing()

        kingPos = king.position

        opPlayer = board.getOppositePlayer(self.color)

        for piece in opPlayer.pieces:
            valid_spaces = piece.validPositions(board)

            if(kingPos in valid_spaces):
                return(True)

        return(False)



class board():
    def __init__(self):
        self.bounds = (8,8)
        self.players = [player(False), player(True)]

        self.playerTurn = False  # False = white, True = black

        self.chaToNum  = {"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8}
        self.sintToNum = {"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8}

        self.colorDict = {False:'White', True:'Black'}

        self.moveList = []

    def positionInBounds(self, position):
        if(position is None or not isinstance(position, tuple) or not isinstance(position[0], int) or not isinstance(position[1], int)):
            return(False)

        if(position[0] < 1 or position[0] > self.bounds[0]):
            return(False)
        
        elif(position[1] < 1 or position[1] > self.bounds[1]):
            return(False)

        return(True)

    def showBoard(self):
        color_dict = {False:'red', True:'blue'}

        numList = ["1 ","2 ","3 ","4 ","5 ","6 ","7 ","8 "]
        chaList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        whitePlayer = self.players[0]
        blackPlayer = self.players[1]

        boardTop    = "  " + "_" * 5 * self.bounds[0] + " "
        pieceBottom = "|___|"
        bottomCap   = "  " + pieceBottom * self.bounds[0] + "\n"

        letterCap   = "  "
        chaSeed = "  {}  "
        for cha in chaList:
            letterCap = letterCap + chaSeed.format(cha)

        pieceLeftCap = "| "
        pieceRightCap = " |"

        boardPrint = boardTop + "\n"

        for i in range(self.bounds[0], 0, -1):
            boardPrint = boardPrint + str(numList[i-1])
            for j in range(1, self.bounds[1]+1):
                current_position = (i, j)

                piece = whitePlayer.getPieceAtPosition(current_position)
                if(piece is None):
                    piece = blackPlayer.getPieceAtPosition(current_position)
                
                if(piece is None):
                    boardPrint = boardPrint + pieceLeftCap + " " + pieceRightCap 
                else:
                    boardPrint = boardPrint + pieceLeftCap + colored(piece.symbol, color_dict[piece.color]) + pieceRightCap

            boardPrint = boardPrint + "\n" + bottomCap

        boardPrint += letterCap
        
        print(boardPrint)

        return 

    def getColorPlayer(self, color):
        return(self.players[color])

    def getOppositePlayer(self, color):
        return(self.players[not color])

    def play(self):
        while True: 
            self.next() 

            if(self.exitCondition()):
                print("***  GAMVE OVER  ***")
                print("***  {} WINS   ***".format(self.colorDict[self.playerTurn]))

                self.showBoard()
                break

            self.playerTurn = not self.playerTurn

    def next(self):
        self.showBoard()

        playerGoing = self.getColorPlayer(self.playerTurn)

        playerGoing = playerGoing.step(self)

    def exitCondition(self):
        if(self.getOppositePlayer(self.playerTurn).isKingCaptured()):
            return(True)
        return(False)

    def addToMoveList(self, movedPiece, startingPos, endingPos, takenPiece):
        self.moveList.append((movedPiece, startingPos, endingPos, takenPiece))

def main():
    b = board()

    b.play()



if(__name__ == "__main__"):
    main()



