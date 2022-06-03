def find_length_n_paths(n, board, words):
    for x, y in zip(range(len(board)), range(len(board))):
        words.append(_find_path_helper((x, y), board, n, [], [], WDICT, "path"))
    return words

def _find_path_helper(start, board, n, path, all, wdict, find_by):
    word = "".join([board[cell[0]][cell[1]] for cell in path])
    if find_by == "path":
        key = path
    else:
        key = word
    if len(key) == n:
        if word in wdict:
            all.append(key.copy())
            # return all
        # else:
            # return all

    else:
        for cell in get_neighbors(start):
            if cell not in path:
                path.append(cell)
                _find_path_helper(cell, board, n, path, all, wdict, find_by)
                path.pop(cell)
        return all

def find_length_n_words(n, board, words):
    for x, y in zip(range(len(board)), range(len(board))):
        words.append(_find_path_helper((x, y), board, n, [], [], WDICT, "word"))
    return words