use std::cmp::Ord;

fn insertion_sort<T: Ord>(array: &mut [T]) {
    for i in 1..array.len() {
        let mut j = i;
        while j > 0 && array[j] < array[j - 1] {
            array.swap(j, j - 1);       // swaps values from behind and goes backwards
            j -= 1;
        }
    }
}

fn main() {
    let mut arr: [i32; 11] = [25, 47, 92, 70, 64, 89, 25, 13, 31, 6, 58];
    insertion_sort(&mut arr);
}
