from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        # ask1 = make statement to ask as (on ?X peg1)
        # ask2 = statement (on ?X peg2)
        # ask3 = statement (on ?X peg3)
        # self.kb.ask(ask1) for 2 and 3 as well.
        # assign the bindings from ask to the tuples in the tuple.

        ask1 = parse_input("fact: (on ?X peg1)")
        ask2 = parse_input("fact: (on ?X peg2)")
        ask3 = parse_input("fact: (on ?X peg3)")
        bindings1 = self.kb.kb_ask(ask1)
        bindings2 = self.kb.kb_ask(ask2)
        bindings3 = self.kb.kb_ask(ask3)

        peg1_list = []
        peg2_list = []
        peg3_list = []

        if bindings1:
            for bindingg in bindings1.list_of_bindings:
                curr_disk = bindingg[0].bindings[0].constant.element
                if "disk" in curr_disk:
                    peg1_list.append(int(curr_disk[4:]))
            peg1_list.sort()

        if bindings2:
            for bindingg in bindings2.list_of_bindings:
                curr_disk = bindingg[0].bindings[0].constant.element
                if "disk" in curr_disk:
                    peg2_list.append(int(curr_disk[4:]))
            peg2_list.sort()

        if bindings3:
            for bindingg in bindings3.list_of_bindings:
                curr_disk = bindingg[0].bindings[0].constant.element
                if "disk" in curr_disk:
                    peg3_list.append(int(curr_disk[4:]))
            peg3_list.sort()

        peg1_tuple = tuple(peg1_list)
        peg2_tuple = tuple(peg2_list)
        peg3_tuple = tuple(peg3_list)


        game_state = (peg1_tuple, peg2_tuple, peg3_tuple)
        return game_state

    def getFact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument
        Args:
            fact (Fact): Fact we're searching for
        Returns:
            Fact: matching fact
        """
        for kbfact in self.kb.facts:
            if fact == kbfact:
                return True
        return False


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        # make statement of (on disk firstpeg) and (on disk secondpeg) from movable_statement
        # retract (on disk firstpeg)
        # add (on disk secondpeg)
        # that should be it...

        if type(movable_statement) != Statement or not self.kb.kb_ask(Fact(movable_statement, [])):
            # print("current gamestate: ", self.getGameState())
            # print("~~~~~~~Error: ", movable_statement, "is not a valid movable statement~~~~~~~")
            return None

        # print("current gamestate: ", self.getGameState())
        # if self.kb.kb_ask(parse_input("fact: (movable ?X ?A ?B)")):
        #     for binding in self.kb.kb_ask(parse_input("fact: (movable ?X ?A ?B)")):
        #         print("movable: ", binding.bindings[0].constant.element)
        # if self.kb.kb_ask(parse_input("fact: (empty ?X)")):
        #     for binding in self.kb.kb_ask(parse_input("fact: (empty ?X)")):
        #         print("empty: ", binding.bindings[0].constant.element)
        # if self.kb.kb_ask(parse_input("fact: (top ?X ?A)")):
        #     for binding in self.kb.kb_ask(parse_input("fact: (top ?X ?A)")):
        #         print("top fact: ", binding.bindings[0].constant.element)
        # print("moving: ", movable_statement)



        # remove old "on", add new "on"
        statement1_list = ["on"]
        statement2_list = ["on"]

        statement1_list.append(movable_statement.terms[0])
        statement1_list.append(movable_statement.terms[1])

        statement2_list.append(movable_statement.terms[0])
        statement2_list.append(movable_statement.terms[2])

        curr_fact = Fact(Statement(statement1_list), [])
        new_fact = Fact(Statement(statement2_list), [])


        # print("retracted: fact: (top " + movable_statement.terms[0].term.element + " " + movable_statement.terms[1].term.element + ")")


        # (movable disk1 peg1 peg2)
        # retract (fact: on disk1 peg1)

        # DISK We're moving from:
        # Retract previous on statement
        # Retract previous top statement
        # If empty, say empty.
        # If not empty, make the new top statement using ontopof

        # STEP 1
        self.kb.kb_retract(curr_fact)
        moved_disk= movable_statement.terms[0].term.element
        prev_peg= movable_statement.terms[1].term.element
        new_peg=movable_statement.terms[2].term.element

        # STEP 2
        top_ask = parse_input("fact: (top " + moved_disk + " " + prev_peg + ")")
        if self.kb.kb_ask(top_ask):
            self.kb.kb_retract(top_ask)
        else:
            print("something went wrong with top...")

        # STEP 3
        prev_top_ask = parse_input("fact: (onTopOf " + moved_disk + " ?X)")
        if self.kb.kb_ask(prev_top_ask):
            # then it's not empty, make this one the top.
            for binding in self.kb.kb_ask(prev_top_ask):
                # there should only be one binding...
                disk_on_bottom = binding.bindings[0].constant.element
                # make the disk on bottom the new top of the previous peg
                # then remove the "ontopof" fact because it's no longer true.
                self.kb.kb_assert(parse_input("fact: (top " + disk_on_bottom + " " + prev_peg + ")"))
                self.kb.kb_remove(parse_input("fact: (onTopOf " + moved_disk + " " + disk_on_bottom + ")"))
        else:
            self.kb.kb_assert(parse_input("fact: (empty " + prev_peg + ")"))



        # DISK WE'RE MOVING TO: DEALING WITH TOP, EMPTY, and ONTOPOF.
        # Add new on statement
        # if empty, then remove empty statement. if not, add new ontopof statement and remove old top statement.
        # Add new top statement

        # STEP 1
        self.kb.kb_assert(new_fact)

        # STEP 2
        empty_ask = parse_input("fact: (empty " + new_peg + ")")
        top_ask = parse_input("fact: (top ?X " + new_peg + ")")
        if self.kb.kb_ask(empty_ask):
            self.kb.kb_retract(empty_ask)
        else:
            top_disk = self.kb.kb_ask(top_ask).list_of_bindings[0][0].bindings[0].constant.element
            oldTopFact = parse_input("fact: (top " + top_disk + " " + new_peg + ")")
            ontopof_fact = parse_input("fact: (onTopOf " + moved_disk + " " + top_disk + ")")

            self.kb.kb_retract(oldTopFact)
            self.kb.kb_add(ontopof_fact)

        newTopFact = parse_input("fact: (top " + moved_disk + " " + new_peg + ")")
        self.kb.kb_add(newTopFact)

        # if self.kb.kb_ask(top_ask):
        #     self.kb.kb_retract(parse_input(
        #         "fact: (top " + self.kb.kb_ask(top_ask)[0].bindings[0].constant.element + " " + movable_statement.terms[
        #             1].term.element + ")"))






        # if self.kb.kb_ask(empty_ask):
        #     for binding in self.kb.kb_ask(empty_ask):
        #         empty_peg = binding.bindings[0].constant.element
        #         remove_empty = parse_input("fact: (empty " + empty_peg + ")")
        #         if self.kb.kb_ask(parse_input("fact: (on ?X " + empty_peg + ")")):
        #             print("removing: ", remove_empty)
        #             self.kb.kb_retract(remove_empty)
        #             # print("retracting: (empty " + empty_peg + ")")



        # DISK WE'RE MOVING FROM: DEALING WITH TOP AND EMPTY.
        # First, we retract the previous top statement.
        # then, we must check: if the disk is now empty, we must say it's empty.
        # if it's not, we must now add the new top statement.




        # empty check

        #
        # for top_statement in self.kb.kb_ask(parse_input("fact: (top ?X ?A)")):
        #     print(top_statement)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        ask_tile_11 = parse_input("fact: (located ?X pos1 pos1)")
        ask_tile_12 = parse_input("fact: (located ?X pos2 pos1)")
        ask_tile_13 = parse_input("fact: (located ?X pos3 pos1)")
        ask_tile_21 = parse_input("fact: (located ?X pos1 pos2)")
        ask_tile_22 = parse_input("fact: (located ?X pos2 pos2)")
        ask_tile_23 = parse_input("fact: (located ?X pos3 pos2)")
        ask_tile_31 = parse_input("fact: (located ?X pos1 pos3)")
        ask_tile_32 = parse_input("fact: (located ?X pos2 pos3)")
        ask_tile_33 = parse_input("fact: (located ?X pos3 pos3)")

        bindings_11 = self.kb.kb_ask(ask_tile_11)
        bindings_12 = self.kb.kb_ask(ask_tile_12)
        bindings_13 = self.kb.kb_ask(ask_tile_13)
        bindings_21 = self.kb.kb_ask(ask_tile_21)
        bindings_22 = self.kb.kb_ask(ask_tile_22)
        bindings_23 = self.kb.kb_ask(ask_tile_23)
        bindings_31 = self.kb.kb_ask(ask_tile_31)
        bindings_32 = self.kb.kb_ask(ask_tile_32)
        bindings_33 = self.kb.kb_ask(ask_tile_33)

        row1_list = []
        row2_list = []
        row3_list = []

        row1_list.append(bindings_11.list_of_bindings[0][0].bindings[0].constant.element)
        row1_list.append(bindings_12.list_of_bindings[0][0].bindings[0].constant.element)
        row1_list.append(bindings_13.list_of_bindings[0][0].bindings[0].constant.element)

        row2_list.append(bindings_21.list_of_bindings[0][0].bindings[0].constant.element)
        row2_list.append(bindings_22.list_of_bindings[0][0].bindings[0].constant.element)
        row2_list.append(bindings_23.list_of_bindings[0][0].bindings[0].constant.element)

        row3_list.append(bindings_31.list_of_bindings[0][0].bindings[0].constant.element)
        row3_list.append(bindings_32.list_of_bindings[0][0].bindings[0].constant.element)
        row3_list.append(bindings_33.list_of_bindings[0][0].bindings[0].constant.element)

        counter = 0
        for tile in row1_list:
            if tile == "empty":
                row1_list[counter] = -1
            else:
                row1_list[counter] = int(tile[4:])
            counter += 1

        counter = 0
        for tile in row2_list:
            if tile == "empty":
                row2_list[counter] = -1
            else:
                row2_list[counter] = int(tile[4:])
            counter += 1

        counter = 0
        for tile in row3_list:
            if tile == "empty":
                row3_list[counter] = -1
            else:
                row3_list[counter] = int(tile[4:])
            counter += 1

        gamestate = (tuple(row1_list), tuple(row2_list), tuple(row3_list))
        return gamestate

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        if type(movable_statement) != Statement or not self.kb.kb_ask(Fact(movable_statement, [])):
            return None

        statement1_list = ["located"]
        statement2_list = ["located"]

        statement1_list.append(movable_statement.terms[0])
        statement1_list.append(movable_statement.terms[1])
        statement1_list.append(movable_statement.terms[2])

        statement2_list.append(movable_statement.terms[0])
        statement2_list.append(movable_statement.terms[3])
        statement2_list.append(movable_statement.terms[4])

        curr_fact1 = Fact(Statement(statement1_list), [])
        new_fact1 = Fact(Statement(statement2_list), [])

        curr_empty = parse_input("fact: (located empty " + statement2_list[2].term.element + " " + statement2_list[3].term.element + ")")
        statement3_list = statement1_list
        statement3_list[1] = "empty"
        new_empty = Fact(Statement(statement3_list), [])

        self.kb.kb_retract(curr_fact1)
        self.kb.kb_assert(new_fact1)
        self.kb.kb_retract(curr_empty)
        self.kb.kb_assert(new_empty)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
