s="asbuddvbbsabcdeiewjgiwtuvwxyzxmn"
temp = s[0]
long = s[0]
for i in range(1, len(s)):
    if s[i] >= temp[-1]:
        temp += s[i]
        if len(temp) > len(long):
            long = temp
    else:
        temp = s[i]
print "Longest substring in alphabetical order is:" +long
