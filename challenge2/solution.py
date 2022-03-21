import itertools


def solution(l):
    max = 0
    l.sort(reverse=True)
    for L in range(len(l)+1, 0, -1):
        for subset in itertools.combinations(l, L):
            x = int(''.join(str(e) for e in subset))
            if (x > max and x % 3 == 0):
                max = x
            if x < max:
                break
    return max

print(solution([3, 1, 4, 1]))
print(solution([3, 1, 4, 1, 5, 9]))
