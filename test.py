def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start+n]


nums = "Abhi shek pand ey"
for chunk in chunks(nums, 4):
    print(chunk)