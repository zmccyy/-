"""Fill in the solution cells of the two homework notebooks (by cell index).

Run from the homework root:  python tools/fill_solutions.py
Kept as a record of what was filled in for the 2026-10-12 FFT / closest-pair assignment.
"""
import json
import os
import sys

FFT_SOLUTIONS = {
    5: '''def roots_of_unities(n):
    """
    args:
        n:int = n describes which root of unity to return
    return:
        a list of n complex numbers containing the n-th roots of unity [w^0, w^1, w^2, ..., w^{n-1}]
    """
    # w = e^{2*pi*i/n} is the principal n-th root of unity, so the roots in
    # order are [w^0, w^1, ..., w^{n-1}].
    return np.exp(2j * np.pi * np.arange(n) / n)
''',
    11: '''def dft_naive(coeffs):
    """
    args:
        coeffs:np.array = list of numbers representing the coefficients of a polynomial where coeffs[i]
                    is the coeffiecient of the term x^i
    return:
        List containing the results of evaluating the polynomial at the roots of unity. Can be either a list or np.array
        [P(w_0), P(w_1), P(w_2), ...]
    """
    coeffs = np.asarray(coeffs, dtype=complex)
    n = len(coeffs)
    roots = roots_of_unities(n)
    powers = np.arange(n)
    # P(w_j) = sum_k coeffs[k] * w_j^k, computed naively for every root (O(n^2)).
    return np.array([np.sum(coeffs * roots[j] ** powers) for j in range(n)])
''',
    17: '''def fft(coeffs, roots):
    """
    args:
        coeffs (np.array): array of numbers representing the coefficients of a polynomial where coeffs[i]
                    is the coeffiecient of the term x^i
        roots (np.array): array containing the roots of unity [w_0, w_1, w_2, ..., w_{n-1}]
    return:
        List containing the results of evaluating the polynomial at the roots of unity
        [P(w_0), P(w_1), P(w_2), ...]
    """
    n = len(coeffs)
    assert n == hyperceil(n)
    coeffs = np.asarray(coeffs, dtype=complex)
    roots = np.asarray(roots, dtype=complex)

    if n == 1:
        return coeffs

    # Split P into its even and odd parts: P(x) = E(x^2) + x * O(x^2).
    even = fft(coeffs[0::2], roots[0::2])
    odd = fft(coeffs[1::2], roots[0::2])

    # (w^k)^2 = w^{2k} = roots[2k], so the half-sized problem uses roots[::2].
    # For the top half of the roots, w^{k + n/2} = -w^k.
    half = n // 2
    return np.concatenate((even + roots[:half] * odd, even + roots[half:] * odd))
''',
    26: '''def ifft(vals, roots):
    """
    args:
        val (np.array): numpy array containing the results of evaluating the polynomial at the roots of unity
                    [P(w_0), P(w_1), P(w_2), ...]

        roots (np.array): numpy array containing the roots of unity [w_0, w_1, w_2, ..., w_{n-1}]

    return:
        List containing the results of evaluating the polynomial at the roots of unity. Can be a Python list
            or numpy array.
        [P(w_0), P(w_1), P(w_2), ...]
    """
    n = len(vals)
    assert n == hyperceil(n)
    roots = np.asarray(roots, dtype=complex)
    # The inverse DFT is the DFT with w replaced by w^{-1}, scaled by 1/n:
    # w^{-k} = 1 / w^k, so inverting the roots elementwise gives the reverse order.
    return fft(vals, 1 / roots) / n
''',
    30: '''def pad(coeffs, to):
    """
    args:
        coeffs:List[] = list of numbers representing the coefficients of a polynomial where coeffs[i]
                    is the coeffiecient of the term x^i
        to:int = the final length coeffs should be after padding

    return:
        List of coefficients zero padded to length 'to'
    """
    coeffs = np.asarray(coeffs, dtype=complex)
    if to <= len(coeffs):
        return coeffs[:to]
    return np.concatenate((coeffs, np.zeros(to - len(coeffs), dtype=complex)))


def poly_multiply(coeffs1, coeffs2):
    """
    args:
        coeffs1:List[] = list of numbers representing the coefficients of a polynomial where coeffs[i]
                    is the coeffiecient of the term x^i
        coeffs2:List[] = list of numbers representing the coefficients of a polynomial where coeffs[i]
                    is the coeffiecient of the term x^i

    return:
        List of coefficients corresponding to the product polynomial of the two inputs.
    """
    # The product of two polynomials of lengths n1, n2 has length n1 + n2 - 1,
    # so we evaluate both on n >= n1 + n2 - 1 points where n is a power of 2.
    n = hyperceil(len(coeffs1) + len(coeffs2) - 1)
    roots = roots_of_unities(n)
    vals1 = fft(pad(coeffs1, n), roots)
    vals2 = fft(pad(coeffs2, n), roots)
    # Multiply pointwise, then interpolate back to coefficient form.
    return ifft(vals1 * vals2, roots)
''',
}

