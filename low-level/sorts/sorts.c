#include <stdio.h>

void insertion_sort(int *array, int length) {   // in-place sort
    int i, j, value;
    for (i = 1; i < length; i++) {
        j = i - 1;
        value = array[i];
        while (j >= 0 && array[j] > value) {
            array[j + 1] = array[j];    // overwrites the values in front and moves forward
            j -= 1;
        } array[j + 1] = value;
    }
}

void main() {
    int arr[] = {25, 47, 92, 70, 64, 89, 25, 13, 31, 6, 58};
    int length = sizeof(arr) / sizeof(arr[0]);
    insertion_sort(arr, length);
}
