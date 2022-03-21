def solution(s):
    # Your code here
    part = ""
    num_equal = []
    for i in range(len(s)):
        part += s[i]
        if (len(part) * s.count(part) == len(s)):
            num_equal.append(s.count(part))
    return max(num_equal)


# solution("abcabcabcabc")
# solution("abccbaabccba")
print(solution("abcabcabcabc"))
print(solution("abccbaabccba"))
