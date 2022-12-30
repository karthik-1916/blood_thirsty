def extract_subs(queue):
    subdomains = []
    for q in range(queue.qsize()):
        subs = queue.get()
        for sub in subs:
            if '*' not in sub:
                if 'crowdstrike' in sub:
                    subdomains.append(sub)

    return subdomains
