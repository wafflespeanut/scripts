arr = [25, 47, 92, 70, 64, 89, 25, 13, 31, 6, 58];

def insertion_sort(array):      # in-place sort
    for i in xrange(1, len(array)):
        j = i
        while j and array[j] < array[j - 1]:
            array[j], array[j - 1] = array[j - 1], array[j]
            j -= 1

def merge_sort(array):          # recursive out-of-place sort
    length = len(array)
    def merge(left, right):
        result = []
        while left and right:
            if left[0] < right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left if left else right)
        return result

    if length <= 1:
        return array
    left, right = merge_sort(array[:(length / 2)]), merge_sort(array[(length / 2):])
    return merge(left, right)
