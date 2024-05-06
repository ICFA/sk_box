import re
def is_strong_password(password):
    words = re.findall(r'[a-zA-Zа-яА-ЯёЁ]{4,}', password.lower())
    file = open("words.txt", "r")
    lines = file.read().lower().split('\n')
    if any(word in lines for word in words):
        return False
    return True

print(is_strong_password('yieldddheLLO,123'))