from django import template

register = template.Library()

CENSORSHIP = [
    'instagram',
    'facebook',
]


@register.filter()
def censor(value: str):
    if not isinstance(value, str):
        raise TypeError('фильтр должен применяться к строковому выражению')

    result = value
    for c in CENSORSHIP:
        pieces = result.upper().split(c.upper())
        puzzle = ''
        for piece in pieces:
            puzzle += result[len(puzzle):len(puzzle) + len(piece)]
            swear_word = result[len(puzzle):len(puzzle) + len(c)]
            puzzle += swear_word[0] + '*' * (len(swear_word) - 1) if len(swear_word) > 0 else ''
        result = puzzle
    return result
