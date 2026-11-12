def add_label(label: str, labels: list[str] | None = None) -> list[str]:
    if labels is None:
        labels = []
    labels.append(label)
    return labels