def load_english_words(min_len=5, dictionary_path='/usr/share/dict/words'):
    word_set = set()
    with open(dictionary_path, encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if len(word) >= min_len:
                word_set.add(word)
    return word_set


ENGLISH_WORDS = load_english_words()


def is_strong_password(password):
    pass_lower = password.lower()

    for i in range(len(pass_lower)):
        for j in range(i + 5, len(pass_lower) + 1):
            if pass_lower[i:j] in ENGLISH_WORDS:
                return False
    return True
