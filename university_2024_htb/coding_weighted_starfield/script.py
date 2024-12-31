signals = eval(input())
weights = eval(input())

modified_signals = [signal * weight for signal, weight in zip(signals, weights)]

def max_stability_score(modified_signals):
    max_so_far = modified_signals[0]
    min_so_far = modified_signals[0]
    result = max_so_far

    for i in range(1, len(modified_signals)):
        temp = max_so_far
        max_so_far = max(modified_signals[i], max_so_far * modified_signals[i], min_so_far * modified_signals[i])
        min_so_far = min(modified_signals[i], temp * modified_signals[i], min_so_far * modified_signals[i])
        result = max(result, max_so_far)

    return result

print(max_stability_score(modified_signals))
