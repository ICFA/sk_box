import re
import sys

def decrypt(encryption):
    result = encryption
    while '..' in result:
        result = re.sub(r'[^\.]\.\.', r'', result)
        if result[:2] == '..':
            result = result[2:]
    result = result.replace('.', '')
    return result


if __name__ == '__main__':
    data = sys.stdin.read()
    decryption = decrypt(data)
    print(decryption)