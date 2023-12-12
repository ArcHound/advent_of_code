def binom(n, k):
    prod = 1
    if k > n:
        return 0
    for i in range(k):
        prod = (prod * (n - (k - 1 - i))) // (i + 1)
    return prod


def buckles(elements, choice_length, comb_index):
    # get i-th combination of selected length from elements
    # everything is zero indexed
    # https://dl.acm.org/doi/pdf/10.1145/355732.355739
    if elements < choice_length:
        # Too many pidgeons!
        return None
    elif comb_index > binom(elements, choice_length):
        # Combination index bigger than binom(n,k)
        return None
    else:
        combination = [0] * choice_length
        if choice_length == 1:
            combination[0] = comb_index
            return combination
        i = 1
        r = binom(elements - i, choice_length - 1)
        k = r
        while k <= comb_index:
            i += 1
            r = binom(elements - i, choice_length - 1)
            k += r
        k -= r
        combination[0] = i - 1

        for j in range(2, choice_length):
            i += 1
            r = binom(elements - i, choice_length - j)
            k += r
            while k <= comb_index:
                i += 1
                r = binom(elements - i, choice_length - j)
                k += r
            k -= r
            combination[j - 1] = i - 1
        combination[choice_length - 1] = i + comb_index - k
        return combination
