def get_ch():
    #asks for a a single character.
    ch = input("Enter a character or press the Return key to finish: ")
    while(len(ch) > 1):        
        print("Invalid input, please try again.")
        ch = input("Enter a character or press the Return key to finish: ")
    return ch
def find_state(state, ch):
    """takes in the previous state and character. 
    The function then goes through the following conditions until one condition is met 
    """
    if ch =="h" and (state == 1 or state == 3):
        state = 2;
    elif ch == "a" or ch == "o":
        state = 3
    elif state == 3 and ch == "!":
        state = "success"
    else:
        state = "failure"
    return state
def main():
    """"
    The following function composes two strings. 
    One string is composed of all the states,and another string is composed 
    of all the characters.
    """
    print("I can recognize if you are laughing or not.")
    print("Please enter one character at a time.")
    state = 1
    string = ""
    state_string = "1"
    ch = get_ch()
    string +=ch
    while ch != "":
        state,ch = find_state(state,ch),get_ch()
        string +=ch
        state_string += str(state)
    print("\nYou entered", string)
    if "failure" not in state_string and state_string[-1] == "s":
        print("You are laughing.")
    else:
        print("You are not laughing.")
main()