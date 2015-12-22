# abbreviation replacements

REPLACES = {
    'baseball': {
        'Korean_KBO': 'KKBO',
        'Japanese_NPB': 'JNPB',
        'Can-Am_': 'CAL',
    },
    'basketball': {
        'NBA_D-League': 'NBADL',
        'NBL-Aus': 'NBLAUS',
        'NBL_Canada': 'NBACA',
    }
}

# exclude leagues without teams

EXCLUDES = {
    'baseball': [
        'major league baseball',
        'minor league baseball',
    ]
}
