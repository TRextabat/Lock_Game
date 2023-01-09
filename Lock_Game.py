ALPHA_B = "ABCDEFGH"
MAX_DIMENTION = 8
MIN_DIMENTION = 4

def main():
    cont = "Y"
    print("""Welcome to the lock game """)
    print("This game has been developed by Elyar and Amir ")
    print("This game has been developed without the use of any third party library")
    print("Enjoy The game :))")
    print()
    playerA = input("Enter a character to represent player 1: ")
    print()
    while len(playerA) != 1:
        playerA = input("You can just Enter 1 character for each player\nEnter a character to represent player 1: ")
        print()
    
    playerB = input("Enter a character to represent player 2: ")
    print()
    while len(playerB) != 1 or playerA == playerB:
        if playerA == playerB:
            playerB = input("""Player1 and Player2 symbols can not be same \nchoose another symbole to Player 2: """)
        elif len(playerB) != 1 :
            playerB = input("You can just Enter 1 character for each player\nEnter a character to represent player 2: ")

    while cont == "Y":
        try:
            fieldsize = int(input(f"Enter the row/column number of the playing field ({MIN_DIMENTION}-{MAX_DIMENTION}): "))
            print()
            while not (MIN_DIMENTION <= fieldsize <= MAX_DIMENTION):
                fieldsize = int(input(f"""Field size has to be between {MIN_DIMENTION} and {MAX_DIMENTION} \nEnter the row/column number of the playing field(4-8): """))
                print()
        except ValueError:
            fieldsize = info()
        board = board_make(fieldsize, playerA, playerB)
        board_print(board)
        attacker = playerA
        defender = playerB
        stone_count = {playerA : fieldsize , playerB:fieldsize}
        while stone_count[playerA] != 1 and  stone_count[playerB] != 1 :
            new_location = moving(board,attacker)
            removed_stones_count = lock(board, new_location, attacker, defender)
            stone_count[defender] -= removed_stones_count
            attacker , defender = defender , attacker
            board_print(board)
        if stone_count[playerA] == 1:
            winner = playerB
        else:
            winner = playerA
        print(f"Player {winner} won the game.\n ") 
        cont = input(f"Would you like to play again(Y/N)?: ")
        print()
        while not cont in "NY":#As the example in PDF also doesn't accept y or n
            cont = input("Please Enter Y or N :")  
            print() 
    print("We hope you enjoyed our game see you again :)\n ")

def info():# checks the input so it will not be any other data type than integer 
    try:
        value = int(input(f"""Invalid input \nEnter the row/column number of the playing field({MIN_DIMENTION}-{MAX_DIMENTION}): """))
        print()
        while not (MIN_DIMENTION <= value <= MAX_DIMENTION):
                value = int(input(f""" Field size has to be between {MIN_DIMENTION} and {MAX_DIMENTION} \nEnter the row/column number of the playing field(4-8): """))
                print()
    except ValueError:
        value = info()
    except TypeError:
        value = info()
    return value

def board_make(fieldsize:int, playerA:str, playerB:str):# creates a dictionary representing the rooms on the board exmp = {(1,"A"):x , (2,"B"):None} None represents an empty space 
    field = {}
    for row in range(fieldsize):
        for colum in range(fieldsize):
            if row+1 == 1 :
                field[row+1, ALPHA_B[colum]] = playerA

            elif row+1 == fieldsize:
                field[row+1, ALPHA_B[colum]] = playerB

            else:
                field[row+1, ALPHA_B[colum]] = None
    return field 

def moving(board:dict , attacker:str):  #takes the move as an input and changes the board based on it
    premission = False
   
    while premission == False:
        move = input(f"""Player {attacker}, please enter the position of your own stone you want to move and the \ntarget position(for example 3C 1C):  """)
        print()
        while  (len(move) != 5) or (not " " in move):
            move = input("Please write like example: ")
            print()
        
        try:
            move = [[int(move[0]), move[1].upper()], [int(move[3]), move[4].upper()]]
        except ValueError:
            print("Invalid input enter like example\n ")
            continue
        premission, message = check(board, move,attacker)
       
        if message != None:
            print(f"{message}\n ")
            
    board[tuple(move[0])], board[tuple(move[1])] = board[tuple(move[1])],board[tuple(move[0])]
    return move[1]

