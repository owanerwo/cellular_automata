import core

board = [[]]
num_gens = 0
neighborhood_type = "Moore" # "Moore" or "vonNeumann"
rules = {}

def main():
    core.play_cellular_automaton(board, num_gens, neighborhood_type, rules)

if __name__ == "__main__":
    main()
