import re

import javscraper

guesser_regex: dict[str, re.Pattern] = {
    's1': re.compile(r'^(?:ssis|ssni|sivr|ofje)[\d\s-]', re.IGNORECASE),
    'sod': re.compile(r'^(?:stars?|sdnm|sdmm|sddr|sdab|sdjs|sdde|sdmu|mogi|dsvr|mfsh)[\d\s-]', re.IGNORECASE),

    'fc2': re.compile(r'fc2(?:-ppv)?', re.IGNORECASE),
    '1pondo': re.compile(r'1pondo', re.IGNORECASE),
    'carib': re.compile(r'carib', re.IGNORECASE),
    'heyzo': re.compile(r'\d{4}', re.IGNORECASE),
}

extractor_regex = {
    '1pondo': re.compile(r'(\d{6})[ -_](\d{3})'),
    'heyzo': re.compile(r'(?:heyzo)?-?(\d{3,})', re.IGNORECASE),
    'general': re.compile(r'((?:[A-Za-z]{2,6})|(?:t-?28))(?: |-|_)?(\d+)(e|z)?', re.IGNORECASE)
}


def normalize_code(scraper_type, code: str) -> str:
    if scraper_type == javscraper.Caribbeancom:
        return code
    if scraper_type == javscraper.Heyzo:
        groups = extractor_regex['heyzo'].search(code)
        if groups is not None:
            return "Heyzo-{}".format(groups.group(1))
        return code
    if scraper_type == javscraper.OnePondo:
        groups = extractor_regex['1pondo'].search(code)
        if groups is not None:
            return "{}_{}".format(*groups.group(1, 2))

    return normalize_general_name(code)


def normalize_general_name(code: str) -> str:
    groups = extractor_regex['general'].search(code)
    if groups is None:
        return code

    return "{}-{}{}".format(
        groups.group(1).replace('-', '').upper(),
        str(int(groups.group(2))).zfill(3),
        groups.group(3) or '',
    )
