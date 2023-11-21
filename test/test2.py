import json


def asdf(name: str, id: int, coordinates: list):
    result = f'Name: {name}, id: {id}, coordinates: {coordinates}'
    print(result)
    return result


with open("test2.json") as f:
    j = f.read()
    content = json.loads(f.read)

asdf(**content)
