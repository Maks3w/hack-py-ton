def basic_validation(passphrase: str) -> bool:
    """
    A passphrase consists of a series of words (lowercase letters) separated by spaces.
    To ensure security, a valid passphrase must contain no duplicate words.
    """
    words = passphrase.split(' ')
    return len(words) == len(set(words))


def advanced_validation(passphrase: str) -> bool:
    raise NotImplemented
