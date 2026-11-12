def parse_quantity(text: str) -> int:
    try:
        return int(text)
    except Exception:
        return 0


def normalize_label(label):
    return label.strip().lower()


def read_description(path: str) -> str:
    handle = open(path, encoding="utf-8")
    return handle.read()


def read_description_safely(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()