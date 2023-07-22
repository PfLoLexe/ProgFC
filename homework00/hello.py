def get_greeting(name: str) -> str:
    ans = "Hello, " + name + '!'
    return (ans)


if __name__ == "__main__":
    message = get_greeting("World")
    print(message)
