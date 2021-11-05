lines1 = [line.rstrip('\r\n') for line in open("output.txt")]
lines2 = [line.rstrip('\r\n') if line[0] != "%" else None for line in open("xwr68xx_profile_2021_10_24T03_23_44_468.cfg")]
lines2 = list(filter(None, lines2))
#print(lines1)
for i, v in enumerate(lines1):
    if v != lines2[i]:
        print([v, lines2[i]])