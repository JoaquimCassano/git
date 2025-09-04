import sys, os
import zlib
import hashlib
import stat

def parse_blob(data:bytes) -> str:
    return data.decode().split("\x00", 1)[-1]

def git_filemode(path: str) -> str:
    st = os.lstat(path)  # use lstat so symlinks are not resolved

    if stat.S_ISDIR(st.st_mode):
        return "040000"  # tree (directory)
    elif stat.S_ISLNK(st.st_mode):
        return "120000"  # symbolic link
    elif stat.S_ISREG(st.st_mode):
        # regular file
        if st.st_mode & stat.S_IXUSR:
            return "100755"  # executable file
        else:
            return "100644"  # normal file
    else:
        return "000000"  # unknown/unsupported

def ls_tree(hash:str, name_only:bool) -> None:
    msg = ""
    folderName = hash[:2]
    fileName = hash[2:]
    path = f".git/objects/{folderName}/{fileName}"
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                if name_only:
                    msg += f"{entry.name}\n"
                else:
                    file_content = open(entry.path, mode="r").read()
                    file_hash = create_hash(file_content)
                    msg += f'{git_filemode(entry.path)} blob {file_hash}\t{entry.name}'
            else:
                if name_only:
                    msg += f"{entry.name}\n"
                else:
                    pass
        print(msg, end="")


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
    folder = file_hash[:2]
    fileName = file_hash[2:]
    path = f".git/objects/{folder}"
    print(f'Creating directory at {path}', file=sys.stderr)
    os.mkdir(path)
    with open(f'{path}/{fileName}', "wb") as f:
        content = f"blob {len(fileContent)}\0{fileContent}".encode("utf-8")
        encoded = zlib.compress(content)
        f.write(encoded)
    print(file_hash, end="")



if __name__ == "__main__":
    print(create_hash("hello world"))