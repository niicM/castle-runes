
# The actual spells the players see when they decode the rune spell
# They all need to be the same length
spell_phrases = [
    "@example#",
    ...,
]
spell_len = len(spell_phrases[0])

# The list of the whot runes encrypt a particular rune
# Could be a list...
dep_list = {
    1: (2,),
    2: (3, 4),
    3: ...,
}

# From a to z 
# alphabet_a_z = list((chr(ord('a') + i) for i in range(26))))

# The 30 symbols we use:
# We keep the special symbols coprime to 30,
# only really important to the start 
#                  012345678901234567890123456789
alphabet_decode = "abcdefg#hij@k!lmn$opqrstuvwxyz"
alphabet_encode = {
    alphabet_decode[n]: n
    for n in range(30)
}

encoded_spell_phrases = [
    [alphabet_encode[c] for c in spell_phrase]
    for spell_phrase in spell_phrases
] 

def encript_spell(i: int) -> list[int]:
    ...
