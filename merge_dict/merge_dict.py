from copy import deepcopy


def merge_dict(left, right):
    if not isinstance(right, dict):
        return right

    merged = dict(left)
    for key, value in right.items():
        if isinstance(merged.get(key), dict):
            merged[key] = merge_dict(merged[key], value)
        else:
            merged[key] = deepcopy(value)

    return merged


if __name__ == '__main__':
    print(merge_dict(
        left={
            'a': 1,
            'b': 2,
        },
        right={
            'b': -2,
            'c': -3,
        }))
    # {'a': 1, 'b': -2, 'c': -3}

    print(merge_dict(
        left={
            'a': 1,
            'b': {
                'b.a': 21,
            },
            'c': 3,
            'd': {
                'd.a': 41,
                'd.b': 42,
            },
        },
        right={
            'b': -2,
            'c': {
                'c.a': -31,
            },
            'd': {
                'd.b': -43,
                'd.d': -44,
            },
        }))
    # {'a': 1, 'b': -2, 'c': {'c.a': -31}, 
    #  'd': {'d.a': 41, 'd.b': -43, 'd.d': -44}}
