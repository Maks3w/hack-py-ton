def basic_validation(passphrase: str) -> bool:
    """
    A passphrase consists of a series of words (lowercase letters) separated by spaces.
    To ensure security, a valid passphrase must contain no duplicate words.
    """
    words = passphrase.split(' ')
    return len(words) == len(set(words))


def advanced_validation(passphrase: str) -> bool:
    """
    A valid passphrase must contain no two words that are anagrams of each other - that is,
    a passphrase is invalid if any word's letters can be rearranged to form any other word in
    the passphrase.
    """
    words = passphrase.split(' ')
    # Normalize each word before unique check
    return len(words) == len(set(map(lambda w: ''.join(sorted(w)), words)))
