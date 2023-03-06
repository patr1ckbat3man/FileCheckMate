def interval_config(default_interval: int = 600) -> int:
    try:
        interval = input("Enter verification interval in seconds (press [ENTER] for default 600):\n> ")
        if not interval:
            return default_interval
        return int(interval)
    except ValueError:
        print("Wrong data input!")

def file_config() -> list[str] | None:
    print("Excluding specific file(s) ignores them instead of deleting them from the directory.")
    print("1 - Exclude specific file(s) from monitoring")
    print("2 - Monitor all files in the target directory.")

    try:
        choice = int(input("> "))
        if choice not in [1, 2]:
            print("Invalid choice! Choose from 1 - 2")
        elif choice == 1:
            file_arr = input("Name of file(s) to be excluded: (Separated by space)\n> ").split(" ")
            return file_arr
        else:
            return None
    except ValueError:
        print("Wrong data input!")
