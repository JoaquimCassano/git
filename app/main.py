import sys
import os
from .git_objects import cat_file, hash_object, create_hash

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)


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
    elif command=="hash-object":
        if len(sys.argv) == 4:
            if sys.argv[2] == "-w":
                hash_object(sys.argv[3])
            else:
                raise RuntimeError(f"Invalid argument: {sys.argv[2]}")
        print(create_hash(open(sys.argv[2], "r").read()), end="")


    else:
         raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    #print(parse_blob(b"blob 52\x00raspberry grape blueberry strawberry mango pineapple a"))
    main()

