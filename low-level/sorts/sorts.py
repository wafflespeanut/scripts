arr = [25, 47, 92, 70, 64, 89, 25, 13, 31, 6, 58];

def insertion_sort(array):
    for i in xrange(1, len(array)):
        j = i
        while j and array[j] < array[j - 1]:
            array[j], array[j - 1] = array[j - 1], array[j]
            j -= 1

if __name__ == '__main__':
    insertion_sort(arr)
