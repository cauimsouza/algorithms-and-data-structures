def sort_characters(s: str) -> tuple[list[int], list[int]]:
    n = len(s)

    ALPHABET_SIZE = 256
    count = [0] * ALPHABET_SIZE
    for c in s:
        count[ord(c)] += 1
    for i in range(1, ALPHABET_SIZE):
        count[i] += count[i - 1]
    order = [0] * n
    for i, c in enumerate(s):
        count[ord(c)] -= 1
        order[count[ord(c)]] = i

    rank, curr_rank = [0] * n, 0
    for i in range(1, n):
        if s[order[i]] == s[order[i - 1]]:
            rank[order[i]] = curr_rank
        else:
            curr_rank += 1
            rank[order[i]] = curr_rank
    
    return order, rank

def build_suffix_array_simple(s: str) -> list[int]:
    ''''Builds suffix array in O(n log^2 n) time.
    
    's' must contain only letters from the English alphabet.
    '''

    if not s:
        return []

    s += '$'
    n = len(s)

    order, rank = sort_characters(s)
    size = 1
    # Before each iteration, the suffixes are sorted in ascending order based on the first 'size' characters.
    # order[i]: index of the i-th smallest suffix
    # class_[i]: equivalence class of the suffix starting at s[i]
    while size < n:
        aux_order = sorted(((rank[i], rank[(i + size) % n], i) for i in range(n)))

        rank, curr_rank = [0] * n, 0
        for j in range(n):
            i = aux_order[j][2]
            order[j] = i

            if j > 0 and aux_order[j][:2] == aux_order[j - 1][:2]:
                rank[i] = curr_rank
            else:
                curr_rank += 1
                rank[i] = curr_rank

        size *= 2
    
    return order[1:] # Ignore the (also smallest) dummy suffix '$'

def build_suffix_array(s: str) -> list[int]:
    ''''Builds suffix array in O(n log n) time.
    
    's' must contain only letters from the English alphabet.
    '''

    if not s:
        return []

    # The algorithm below actually sorts the cyclic shifts of the string s.
    # To actually sort the suffixes of s, we append a character that is
    # smaller than any character of s.
    s += '$'
    n = len(s)

    order, rank = sort_characters(s)

    # We iterate floor(log n) times. In the i-th iteration (1-based), we sort substrings of length 2^i in O(n) time,
    # thus achieving a total time complexity of O(n log n). Space complexity is O(n).
    # Invariant: Before each iteration, the substrings are sorted in ascending order based on the first 'size' characters.
    # order[i]: index of the i-th smallest substring of length 'size'
    # class_[i]: equivalence class of the substring of length 'size' starting at s[i]
    size = 1
    while size < n:
        # We sort the substrings of length 2^k by sorting the pairs (class[i], class[i + 2^(k-1)]).
        # We use counting sort, sorting first by the second element of the pairs then (with a stable sort) by the first.
        # Counting sort ensures the sorting takes O(n) time.

        # To sort by the second element, notice that if the smallest substring of length 2^(k-1) starts at index i, then
        # the substring of length 2^k with the smallest second half starts at index i - 2^(k-1).
        sec_order = [0] * n
        for j in range(n):
            i = (order[j] - size) % n
            sec_order[j] = i
        
        # Counting sort on the first element, stable relative to the order of the first elements (sec_order).
        count = [0] * n # Equivalence classes are always between 0 and n - 1.
        for i in range(n):
            count[rank[i]] += 1
        start = [0] * n
        for j in range(1, n):
            start[j] = start[j - 1] + count[j - 1]
        new_order = [0] * n
        for i in sec_order:
            pos = start[rank[i]]
            start[rank[i]] += 1
            new_order[pos] = i
        order = new_order

        new_rank, curr_rank = [0] * n, 0
        for j in range(1, n):
            i = order[j]
            prev = order[j - 1]

            if (rank[i], rank[(i + size) % n]) == (rank[prev], rank[(prev + size) % n]):
                new_rank[i] = curr_rank
            else:
                curr_rank += 1
                new_rank[i] = curr_rank
        rank = new_rank

        size *= 2
    
    return order[1:] # Ignore the (also smallest) dummy suffix '$'

if __name__ == '__main__':
    print(build_suffix_array('aaba'))