def check(board:dict, move:list, attacker:str):#checks the move so it is valid 
    move_premission = True
    message = None
    if not (tuple(move[0]) in board) or not(tuple(move[1]) in board):
        move_premission = False
        message = """ One of your choices is not in the game board:( ! \nplease Enter valid location """
    elif not board[tuple(move[0])] in (attacker , None) :
        move_premission = False
        message = "You can not choose an opponents stone :( !"
    
    elif board[tuple(move[0])] == None:
        move_premission = False
        message = "There is no stone in the position you have chosen please pay attention :("
    
    elif  move[0] == move[1]:
        move_premission = False
        message = "Your target is the same as your location :) whyyyy?"
    
    elif board[tuple(move[1])] != None:
        move_premission = False
        message = "Your target position is occupied :( "
   
    elif not(move[0][0] == move[1][0]) and not(move[0][1] == move[1][1]):
        move_premission = False
        message = "You can only move vertically or horizontally :("
     
    else:#if move is valid , checks so there will be no stones blocking the road
        if move[0][0] == move[1][0] :#move in same row
            loc_1 = ALPHA_B.index(move[0][1])
            loc_2 = ALPHA_B.index(move[1][1])
            
            for location in range(loc_1 - (abs(loc_1-loc_2)//(loc_1-loc_2)) , loc_2, abs(loc_1-loc_2)//(loc_2-loc_1)):#loop itirates from position to target moving through rows,loc_1 is position row , loc_2 is target row , sgn(loc_2 - loc_1) tells the loop how to itirate
                key = (move[0][0],ALPHA_B[location])
                if board[key] != None :
                    move_premission = False
                    message = "There is a stone in the way :( "
                    break
        
        elif move[0][1] == move[1][1]:#move in same column
            loc_1 = move[0][0] 
            loc_2 = move[1][0]
            for location in range(loc_1 - (abs(loc_1-loc_2)//(loc_1-loc_2)) , loc_2 , abs(loc_1-loc_2)//(loc_2-loc_1)):
                key =(location , move[0][1])
                
                if board[key] != None :
                    move_premission = False
                    message = "There is a stone in the way :( "
                    break
    return move_premission, message

def lock(board:dict, room:list, attacker:str, defender:str):#checks if there are any stones locked that are going to be removed
    removed_stones_count = 0
    for i in range(4):# checking the four rooms around the moved stone - 0 is upper square 2 is lower square 1 is right square 3 is left square
        removed_stone = None
        board_dimention = int(len(board) ** 0.5)
        try:
            
            if i == 0 or i == 2:
                sign = abs(i - 1) // (i-1) # if it is 0 sign will be minus to check the upper square (row - 1) = (row - sign)
                checked_tuple = (room[0]+sign , room[1])# checked tuple is the tuple representing one of the four squares that is being checked in an itiration
                if i == 0 :
                    corner_index = 1 # upper corners
                else:
                    corner_index = board_dimention# lower corners
                corner_1  , corner_2  = (corner_index, ALPHA_B[0]) ,(corner_index, ALPHA_B[board_dimention - 1]) # the corners to be checked when i = 0 or 2
            else:
                sign = -1 * abs(i - 2) // (i - 2) #sign specifies if the code is checking left or right
                checked_tuple = (room[0], ALPHA_B[ALPHA_B.index(room[1])+sign]) 
                if i == 1 :
                    corner_index = board_dimention - 1# right corners 
                else:
                    corner_index = 0#left corners
                corner_1 , corner_2 = (1 , ALPHA_B[corner_index]) ,(board_dimention , ALPHA_B[corner_index]) # the corners to be checked when i = 1 or 3
            if board[checked_tuple] == defender:#if there is one of the opponents stones in the square that is being checked

                if checked_tuple == corner_1:#if the square is in the corner_1
                    if i == 0 or i == 2 :# corner 1 is calculated based on i so calculating it here pervents and unwanted exception
                        corner_1_around = (corner_index,ALPHA_B[1])
                    else:
                        corner_1_around = (room[0]+1, ALPHA_B[ALPHA_B.index(room[1])+sign])
                    
                    if board[corner_1_around] == attacker :#if there is another attacker stone locking the stone
                        removed_stone = checked_tuple
                        board[checked_tuple] = None
                        removed_stones_count += 1 

                elif checked_tuple == corner_2:#if the upper stone is in corner 2
                    if i == 0 or i == 2 :
                        corner_2_around = (corner_index,ALPHA_B[board_dimention - 2])
                    else:
                        corner_2_around = (room[0]-1, ALPHA_B[ALPHA_B.index(room[1])+sign])

                    if board[corner_2_around] == attacker :
                        removed_stone = checked_tuple
                        board[checked_tuple] = None
                        removed_stones_count += 1
               
                else:# if the stone is not on any corners
                    if i == 0 or i == 2 :
                        stone_not_corner = (room[0]+sign*2, room[1])
                    else:
                        stone_not_corner = (room[0], ALPHA_B[ALPHA_B.index(room[1])+sign*2])
                    
                    if board[stone_not_corner] == attacker:#if the stone is not in a corner check if there is another stone locking it
                        removed_stone = checked_tuple
                        board[checked_tuple] = None
                        removed_stones_count += 1 
            
        except KeyError:#if there is a room being checked that is out of the board then the loop will countinue
            continue
        except IndexError:
            continue
        else:#if there are any stones removed, returns the number of stones removed 
            if removed_stone != None:
                print()
                print(f"the stone at position {tuple_to_string(removed_stone)} was locked and removed\n ")
    return removed_stones_count

def tuple_to_string(tup:tuple):
    result = ""
    for member in tup:
        result += str(member)
    return result 

def board_print(board:dict):
    board_dimantion = int(len(board) ** 0.5)
    seprator = "-"*int(board_dimantion*6.5)
    print(' ',end = "")
    for column in range(board_dimantion):
        print(f"     {ALPHA_B[column]}" , end = "")
    print()
    for row in range(board_dimantion) :
        print("  "+seprator)
        print(f"{row+1}  ", end="")
        for column in range(board_dimantion):
            print(f"|  ",end = "")
            if board[(row+1, ALPHA_B[column])] != None:
                print(f"{board[(row+1, ALPHA_B[column])]}  ",end = "")
            else:
                print("   ", end = "")
        print(f"|  {row+1}")
    print("  "+seprator)
    print(' ',end = "")
    for column in range(board_dimantion):
        print(f"     {ALPHA_B[column]}" , end = "")
    print(" \n ")

main()   