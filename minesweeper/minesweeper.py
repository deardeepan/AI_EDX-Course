import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
  
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.safes.add(cell)
        x=cell[0]
        y=cell[1]
        cells = set()
        for i in (x-1, x, x+1):
                if i>-1 and i<8:
                    for j in (y-1, y, y+1):
                        if j>-1 and j<8:
                            cells.add((i,j))
        #cells.remove((x,y))
        newmine=0
        sentence = Sentence(cells, count)
        sentence1 = Sentence(cells, count)
        self.knowledge.append(sentence)
        #for sentencex in self.knowledge and x in len(self.knowledge):
        for cell in sentence.cells:
            if cell in self.moves_made:
                sentence1.cells.remove(cell)
            if cell in self.safes and cell in sentence1.cells:
                sentence1.cells.remove(cell)
            if cell in self.mines and cell in sentence1.cells:
                sentence1.cells.remove(cell)
                sentence1.count=sentence1.count -1
            if len(sentence1.cells) == 1 and sentence1.count ==0:
                for cell in sentence1.cells:
                    if cell not in self.mines:
                        self.safes.add(cell)
            if len(sentence1.cells) == sentence1.count and sentence1.count>0:
                self.mines.update(sentence1.cells)
                newmine=1
        if sentence1.count == 0:
            for cell in sentence1.cells:
                if cell not in self.mines:
                    self.safes.update(sentence1.cells)
         
        while newmine == 1:
            newmine=0
            for sentence in self.knowledge:
                sentence1 = copy.deepcopy(sentence)
                for cell in sentence.cells:
                    if cell in self.moves_made:
                        sentence1.cells.remove(cell)
                    if cell in self.safes and cell in sentence1.cells:
                        sentence1.cells.remove(cell)
                    if cell in self.mines and cell in sentence1.cells:
                        sentence1.cells.remove(cell)
                        sentence1.count=sentence1.count -1
                    if len(sentence1.cells) == 1 and sentence1.count ==0:
                        for cell in sentence1.cells:
                            if cell not in self.mines:
                                self.safes.add(cell)
                    if len(sentence1.cells) == sentence1.count and sentence1.count > 0:
                        if all(cell not in self.mines for cell in sentence1.cells):
                            self.mines.update(sentence1.cells)
                            newmine=1
                if sentence1.count == 0:
                    for cell in sentence1.cells:
                        if cell not in self.mines:
                            self.safes.update(sentence1.cells) 
        
         
        #print(self.safes)
        print("mines are",self.mines)       

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) == 0:
            return(None)
        else:
            movet = random.choice(list(self.safes))
            y=len(self.safes)
            x=0
            while movet in self.moves_made:
                movet=random.choice(list(self.safes))
                x=x+1
                if x == y:
                   return(None)
            self.moves_made.add(movet)
            print("safe move is",movet)
            return(movet)
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        self.height = random.randrange(0,7)
        self.weight = random.randrange(0,7)    
        move = (self.height,self.weight)
        while move in self.moves_made or move in self.mines:
            self.height = random.randrange(0,7)
            self.weight = random.randrange(0,7)  
            if len(self.safes)+len(self.mines) == 64:
                print("64")
                return(None)
            else:
                move = (self.height,self.weight)
        self.moves_made.add(move)     
        return(move)              
        raise NotImplementedError
