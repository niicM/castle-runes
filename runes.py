import random
import functools

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
    !!!!!!!!!!!!
    @pixie#dust!
    @fey#folk!!!
    @glamour!!!!
    @elf#light!!
    @sprite!!!!!
    @fair#one!!!
    @will#o#wisp
    @moss#child!
    @dew#drops!!   
    !!!!!!!!!!!!
    @dark#lord!!
    @nemesis!!!!
    @evil#queen!
    @mad#king!!!
    @the#fiend!!
    @doom#bringe
    @wicked#one!
    @menace!!!!!
    @corruption!
    !!!!!!!!!!!!
""".split()

spell_len = len(spell_phrases[0])
spell_count = len(spell_phrases)
print(f"{spell_len=} {spell_count=}")

# The list of the runes that encrypt a particular rune
# Could be a list...

dep_list = {
    i: [i + 1]
    for i in range(29)
}

for i in (9, 19, 29):
    dep_list[i] = []

dep_list[7].append(19)    
dep_list[18].append(8)    
dep_list[28].append(18)

print(dep_list)
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

def combine(rune_a: list[int], rune_b: list[int]) -> list[int]:
    return [
        (a - b) % 30
        for (a, b) in zip(rune_a, rune_b)
    ]

def random_msg(seed: int) -> list[int]:
    random.seed(seed)
    return [random.randint(0, 29) for _ in range(spell_len)]
    
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

# print('\n'.join(decoded_encrypted_spell_phrases))

real_idx_to_public_idx = list(range(spell_count))

random.seed(42)
random.shuffle(real_idx_to_public_idx)
public_idx_to_real_idx = {
    real_idx_to_public_idx[i]: i
    for i in range(spell_count)
}

for (i, decoded) in enumerate(decoded_encrypted_spell_phrases):
    print(f"{i:2} ({real_idx_to_public_idx[i]:2})  {decoded}")
    
for public in range(spell_count):
    print(f"p {public:2}: {public_idx_to_real_idx[public]:2}")
