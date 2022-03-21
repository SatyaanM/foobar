def solution(l):
    n = len(l)
    for i in range(n-1):
        for j in range(0, n-i-1):
            first = [int(x) for x in l[j].split('.')]
            second = [int(x) for x in l[j+1].split('.')]

            if first[0] > second[0]:
                l[j], l[j+1] = l[j+1], l[j]
            elif first[0] == second[0]:
                if (len(first) == 1 and len(second) > 1):
                    pass
                elif (len(first) > 1 and len(second) == 1):
                    l[j], l[j+1] = l[j+1], l[j]
                else:
                    if first[1] > second[1]:
                        l[j], l[j+1] = l[j+1], l[j]
                    elif first[1] == second[1]:
                        if (len(first) == 2 and len(second) > 2):
                            pass
                        elif (len(first) > 2 and len(second) == 2):
                            l[j], l[j+1] = l[j+1], l[j]
                        else:
                            if (first[2] > second[2]):
                                l[j], l[j+1] = l[j+1], l[j]
    return l
            

print(solution(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]))
# # returns 0.1, 1.1.1, 1.2, 1.2.1, 1.11, 2, 2.0, 2.0.0
print(solution(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"]))
# # returns 1.0, 1.0.2, 1.0.12, 1.1.2, 1.3.3
