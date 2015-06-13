import random
nameList = []

def calls(people = nameList):           # This is still an exhaustive way
    num = len(people)
    assigned = dict(zip(people,[[] for i in people]))
    noluck = False
    if num < 2:
        print 'We need at least two fellas to have an inter-chat!'
    total = (num * (num - 1)) / 2
    lowerLimit = total / num
    print total, 'calls have to be made! Each user has to make at least', lowerLimit, 'calls!'
    if total % num:
        noluck = total % num            # Notice that also, noluck = len(people) / 2
        print '\nUnequalized calls!', noluck, 'unlucky users who gotta make an extra call!'
    else:
        print '\nBalanced calls...'
    for person in people:
        count = 0
        while count < lowerLimit:
            choice = random.choice(range(0,len(people)))
            if people[choice] is not assigned[person]:
                if people[choice] not in assigned[person]:
                    if person not in assigned[people[choice]]:
                        assigned[person].append(people[choice])
                        count += 1
    return assigned
