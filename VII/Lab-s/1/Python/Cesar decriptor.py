alps = {
    "Russian" : ['а', 'б', 'в', 'г', 'д', 'е',
    'ё', 'ж', 'з', 'и', 'й', 'к',
    'л', 'м', 'н', 'о', 'п', 'р',
    'с', 'т', 'у', 'ф', 'х', 'ц',
    'ч', 'ш', 'щ', 'ъ', 'ы', 'ь',
    'э', 'ю', 'я']
}

def encode(s: str, shift: int, alp: list):
    res = ""
    l = len(alp)

    while (shift < 0):
        shift += l

    for i in range(len(s)):
        res += alp[(alp.index(s[i]) + shift) % l]

    return res

languageKey = "Russian"

def decode(s: str, shift: int, alp: list):
    return encode(s, -shift, alp)

def search(s: str, alp: list):
    res = []
    l = len(alp)

    for i in range(l):
        res.append(encode(s, i, alp))

    return res 
    
print("Current language: ", languageKey)

commands = {
    "к" : encode,
    "д" : decode,
    "п" : search
}

def doCommand(command: str):
    if (command not in commands.keys()):
        exit()

    arg1 = input("Input one word: ")

    if (command in ["к", "д"]):
        arg2 = int(input("Input shift/key: "))
        return commands[command](arg1, arg2, alps[languageKey])
    else:
        return commands[command](arg1, alps[languageKey])

while (True):

    s = input("Input:\nк - кодировать\nд - декодировать\nп - перебор ключей\nanother - exit\n").lower()
    print(doCommand(s))