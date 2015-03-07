s="asbuddvbbsabdgkmpqcdeiewjgiwtuvwxyzxmn"

def longalpha(s):
    t=s[0]; l=s[0]
    for i in range(1,len(s)):
        if s[i]>=t[-1]:
            t+=s[i]
            if len(t)>len(l): l=t
        else: t=s[i]
    return l

print "Longest substring in alphabetical order is:",longalpha(s)
