# Assignment 4 — Analysis

## Environment and commands

- Programming language: Python
- Operating system: Windows 10 Pro
- Project language selection: Python
- Implementation file: `Python/source/algorithms.py`
- Test command: `py tools/run.py --check`
- Test result: 44/44 tests passed.

The project uses Python dictionaries, lists, sets and the `collections.deque` queue. Sorting is performed using Python's built-in sorting method.

## Algorithm explanations

### 1. LCS (Longest Common Subsequence)

**State:** `dp[i][j]` stores the length of the longest common subsequence of the first `i` characters of two strings.

**Transition:** If the characters are equal, the value is `1 + dp[i-1][j-1]`. Otherwise, it is the maximum of `dp[i-1][j]` and `dp[i][j-1]`.

**Base case:** The first row and first column contain zeros.

**Processing order:** The table is filled from top to bottom and left to right because each cell depends on previous cells.

**Correctness:** The algorithm checks both possibilities: matching characters and skipping one character. Therefore, it finds the optimal subsequence.

**Reconstruction:** The algorithm follows the DP table backwards to build the subsequence. A consistent direction is used when values are equal.

**Complexity:** Time O(n*m), memory O(n*m), where n and m are the lengths of the strings.

**Boundary test:** Two empty strings. The expected LCS length is zero. This checks empty input handling.

### 2. Merge

**State:** `dp[i][j]` stores the minimum cost of merging the interval from index `i` to index `j`.

**Transition:** The interval is divided into two smaller intervals. The algorithm tries every possible split and selects the minimum total cost.

**Base case:** A single element has zero merging cost.

**Processing order:** Shorter intervals are calculated before longer intervals because larger intervals depend on smaller ones.

**Correctness:** Every possible split is considered, so the algorithm can find the minimum total cost.

**Reconstruction:** The selected split points are used to rebuild the merging order. Equal-cost solutions use a consistent tie-breaking rule.

**Complexity:** Time O(n^3), memory O(n^2), where n is the number of elements.

**Boundary test:** An array with one element. The expected cost is zero.

### 3. Tree

**State:** The DP stores two values for each node: the best result when the node is selected and when it is not selected.

**Transition:** If a node is selected, its children cannot be selected. If it is not selected, the best result from each child is used.

**Base case:** A leaf node uses its own weight when selected and zero when not selected.

**Processing order:** Children are processed before their parent so that all required values are ready.

**Correctness:** Every valid solution either includes the current node or excludes it. The two states cover both possibilities.

**Reconstruction:** The stored decisions are used to determine which nodes belong to the optimal solution.

**Complexity:** Time O(V+E), memory O(V), where V is the number of vertices and E is the number of edges.

**Boundary test:** A tree with one node and a negative weight. This checks whether the algorithm correctly handles negative values.

### 4. Naive String Search

**State:** The current index represents the possible starting position of the pattern in the text.

**Transition:** The algorithm compares pattern characters with text characters one by one. If a mismatch occurs, it moves to the next starting position.

**Base case:** An empty pattern is handled according to the problem contract.

**Processing order:** Starting positions are checked from left to right.

**Correctness:** Every possible starting position is checked, so no valid match is missed.

**Reconstruction:** The algorithm returns the positions where the complete pattern matches the text.

**Complexity:** Time O(n*m), memory O(k), where n is text length, m is pattern length and k is the number of returned matches.

**Boundary test:** A pattern longer than the text. The expected result is no matches.

### 5. KMP (Knuth-Morris-Pratt)

**State:** The prefix array stores the length of the longest proper prefix that is also a suffix for each pattern position.

**Transition:** On a mismatch, the algorithm uses the prefix array to move the pattern without repeating unnecessary comparisons.

**Base case:** The first prefix value is zero.

**Processing order:** The prefix array is built from left to right. Then the text is scanned from left to right.

**Correctness:** The prefix information preserves all possible matching prefixes after a mismatch.

**Reconstruction:** The algorithm records the starting position whenever the complete pattern is found. It also supports overlapping matches.

**Complexity:** Time O(n+m), memory O(m+k), where k is the number of matches.

**Boundary test:** Text `aaaaa` and pattern `aaa`. This checks overlapping matches.

### 6. Rabin-Karp (RK)

**State:** The algorithm stores a rolling hash for the current text window and a hash for the pattern.

**Transition:** The hash is updated using base 31 and modulus 101. When the hashes match, the actual characters are compared to verify the candidate.

**Base case:** The first window hash and the pattern hash are calculated before scanning.

**Processing order:** Windows are processed from left to right.

**Correctness:** Hashes help find possible matches, while character verification prevents incorrect results caused by hash collisions.

**Reconstruction:** Verified matching positions are added to the result.

**Complexity:** Rolling hash calculation is O(n+m). With c hash candidates requiring verification, the total time is O(n+m+c*m). The worst case is O(n*m). Extra memory is O(k).

**Boundary test:** A hash collision where two different strings have the same hash. This checks that the algorithm verifies actual characters instead of trusting the hash.

The modulus 101 is deliberately small, so collisions are more frequent than with large production hash moduli. This observation applies to this implementation and does not describe every Rabin-Karp implementation.

### 7. Suffix Array

**State:** The suffix array stores the starting positions of all suffixes in lexicographical order. Each position has a rank.

**Doubling:** The algorithm initially sorts suffixes by their first character. Then it repeatedly sorts them using rank pairs representing twice the previous substring length. The length doubles after each round until all suffixes are ordered.

**Kasai algorithm:** Kasai builds the LCP array. Each LCP value represents the common prefix length of two neighboring suffixes in the suffix array. It reuses previous comparisons to avoid unnecessary work.

