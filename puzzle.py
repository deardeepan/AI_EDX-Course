from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is a knight or a knave but not both:
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # If A is a knight his sentence is true:
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is a knave his sentence is false:
    Implication(AKnave, Not(And(AKnight, AKnave)))
)
   
# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
   # A is a knight or a knave but not both:
   And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
   # A is a knight or a knave but not both:
   And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # If A is a knight his sentence is true:
   Implication(AKnight, And(AKnave, BKnave)),
    # If A is a knave his sentence is false:
    Implication(AKnave, Not(And(AKnave, BKnave)))
      
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is a knight or a knave but not both:
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is a knight or a knave but not both:
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
  # If A is a knight his sentence is true:
      Implication(AKnight,Or(And(AKnave,BKnave),And(AKnight,BKnight))),
      # If A is a knave his sentence is false:
       Implication(AKnave,Not(Or(And(AKnave,BKnave),And(AKnight,BKnight)))),
      # If B is a knight his sentence is true:
        Implication(BKnight,Or(And(AKnave,BKnight),And(AKnight,BKnave))),
    # If B is a Knave his sentence is false:
        Implication(BKnave,Not(Or(And(AKnave,BKnight),And(AKnight,BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
## "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A,B,C is a knight or a knave but not both:
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight,CKnave)),Not(And(CKnight,CKnave)),
    # B says "A said 'I am a knave'.":
        Implication(BKnight,And(Implication(AKnight,AKnave),Implication(AKnave,Not(AKnave)))),
        Implication(BKnave,Not(And(Implication(AKnight,AKnave),Implication(AKnave,Not(AKnave))))),
    # B says "C is a knave."
    Implication(BKnight, CKnave), 
    Implication(BKnave, Not(CKnave)),
    # C says "A is a knight."    
    Implication(CKnight,AKnight),
    Implication(CKnave,Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
