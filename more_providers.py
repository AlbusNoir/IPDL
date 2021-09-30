from pydnsbl.providers import Provider

plist = []

with open('providers.txt') as f:
    for line in f:
        plist.append(line.rstrip())


more_providers = list(map(Provider, plist))