CLOSEST_SOLUTIONS = {
    5: '''def distance(p1, p2):
    """ Finds the distance between point p1 and point p2.

    Args:
        p1 (Tuple[int, int]): A point.
        p2 (Tuple[int, int]): A point.

    Returns:
        double: The distance between point p1 and point p2.
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
''',
    8: '''import itertools


def naive_closest_pair(s):
    """Implements the closest pair algorithm to find the pair of points of minimum distance from set s naively.

    Args:
        s ([List[Tuple[int, int]]]): The list of points.

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]: A tuple of the closest pair of points.
    """
    points = list(s)
    best_pair, best_dist = None, float("inf")
    # Every pair of points is considered once: O(n^2) distance computations.
    for p1, p2 in itertools.combinations(points, 2):
        d = distance(p1, p2)
        if d < best_dist:
            best_dist, best_pair = d, (p1, p2)
    return best_pair
''',
    12: '''def find_median(s):
    """Finds the median x-coordinate among the points s.

    Args:
        s ([List[Tuple[int, int]]]): The list of points sorted by x-coordinate.

    Returns:
        int: The median x-coordinate.
    """
    # s is already sorted by x-coordinate, so the middle element holds the median.
    return s[len(s) // 2][0]
''',
    14: '''def closest_pair_in_strip(points_in_strip):
    """Finds the pair of points of minimum distance among the points in points_in_strip.

    Args:
        s ([List[Tuple[int, int]]]): The list of points in the strip sorted by y-coordinate.

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]: A tuple of the closest pair of points in the strip.
    """
    points = list(points_in_strip)
    best_pair, best_dist2 = None, float("inf")
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            # Sorted by y, so once the vertical gap alone exceeds the best
            # distance found so far, no later point can beat it.
            dy = points[j][1] - points[i][1]
            if dy * dy > best_dist2:
                break
            dist2 = (points[j][0] - points[i][0]) ** 2 + dy * dy
            if dist2 < best_dist2:
                best_dist2, best_pair = dist2, (points[i], points[j])
    return best_pair
''',
    16: '''def closest_pair_recurse(sx, sy):
    """Implements the recursive process of the divide and conquer approach.

    Args:
        sx ([List[Tuple[int, int]]]): The list of points.
        sy ([List[Tuple[int, int]]]): The list of points.

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]: A tuple of the closest pair of points.
    """
    # Both inputs hold the same points: sx sorted by x-coordinate, sy sorted by
    # y-coordinate. Passing both down avoids re-sorting at every level.
    def recurse(sx, sy):
        n = len(sx)
        if n < 2:
            return None, float("inf")
        if n <= 3:
            best_pair, best_dist2 = None, float("inf")
            for i in range(n):
                for j in range(i + 1, n):
                    dist2 = (sx[i][0] - sx[j][0]) ** 2 + (sx[i][1] - sx[j][1]) ** 2
                    if dist2 < best_dist2:
                        best_dist2, best_pair = dist2, (sx[i], sx[j])
            return best_pair, best_dist2

        mid = n // 2
        mid_x = sx[mid][0]
        left_x, right_x = sx[:mid], sx[mid:]

        # Split sy according to which half each point landed in. A counter is
        # used instead of a set so that duplicate points split correctly.
        counts = {}
        for p in left_x:
            counts[p] = counts.get(p, 0) + 1
        left_y, right_y = [], []
        for p in sy:
            c = counts.get(p, 0)
            if c > 0:
                counts[p] = c - 1
                left_y.append(p)
            else:
                right_y.append(p)

        left_pair, left_dist2 = recurse(left_x, left_y)
        right_pair, right_dist2 = recurse(right_x, right_y)
        if left_dist2 <= right_dist2:
            best_pair, best_dist2 = left_pair, left_dist2
        else:
            best_pair, best_dist2 = right_pair, right_dist2

        # Only points within best_dist of the dividing line can improve on the
        # two halves; they are already in y-order, so the inner loop can stop
        # as soon as the vertical gap exceeds best_dist.
        strip = [p for p in sy if (p[0] - mid_x) ** 2 <= best_dist2]
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                dy = strip[j][1] - strip[i][1]
                if dy * dy > best_dist2:
                    break
                dist2 = (strip[j][0] - strip[i][0]) ** 2 + dy * dy
                if dist2 < best_dist2:
                    best_dist2, best_pair = dist2, (strip[i], strip[j])
        return best_pair, best_dist2

    pair, _ = recurse(list(sx), list(sy))
    return pair
''',
    18: '''def closest_pair(s):
    """Implements the closest pair algorithm to find the pair of points of minimum distance from set s.

    Args:
        s ([List[Tuple[int, int]]]): The list of points.

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]: A tuple of the closest pair of points.
    """
    points = [(int(p[0]), int(p[1])) for p in s]
    # Sort once by x and once by y; the recursion keeps both orders at all times.
    sx = sorted(points)
    sy = sorted(points, key=lambda p: (p[1], p[0]))
    return closest_pair_recurse(sx, sy)
''',
}


def patch(path, solutions):
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)
    for idx, src in solutions.items():
        cell = nb["cells"][idx]
        assert cell["cell_type"] == "code", (path, idx, cell["cell_type"])
        lines = src.splitlines(keepends=True)
        cell["source"] = lines
        cell["outputs"] = []
        cell["execution_count"] = None
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("patched", path)


if __name__ == "__main__":
    # Run from the homework root. Idempotent: it just rewrites those cells again.
    patch(os.path.join("快速傅里叶变换与多项式乘法", "fft.ipynb"), FFT_SOLUTIONS)
    patch(os.path.join("最近点对", "closest-pair.ipynb"), CLOSEST_SOLUTIONS)
