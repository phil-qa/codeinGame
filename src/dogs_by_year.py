'''
According to the conventions in France for pedigree dogs, their first letter of the name
Is relative to the year they are registered
u=2003, v=2004, a=2005, b=2006 etal

'''

Y = "UVABCDEFGHIJLMNOPRST"
n = int(input())
c = Counter()

for i in range(n):
    name = input()
    c[2003 + Y.index(name[0])] += 1



for x in sorted(c):
    print(x, c[x])