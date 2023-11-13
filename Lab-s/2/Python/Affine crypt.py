def encode(word: str, a: int, b: int, alp: list) -> str:
    l = len(alp)
    res = '' 
    for c in word:
        res += alp[(a * alp.index(c) + b) % l]

    return res

def decode(word: str, a: int, b: int, alp: list) -> str:
    l = len(alp)
    res = ''
    for c in word:
        res += alp[(a * (alp.index(c) + l - b)) % l]

    return res

####################################################

alp = ['о', 'и', 'у', 'ы', 'н', 'т', 'к', '_']

a = 3
b = 19
word = 'У_НИКИТЫ_ОКУНИ'.lower()
cw = encode(word, a, b, alp)
print(f'Start word: {word}')
print(f'Encrypted word: {cw}')
print(f'Decrypted word: {decode(cw, a, b, alp)}')