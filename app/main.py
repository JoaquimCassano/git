import sys
import os
import zlib

def parse_blob(data:str) -> str:
    return data.split("\0", 1)[-1]

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




def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage

    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
             f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file":
        arg = sys.argv[2]
        if arg == "-p":
            hash = sys.argv[3]
            print(cat_file(hash), end="")
    else:
         raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    #print(parse_blob("blob 52\x00raspberry grape blueberry strawberry mango pineapple"))
    main()

