import chardet

with open('CDLI.csv', 'rb') as f:
    result = chardet.detect(f.read())

print(result)
