import timeit

def boyer_moore(text, pattern):
    m, n = len(pattern), len(text)
    bad_char = {pattern[i]: i for i in range(m)}

    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return True
        s += max(1, j - bad_char.get(text[s + j], -1))
    return False


def kmp_search(text, pattern):
    def lps_array(p):
        lps = [0] * len(p)
        length = 0
        i = 1
        while i < len(p):
            if p[i] == p[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                length = lps[length - 1] if length else 0
                if length == 0:
                    lps[i] = 0
                    i += 1
        return lps

    lps = lps_array(pattern)
    i = j = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == len(pattern):
            return True
        elif i < len(text) and text[i] != pattern[j]:
            j = lps[j - 1] if j else 0
            if j == 0:
                i += 1
    return False


def rabin_karp(text, pattern):
    d = 256
    q = 101
    m, n = len(pattern), len(text)

    if m > n:
        return False

    h = pow(d, m - 1) % q
    p = t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t and text[i:i + m] == pattern:
            return True
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q

    return False


def measure(func, text, pattern, number=10):
    return timeit.timeit(lambda: func(text, pattern), number=number)


def run_tests(text, text_name):
    existing_pattern = text[100:130]
    fake_pattern = "qwertyuiopasdfgh"

    algorithms = [
        ("Boyer–Moore", boyer_moore),
        ("KMP", kmp_search),
        ("Rabin–Karp", rabin_karp)
    ]

    print(f"\n Текст: {text_name}")
    print("-" * 50)

    for pattern_name, pattern in [
        ("Існуючий підрядок", existing_pattern),
        ("Вигаданий підрядок", fake_pattern)
    ]:
        print(f"\n{pattern_name}")
        for alg_name, alg in algorithms:
            time = measure(alg, text, pattern)
            print(f"{alg_name:<15}: {time:.6f} сек")


def main():
    with open("article1.txt", encoding="utf-8") as f:
        text1 = f.read()

    with open("article2.txt", encoding="utf-8") as f:
        text2 = f.read()
    
    run_tests(text1, "Article 1")
    run_tests(text2, "Article 2")


if __name__ == "__main__":
    main()