**Base case:** Each suffix initially receives a rank based on its first character.

**Processing order:** Doubling processes increasing substring lengths. Kasai processes suffix positions while maintaining the previous common-prefix information.

**Correctness:** Doubling eventually compares enough characters to distinguish all suffixes. Kasai correctly calculates the common prefix of neighboring sorted suffixes.

**Reconstruction:** The suffix array provides the sorted order of suffix starting positions, and the LCP array provides common-prefix information.

**Complexity:** With comparison-based sorting in each doubling round, time is O(n log^2 n). Kasai takes O(n). Memory is O(n).

**Boundary test:** A string containing repeated characters. This checks correct suffix ordering and LCP values.

### 8. Aho-Corasick

**State:** The algorithm uses a trie containing all patterns. Each node stores transitions, a failure link and pattern information.

**Transition:** Failure links are created using BFS. During text scanning, the algorithm follows trie transitions or failure links when a character does not match.

**Base case:** The root node has no parent and starts the automaton.

**Processing order:** The trie is built first. Failure links are calculated in BFS order, so the required shorter failure states are already available.

**Correctness:** Failure links preserve the longest valid suffix that is also a trie prefix. Therefore, the automaton can find all pattern matches, including overlapping and suffix-pattern matches.

**Reconstruction:** Match counts are collected at visited nodes and propagated through failure links in reverse BFS order. Duplicate patterns are handled using their terminal pattern information. The automaton state is reset before processing a new independent text.

**Complexity:** Building the trie and failure links takes O(P), where P is the total number of pattern characters. Text processing takes O(n). Count propagation and result construction take O(V+p), where V is the number of trie nodes and p is the number of patterns. Memory is O(V+p).

**Boundary test:** Patterns with duplicates and suffix relationships. This checks duplicate counts, suffix matches and correct state reset.

## Search comparison

All three algorithms were tested using the same text and pattern for each case.

- Algorithms: Naive, KMP and Rabin-Karp.
- Text sizes: 500, 1500 and 3000 characters.
- Pattern length: 30 characters.
- Random generator: Python random module, seed 42, alphabet `abcd`.
- Repetitive generator: text and pattern contain only `a`.
- Number of measured runs: 3 per algorithm, size and case.
- Timing unit: milliseconds (ms).
- Timing method: `time.perf_counter()`.
- Warm-up: No separate warm-up was used.
- JIT: No JIT compilation was used; Python ran normally.
- Timing scope: Only the algorithm function call was measured. Input generation and correctness comparison were excluded.
- Correctness: All three algorithms returned identical results for every tested input.

### Raw measurements

| Case | n | m | Algorithm | Run 1 | Run 2 | Run 3 | Median (ms) |
|---|---:|---:|---|---:|---:|---:|---:|
| Random | 500 | 30 | Naive | 0.1402 | 0.0824 | 0.0779 | 0.0824 |
| Random | 500 | 30 | KMP | 0.0782 | 0.0780 | 0.0799 | 0.0782 |
| Random | 500 | 30 | RK | 0.1552 | 0.1081 | 0.1024 | 0.1081 |
| Random | 1500 | 30 | Naive | 0.1991 | 0.2132 | 0.2022 | 0.2022 |
| Random | 1500 | 30 | KMP | 0.1771 | 0.1758 | 0.1747 | 0.1758 |
| Random | 1500 | 30 | RK | 0.3380 | 0.3201 | 0.3184 | 0.3201 |
| Random | 3000 | 30 | Naive | 0.4217 | 0.4218 | 0.4245 | 0.4218 |
| Random | 3000 | 30 | KMP | 0.3639 | 0.3618 | 0.3644 | 0.3639 |
| Random | 3000 | 30 | RK | 0.6323 | 0.6394 | 0.6327 | 0.6327 |
| Repetitive | 500 | 30 | Naive | 1.2115 | 1.1856 | 1.1479 | 1.1856 |
| Repetitive | 500 | 30 | KMP | 0.2508 | 0.2426 | 0.2312 | 0.2426 |
| Repetitive | 500 | 30 | RK | 0.9703 | 0.9595 | 0.9558 | 0.9595 |
| Repetitive | 1500 | 30 | Naive | 3.6877 | 4.0485 | 3.7953 | 3.7953 |
| Repetitive | 1500 | 30 | KMP | 0.3479 | 0.3698 | 0.3203 | 0.3479 |
| Repetitive | 1500 | 30 | RK | 3.0067 | 3.0175 | 4.0679 | 3.0175 |
| Repetitive | 3000 | 30 | Naive | 7.2917 | 7.1991 | 7.3712 | 7.2917 |
| Repetitive | 3000 | 30 | KMP | 0.6873 | 0.6518 | 0.6347 | 0.6518 |
| Repetitive | 3000 | 30 | RK | 7.1163 | 6.0561 | 5.9208 | 6.0561 |

### Observations

For random inputs, all three algorithms performed relatively quickly. KMP was the fastest in these measurements.

For repetitive inputs, Naive and Rabin-Karp became significantly slower because many positions required additional character comparisons. KMP handled repetitive inputs more efficiently.

Rabin-Karp uses base 31 and modulus 101. This small modulus can produce more hash collisions, which increase the number of character verifications. Actual character comparison is necessary to guarantee correct results.

These measurements show the performance of this implementation on the tested inputs. They do not prove theoretical complexity.

The benchmark results are also saved in `benchmark_results.txt`.

## Sources and AI assistance

- AI assistance was used to help understand algorithm concepts