
"""Implement algorithm bodies. See docs/guide/CONTRACTS.md; inputs and outputs are dictionaries."""

from collections import deque


def lcs(request):
    a = request["a"]
    b = request["b"]
    n, m = len(a), len(b)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    result = []
    i, j = n, m

    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result.reverse()

    return {
        "length": dp[n][m],
        "sequence": "".join(result)
    }


def merge(request):
    sizes = request["sizes"]
    n = len(sizes)

    if n <= 1:
        return {"cost": 0, "plan": []}

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + sizes[i]

    dp = [[0] * n for _ in range(n)]
    split = [[-1] * n for _ in range(n)]

    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            best = None

            for k in range(left, right):
                cost = (
                    dp[left][k]
                    + dp[k + 1][right]
                    + prefix[right + 1]
                    - prefix[left]
                )

                if best is None or cost < best:
                    best = cost
                    split[left][right] = k

            dp[left][right] = best

    plan = []

    def build(left, right):
        if left == right:
            return

        k = split[left][right]

        build(left, k)
        build(k + 1, right)

        plan.append([left, k, right])

    build(0, n - 1)

    return {
        "cost": dp[0][n - 1],
        "plan": plan
    }


def tree(request):
    n = request["n"]
    weights = request["weights"]
    edges = request["edges"]

    if n == 0:
        return {"weight": 0, "selected": []}

    adj = [[] for _ in range(n)]

    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    parent = [-1] * n
    order = []
    stack = [0]
    parent[0] = -2

    while stack:
        v = stack.pop()
        order.append(v)

        for u in adj[v]:
            if u != parent[v]:
                parent[u] = v
                stack.append(u)

    take = [0] * n
    skip = [0] * n

    for v in reversed(order):
        take[v] = weights[v]
        skip[v] = 0

        for u in adj[v]:
            if parent[u] == v:
                take[v] += skip[u]
                skip[v] += max(take[u], skip[u])

    selected = []
    reconstruction = [(0, False)]

    while reconstruction:
        v, parent_taken = reconstruction.pop()

        choose = not parent_taken and take[v] > skip[v]

        if choose:
            selected.append(v)

        for u in adj[v]:
            if parent[u] == v:
                reconstruction.append((u, choose))

    return {
        "weight": max(take[0], skip[0]),
        "selected": selected
    }


def naive(request):
    text = request["text"]
    pattern = request["pattern"]

    n = len(text)
    m = len(pattern)

    if m == 0:
        return {"positions": list(range(n + 1))}

    if m > n:
        return {"positions": []}

    positions = []

    for i in range(n - m + 1):
        j = 0

        while j < m and text[i + j] == pattern[j]:
            j += 1

        if j == m:
            positions.append(i)

    return {"positions": positions}


def kmp(request):
    text = request["text"]
    pattern = request["pattern"]

    n = len(text)
    m = len(pattern)

    if m == 0:
        return {"positions": list(range(n + 1))}

    if m > n:
        return {"positions": []}

    pi = [0] * m
    j = 0

    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        pi[i] = j

    positions = []
    j = 0

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == m:
            positions.append(i - m + 1)
            j = pi[j - 1]

    return {"positions": positions}


def rk(request):
    text = request["text"]
    pattern = request["pattern"]

    n = len(text)
    m = len(pattern)

    if m == 0:
        return {"positions": list(range(n + 1))}

    if m > n:
        return {"positions": []}

    base = 31
    mod = 101

    highest_power = pow(base, m - 1, mod)

    pattern_hash = 0
    window_hash = 0

    for i in range(m):
        pattern_hash = (
            pattern_hash * base + ord(pattern[i])
        ) % mod

        window_hash = (
            window_hash * base + ord(text[i])
        ) % mod

    positions = []

    for start in range(n - m + 1):
        if window_hash == pattern_hash:
            match = True

            for j in range(m):
                if text[start + j] != pattern[j]:
                    match = False
                    break

            if match:
                positions.append(start)

        if start < n - m:
            window_hash = (
                (window_hash - ord(text[start]) * highest_power)
                * base
                + ord(text[start + m])
            ) % mod

    return {"positions": positions}


def suffix(request):
    text = request["text"]
    n = len(text)

    if n == 0:
        return {
            "sa": [],
            "lcp": [],
            "repeated": ""
        }

    sa = list(range(n))
    rank = [ord(c) for c in text]
    k = 1

    while k < n:
        sa.sort(
            key=lambda i: (
                rank[i],
                rank[i + k] if i + k < n else -1
            )
        )

        new_rank = [0] * n

        for i in range(1, n):
            prev = sa[i - 1]
            curr = sa[i]

            prev_pair = (
                rank[prev],
                rank[prev + k] if prev + k < n else -1
            )

            curr_pair = (
                rank[curr],
                rank[curr + k] if curr + k < n else -1
            )

            new_rank[curr] = (
                new_rank[prev] + (prev_pair != curr_pair)
            )

        rank = new_rank

        if rank[sa[-1]] == n - 1:
            break

        k *= 2

    lcp = [0] * n
    inverse = [0] * n

    for i, pos in enumerate(sa):
        inverse[pos] = i

    common = 0

    for i in range(n):
        r = inverse[i]

        if r == 0:
            common = 0
            continue

        j = sa[r - 1]

        while (
            i + common < n
            and j + common < n
            and text[i + common] == text[j + common]
        ):
            common += 1

        lcp[r] = common

        if common > 0:
            common -= 1

    best_length = max(lcp)
    best_index = lcp.index(best_length)

    repeated = (
        text[sa[best_index]:sa[best_index] + best_length]
        if best_length > 0 else ""
    )

    return {
        "sa": sa,
        "lcp": lcp,
        "repeated": repeated
    }


def aho(request):
    patterns = request["patterns"]
    texts = request["texts"]

    p = len(patterns)

    if p == 0:
        return {"counts": [[] for _ in texts]}

    # Trie transitions, failure links and BFS order.
    transitions = [{}]
    fail = [0]
    terminal = []

    for pattern in patterns:
        state = 0

        for ch in pattern:
            if ch not in transitions[state]:
                transitions[state][ch] = len(transitions)
                transitions.append({})
                fail.append(0)

            state = transitions[state][ch]

        terminal.append(state)

    queue = deque()
    bfs_order = [0]

    for child in transitions[0].values():
        fail[child] = 0
        queue.append(child)

    while queue:
        v = queue.popleft()
        bfs_order.append(v)

        for ch, u in transitions[v].items():
            f = fail[v]

            while f != 0 and ch not in transitions[f]:
                f = fail[f]

            fail[u] = transitions[f].get(ch, 0)
            queue.append(u)

    results = []

    for text in texts:
        visits = [0] * len(transitions)
        state = 0

        for ch in text:
            while state != 0 and ch not in transitions[state]:
                state = fail[state]

            state = transitions[state].get(ch, 0)
            visits[state] += 1

        # Propagate each state's visits to its failure state.
        for v in reversed(bfs_order[1:]):
            visits[fail[v]] += visits[v]

        results.append([visits[state] for state in terminal])

    return {"counts": results}
