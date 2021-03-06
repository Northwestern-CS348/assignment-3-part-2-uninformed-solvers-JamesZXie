from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution istate s reached, False otherwise
        """
        ### Student code goes here

        curr = self.currentState

        if self.currentState.state == self.victoryCondition:
            return True

        # if "numsteps" in self.visited:
        #     self.visited["numsteps"] += 1
        # else:
        #     self.visited["numsteps"] = 1
        #
        # print("______________________________BEFORE OPERATION " + str(self.visited["numsteps"]) + "___________________________________")
        #
        # print("current children: ")
        # for child in curr.children:
        #     print(child.state)
        # # print("next to visit: ", curr.nextChildToVisit)
        # # print("depth: ", curr.depth)
        # # if curr.parent:
        # #     print("parent: ", curr.parent.state)
        # # else:
        # #     print("parent: ", curr.parent)
        # # print("requiredMovable: ", curr.requiredMovable)
        # print("self.currentState: ", curr.state)
        # # print("current gamestate: ", self.gm.getGameState())
        # if self.gm.getMovables():
        #     for binding in self.gm.getMovables():
        #         print("movable: ", binding)

        depth = curr.depth

        if not curr.children:
            self.visited[curr] = True
            if self.gm.getMovables():
                #if there are places to move, then we're not at a leaf and must initialize the children.
                for a_statement in self.gm.getMovables():
                    # for each movable statement, there is a child. Make the move, store that new state in an object,
                    # then revert back to our current state.
                    self.gm.makeMove(a_statement)
                    currGameState = GameState(self.gm.getGameState(), depth + 1, a_statement)
                    self.gm.reverseMove(a_statement)
                    # add the game state after the move to our children. We should initialize parent, but we'll do that
                    # after we make the nextchildtovisit change, because we want that to be stored.
                    # if currGameState not in self.visited:
                    #     curr.children.append(currGameState)
                    curr.children.append(currGameState)

        # self.currentState.nextChildToVisit += 1
        for a_child in curr.children:
            a_child.parent = self.currentState

        while self.currentState.children[curr.nextChildToVisit] in self.visited:
            self.currentState.nextChildToVisit += 1
            if self.currentState.nextChildToVisit == len(self.currentState.children):
                self.currentState = self.currentState.parent
                self.gm.makeMove(self.currentState.requiredMovable)
                # print("Moving to parent: ", self.currentState.state)



        # print("_____________")
        # print("children initialized: ")
        # for child in curr.children:
        #     print(child.state)
        # print("_____________")

        self.gm.makeMove(curr.children[curr.nextChildToVisit].requiredMovable)
        self.currentState = curr.children[curr.nextChildToVisit]
        curr = self.currentState

        # print("______________________________AFTER OPERATION___________________________________")
        # print("current children: ")
        # for child in curr.children:
        #     print(child.state)
        # print("next to visit: ", curr.parent.nextChildToVisit)
        # print("depth: ", curr.depth)
        # if curr.parent:
        #     print("parent: ", curr.parent.state)
        # else:
        #     print("parent: ", curr.parent)
        # print("requiredMovable: ", curr.requiredMovable)
        # print("after state: ", curr.state)
        # print("victory condition: ", self.victoryCondition)
        # print("visited: ")
        # for key in self.visited:
        #     if type(key) != str:
        #         print(key.state)

        if self.currentState.state == self.victoryCondition:
            return True
        else:
            return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        curr = self.currentState

        if self.currentState.state == self.victoryCondition:
            return True

        # print("______________________________BEFORE OPERATION " + str(
        #     self.visited["numsteps"]) + "___________________________________")
        #
        # print("current children: ")
        # for child in curr.children:
        #     print(child.state)
        # # print("next to visit: ", curr.nextChildToVisit)
        # # print("depth: ", curr.depth)
        # if curr.parent:
        #     print("parent: ", curr.parent.state)
        # # else:
        # #     print("parent: ", curr.parent)
        # # print("requiredMovable: ", curr.requiredMovable)
        # print("self.currentState: ", curr.state)
        # print("current gamestate: ", self.gm.getGameState())
        # if self.gm.getMovables():
        #     for binding in self.gm.getMovables():
        #         print("movable: ", binding)

        depth = curr.depth


        # at this point next_gameState.state should be the next non-visited state, and it should be equal to
        # self.gm.getGameState()

        curr = self.currentState

        if not curr.children:
            self.visited[curr] = True
            if self.gm.getMovables():
                for a_statement in self.gm.getMovables():
                    # for each movable statement, there is a child. Make the move, store that new state in an object,
                    # then revert back to our current state.
                    self.gm.makeMove(a_statement)
                    currGameState = GameState(self.gm.getGameState(), depth + 1, a_statement)
                    self.gm.reverseMove(a_statement)
                    # add the game state after the move to our children. We should initialize parent, but we'll do that
                    # after we make the nextchildtovisit change, because we want that to be stored.
                    if currGameState not in self.visited:
                        self.currentState.children.append(currGameState)



        for a_child in self.currentState.children:
            a_child.parent = self.currentState

        # print("_____________")
        # print("children initialized: ")
        # for child in self.currentState.children:
        #     print(child.state)
        # print("_____________")

        # Back it up to the root
        if self.currentState.parent:
            while self.currentState.parent:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                #
                # print("checking... ", self.currentState.state)
                # print("with... ", self.gm.getGameState())

        # Start BFS + gm.makeMovin' until we reach the next unvisited state.
        queue = [self.currentState]



        # H O L Y SHIT...
        while self.currentState in self.visited:
            self.currentState = queue.pop(0)
            for child in self.currentState.children:
                queue.append(child)

        #store it.
        new_state = self.currentState

        # ok so our state is in the right place, but we don't have the required movables necessary to get to
        # that state. let's stack them up in an array first, appending to the beginning of the array each time.
        moves = []
        if self.currentState.parent:
            while self.currentState.parent:
                moves.insert(0, self.currentState.requiredMovable)
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent

        for move in moves:
            self.gm.makeMove(move)

        self.currentState = new_state

        # Check to see if this state is our victory condition

        # while self.currentState.children[curr.nextChildToVisit] in self.visited:
        #     self.currentState.nextChildToVisit += 1
        #     if self.currentState.nextChildToVisit == len(self.currentState.children):
        #         self.currentState = self.currentState.parent
        #         self.gm.makeMove(self.currentState.requiredMovable)
        #         print("Moving to parent: ", self.currentState.state)
        #
        # print("_____________")
        # print("children initialized: ")
        # for child in curr.children:
        #     print(child.state)
        # print("_____________")
        #
        # self.gm.makeMove(curr.children[curr.nextChildToVisit].requiredMovable)
        # self.currentState = curr.children[curr.nextChildToVisit]
        curr = self.currentState
        #


        if self.currentState.state == self.victoryCondition:
            return True
        else:
            return False

