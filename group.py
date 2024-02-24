import difflib

from collections import defaultdict

from deep_translator import GoogleTranslator


def groups_to_names(data, grouped_addresses):
    """Mapping grouped addresses to names"""
    address_groups_to_names = defaultdict(list)
    for name, address in data:
        for group in grouped_addresses:
            if address in group:
                address_groups_to_names[group].append(name)
                break
    return address_groups_to_names


def group_addresses(addresses):
    """Grouping addresses by matches"""
    grouped_addresses, group_cache = set(), []
    for address in addresses:
        # not English lang
        if not bool(address.isascii()):
            translated_address = GoogleTranslator(source='auto', target='en').translate(address)
            matched_eng = difflib.get_close_matches(translated_address, addresses)
            # translated text grouping
            if matched_eng and tuple(matched_eng) in grouped_addresses:
                grouped_addresses.remove(tuple(matched_eng))
                group_cache.append(matched_eng.copy())
                matched_eng.append(address)
                grouped_addresses.add(tuple(matched_eng))
            elif tuple(matched_eng) not in grouped_addresses:
                grouped_addresses.add(tuple(matched_eng))
            elif not matched_eng:
                grouped_addresses.add(tuple(translated_address))
        else:
            # non translated text grouping
            matched = sorted(difflib.get_close_matches(address, addresses))
            if matched and matched not in group_cache:
                grouped_addresses.add(tuple(matched))
            elif not matched:
                grouped_addresses.add(tuple(address))
    return grouped_addresses
