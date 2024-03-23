alp = ['а', 'б', 'в', 'г', 'д', 'е',
    'ё', 'ж', 'з', 'и', 'й', 'к',
    'л', 'м', 'н', 'о', 'п', 'р',
    'с', 'т', 'у', 'ф', 'х', 'ц',
    'ч', 'ш', 'щ', 'ъ', 'ы', 'ь',
    'э', 'ю', 'я']

def encode(s: str, key: str, alp: list) -> str:
    l = len(alp)
    l2 = len(key)
    res = ""
    j = 0

    if (isinstance(key, str)):
        key = [alp.index(c) for c in key]

    for i in range(len(s)):
        k = key[j]
        while (k < 0):
            k = l - k
        res += alp[(alp.index(s[i]) + k) % l]
        j += 1
        if (j >= l2):
            j = 0

    return res

def decode(s: str, key: str, alp: list) -> str:
    l = len(alp)
    if (isinstance(key, str)):
        key = [alp.index(c) for c in key]
    key = [l - k for k in key]
    return encode(s, key, alp)

print("Current language: Russian")

# s = input("Input word: ").lower()
# key = input("Input key: ").lower()
s = 'методпрямогоперебора'
key = 'выбрать'
cs = encode(s, key, alp)
print("Word: ", s)
print("Crypted word: ", cs)
print("Decrypted word: ", decode(cs, key, alp))