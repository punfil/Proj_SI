import constants


class DisplayComponent:
    def use_menu(self):
        print("0. Play new game!")
        print("1. Exit")
        print("2. Display instruction")
        option = int(input())
        if option == 0:
            print("Enter 1-3 AI difficulty")
            diff = int(input())
            return constants.menu_play_game, diff
        if option == 1:
            return constants.menu_exit, None
        if option == 2:
            return constants.menu_instruction, None

    def display_result(self, winner):
        print(f"Wins: {winner}")
        print("Wanna play again?")

    def display_board(self, board):
        print("#################")
        for i in range(board._size):
            print(board[i][:])
        print("#################\n")

    def display_instruction(self):
        print("!!!!!!!! Quick tutorial just to let you in!")
        print("You are playing as 'x'. AI plays as 'o'")
        print("123")
        print("456")
        print("789")
        print("Positioning is left-upper corner based. 1 is located (0, 0)")
        print("8 is located (2, 1) etc.")


