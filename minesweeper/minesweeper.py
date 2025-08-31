import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        
        self.height = height
        self.width = width
        self.mines = set()

        
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        
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

        
        count = 0

        
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                
                if (i, j) == cell:
                    continue

                
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

        Logic: If the number of cells in the sentence is equal to the
        count of mines, it logically implies that all cells in the
        sentence must be mines.
        """
        if len(self.cells) == self.count and self.count > 0:
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.

        Logic: If the count of mines in the sentence is 0, it logically
        implies that all cells in the sentence must be safe.
        """
        if self.count == 0 and len(self.cells) > 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.

        Logic:
        1. Check if the 'cell' is part of this sentence.
        2. If it is, remove it from 'self.cells' because its status is now known.
        3. Decrement 'self.count' because one of the mines from the original
           count has been identified.
        4. If the 'cell' is not in the sentence, no action is needed as per requirements.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.

        Logic:
        1. Check if the 'cell' is part of this sentence.
        2. If it is, remove it from 'self.cells' because its status is now known.
        3. The 'self.count' does not change because removing a known safe cell
           doesn't change the number of mines among the *remaining* unknown cells.
        4. If the 'cell' is not in the sentence, no action is needed as per requirements.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        
        self.height = height
        self.width = width

        
        self.moves_made = set()

        
        self.mines = set()
        self.safes = set()

        
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

        
        self.mark_safe(cell)

        
        x, y = cell
        neighbors = set()
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i, j) == cell:
                    continue
                    
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor_cell = (i, j)

                    if neighbor_cell not in self.moves_made and \
                       neighbor_cell not in self.safes and \
                       neighbor_cell not in self.mines:
                        neighbors.add(neighbor_cell)
                    elif neighbor_cell in self.mines:
                        count -= 1

        if len(neighbors) > 0:
            new_sentence = Sentence(neighbors, count)
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)

        
        update_needed = True
        while update_needed:
            update_needed = False

            new_mines = set()
            new_safes = set()
            
            for sentence in self.knowledge:
                new_mines.update(sentence.known_mines())
                new_safes.update(sentence.known_safes())

            for mine in new_mines:
                if mine not in self.mines:
                    self.mark_mine(mine)
                    update_needed = True

            for safe in new_safes:
                if safe not in self.safes:
                    self.mark_safe(safe)
                    update_needed = True
            
            new_knowledge_base = []
            for sentence in self.knowledge:
                cells_to_remove = set()

                for cell_in_sentence in sentence.cells:
                    if cell_in_sentence in self.safes:
                        cells_to_remove.add(cell_in_sentence)
                    elif cell_in_sentence in self.mines:
                        cells_to_remove.add(cell_in_sentence)
                        sentence.count -= 1

                for cell_to_remove in cells_to_remove:
                    sentence.cells.remove(cell_to_remove)
                
                if len(sentence.cells) > 0:
                    new_knowledge_base.append(sentence)
                elif len(sentence.cells) == 0 and sentence.count == 0:
                    pass 

            if len(new_knowledge_base) < len(self.knowledge):
                update_needed = True
            self.knowledge = new_knowledge_base

            new_inferences = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 == s2:
                        continue
                    
                    
                    
                    if s1.cells.issubset(s2.cells):
                        if s1.cells != s2.cells:
                            inferred_cells = s2.cells - s1.cells
                            inferred_count = s2.count - s1.count
                            
                            if len(inferred_cells) > 0 and inferred_count >= 0 and \
                               inferred_count <= len(inferred_cells):
                                new_sentence = Sentence(inferred_cells, inferred_count)
                                
                                if new_sentence not in self.knowledge and \
                                    new_sentence not in new_inferences:
                                    new_inferences.append(new_sentence)
                                    update_needed = True
            
            for inference in new_inferences:
                self.knowledge.append(inference)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe_cell in self.safes:
            if safe_cell not in self.moves_made:
                return safe_cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        available_moves = []
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    available_moves.append(cell)
        
        if available_moves:
            return random.choice(available_moves)
        return None
