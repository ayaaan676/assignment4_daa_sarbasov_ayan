import random
import statistics
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "Python" / "source"))

from algorithms import naive, kmp, rk


def run_benchmark():
    sizes = [500, 1500, 3000]
    cases = ["random", "repetitive"]
    seed = 42
    random.seed(seed)

    for case in cases:
        for n in sizes:
            m = min(30, n)
            if case == "random":
                text = ''.join(random.choices("abcd", k=n))
                pattern = ''.join(random.choices("abcd", k=m))
            else:
                text = "a" * n
                pattern = "a" * m

            print(f"\nCase={case}, n={n}, m={m}, seed={seed}")

            expected = None

            for name, algorithm in [
                ("Naive", naive),
                ("KMP", kmp),
                ("RK", rk),
            ]:
                request = {"text": text, "pattern": pattern}

                result = algorithm(request)

                if expected is None:
                    expected = result
                elif result != expected:
                    raise AssertionError(f"{name} returned incorrect output")

                times = []

                for _ in range(3):
                    start = time.perf_counter()
                    algorithm(request)
                    elapsed = (time.perf_counter() - start) * 1000
                    times.append(elapsed)

                print(
                    f"{name}: "
                    f"runs={[round(x, 4) for x in times]}, "
                    f"median={statistics.median(times):.4f} ms, "
                    f"correct=True"
                )


if __name__ == "__main__":
    run_benchmark()