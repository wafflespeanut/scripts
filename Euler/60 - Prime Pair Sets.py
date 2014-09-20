execfile("49 - Prime Permutations.py")

def check(arr):
    for i in arr:
        for j in arr:
            if i!=j:
                if int(str(i)+str(j)) in z:
                    if int(str(i)+str(j)) not in z: return False
                else: return False
    return True

