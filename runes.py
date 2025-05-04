import random
import functools
import sys


log = print

# The actual spells the players see when they decode the rune spell
# They all need to be the same length
spell_phrases = """
    @brave#soul!
    @heroic#act!
    @savior!!!!!
    @masked#one!
    @rescue!!!!!
    @legend!!!!!
    @true#gri!!!
    @avenger!!!!
    @true#fort!!
    @masked#one!
    @pixie#dust!
    @fey#folk!!!
    @glamour!!!!
    @elf#light!!
    @sprite!!!!!
    @fair#one!!!
    @will#o#wisp
    @moss#child!
    @dew#drops!!  
    @sprite!!!!!
    @dark#lord!!
    @nemesis!!!!
    @evil#queen!
    @mad#king!!!
    @the#fiend!!
    @doom#bringe
    @wicked#one!
    @menace!!!!!
    @corruption!
    @doom#bringe
""".split()

spell_len = len(spell_phrases[0])
spell_count = len(spell_phrases)
log(f"{spell_len=} {spell_count=}")

# The list of the runes that encrypt a particular rune
# Could be a list...
# If the dependencies is a list of length n, you need to add all the (n+1) 
# runes to decode it.
# The easiest configuartion is to make a single sequence:
dep_list = {
    i: [i + 1]
    for i in range(spell_count)
}
 
dep_list[spell_count - 1] = []


log(dep_list)
# From a to z 

# The 30 symbols we use:
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

# The combination can be by addind or substracting. 
# By choosng to substract, decoding is easier.
def combine(rune_a: list[int], rune_b: list[int]) -> list[int]:
    return [
        (a - b) % len(alphabet_encode)
        for (a, b) in zip(rune_a, rune_b)
    ]

def random_msg(seed: int) -> list[int]:
    random.seed(seed)
    return [random.randint(0, spell_count - 1) for _ in range(spell_len)]
    
@functools.cache
def encrypted_spell(rune_idx: int) -> list[int]:
    dep_idxs = dep_list[rune_idx]
    if not dep_idxs:
        return random_msg(rune_idx)
    
    return functools.reduce(
        combine,
        [
            encoded_spell_phrases[rune_idx],
            *[encrypted_spell(i) for i in dep_idxs]
        ]
    )

encrypted_spell_phrases = [
    encrypted_spell(idx)
    for idx in range(spell_count)
]


decoded_encrypted_spell_phrases = [
    ''.join([alphabet_decode[c] for c in spell_phrase])
    for spell_phrase in encrypted_spell_phrases
]

real_idx_to_public_idx = list(range(spell_count))

random.seed(42)
random.shuffle(real_idx_to_public_idx)
public_idx_to_real_idx = {
    real_idx_to_public_idx[i]: i
    for i in range(spell_count)
}

for (i, decoded, spell) in zip(range(30), decoded_encrypted_spell_phrases, spell_phrases):
    log(f"{i:2} ({real_idx_to_public_idx[i]:2})  {decoded} {spell}")
    
for public in range(spell_count):
    log(f"p {public:2}: {public_idx_to_real_idx[public]:2}")

