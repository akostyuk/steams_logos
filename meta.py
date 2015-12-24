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
        'NBL_Canada': 'NBACAN',
    },
    'hockey': {
        'Sweden_SEL': 'SELSWE',
        'Finnish_SMliiga': 'SMLIIGAFIN',
        'Aus-HL': 'HLAUT',
        'German_DEL': 'DELDEU',
        'British_EIHL': 'EIHLGBR',
        'Czech_ELH': 'ELHCZE',
        'Mestis': 'MESTISFIN',
        'Swiss_NLA': 'NLACHE',
        'Russia_VHL': 'VHLRUS',
        'Slovak_Ex-Liga': 'EXLSVK',
    },
    'football': {
        'Arena_FL': 'FLARENA',
        'LFL_Canada': 'LFLCAN',
    }
}

# exclude leagues without teams

EXCLUDES = {
    'baseball': [
        'major league baseball',
        'minor league baseball',
    ]
}
