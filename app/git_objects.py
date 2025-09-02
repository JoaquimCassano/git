import sys, os
import zlib
import hashlib

def parse_blob(data:bytes) -> str:
    return data.decode().split("\x00", 1)[-1]

def cat_file(hash:str) -> str:
    folderName = hash[:2]
    fileName = hash[2:]
    path = f".git/objects/{folderName}/{fileName}"
    with open(path, "rb") as file:
        rawData:bytes = zlib.decompress(file.read())
        print(f'rawData: {rawData}', file=sys.stderr)
        parsed = parse_blob(rawData)
        print(parsed, file=sys.stderr)
        return parsed

def create_hash(data:str) -> str:
    content = f"blob {len(data)}\0{data}".encode("utf-8")
    print(f'Data: {content}',file=sys.stderr)
    hashObj = hashlib.sha1(content)
    return hashObj.hexdigest()

def hash_object(filename:str) -> None:
    fileContent = open(filename, mode="r").read()
    file_hash = create_hash(fileContent)
    folder = fileContent[:2]
    fileName = fileContent[2:]
    path = f".git/objects/{folder}"
    os.mkdir(path)
    with open(f'{path}/{fileName}', "wb") as f:
        content = f"blob {len(fileContent)}\0{fileContent}".encode("utf-8")
        encoded = zlib.compress(content)
        f.write(encoded)
    print(file_hash, end="")



if __name__ == "__main__":
    print(create_hash("hello world"))