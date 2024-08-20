import logging

# sort obj for easier comparison
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

def compare_result(expected: dict, result: dict) -> None:
    is_correct = ordered(expected) == ordered(result)
    # if not is_correct:
    #     logging.warning(f"Expected: {expected}")
    #     logging.warning(f"Result: {result}")
    return (1 if is_correct else 0, 1)
