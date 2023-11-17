def solution(start, length):
    ans = 0
    for l in xrange(length - 1, -1, -1):
        b = start + l
        if start == 0:
            xor = (b, 1, b + 1, 0)[b % 4]
        else:
            xor = (b, 1, b + 1, 0)[b % 4] ^ (start-1, 1, start, 0)[(start-1) % 4]
        ans ^= xor
        start += length
    return ans