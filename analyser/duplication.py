def find_duplicate_lines(tree, source):
    lines = source.splitlines()
    duplicates = []

    for i in range(len(lines) - 2):
        if lines[i] == lines[i + 1] == lines[i + 2]:
            duplicates.append(lines[i])

    return duplicates

