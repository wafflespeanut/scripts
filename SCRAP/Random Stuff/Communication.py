import random
nameList = range(1, 43)

def calls(people = nameList):           # This is still an exhaustive way - goes as O(n^2)
    num = len(people)
    assigned = dict(zip(people,[[] for i in people]))
    noluck = False
    if num < 2:
        print 'We need at least two fellas to have an inter-chat!'
    total = (num * (num - 1)) / 2
    lowerLimit = total / num
    print 'Calls to be made:', total
    print 'Minimum calls per user:', lowerLimit
    if total % num:
        noluck = total % num            # Notice that also, noluck = len(people) / 2
        print 'Status: Unbalanced (%s unlucky users gotta make an extra call!)' % noluck
    else:
        print 'Status: Balanced (Equal calls for everyone!\n'
    random.shuffle(people)
    for person1 in people:
        count = 0
        for person2 in people:
            if all([person1 is not person2, person1 not in assigned[person2], person2 not in assigned[person1]]):
                assigned[person1].append(person2)
                count += 1
            if count == lowerLimit:
                break
    if noluck:
        unlucky = []
        for person1 in people:
            for person2 in people:
                if all([person1 is not person2, person2 not in assigned[person1], person1 not in assigned[person2]]):
                    assigned[person1].append(person2)
                    unlucky.append(person1)
                if len(unlucky) == noluck:
                    break
        print 'Unlucky users: %s\n' % unlucky
    for person in assigned:
        print '%s:\t%s' % ([person], ', '.join([str(i) for i in assigned[person]]))
