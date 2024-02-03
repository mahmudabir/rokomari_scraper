class BookCategory:
    def __init__(self, name: str, url: str):
        self.name = name.strip()
        self.url = url.strip()

    def __str__(self):
        return f"{self.name}"
