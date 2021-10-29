from pydnsbl.providers import Provider
import os

plist = []

ap_exists = os.path.exists('all_providers.txt')

if ap_exists:
    with open('all_providers.txt', 'r') as f1, open('providers.txt', 'a') as f2:
        for line in f1:
            f2.write(line)


# providers.txt will ALWAYS exist, all_providers will not
with open('providers.txt') as f2:
    for line in f2:
        plist.append(line.rstrip())


more_providers = list(map(Provider, plist))


# could probably use shutil to do this but eh simplicity