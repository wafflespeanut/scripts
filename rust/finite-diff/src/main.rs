
fn check(matrix: &Vec<f32>, rows: usize, cols: usize, tol: f32) {
    let (mut i, mut j) = (cols + 1, 1);
    let (mut now, mut then) = (matrix.clone(), matrix.clone());
    let mut count = 0;
    while count < (rows - 2) * (cols - 2) {
        then = now.clone();
        now[i] = (then[i - 1] + then[i + 1] + then[i - cols] + then[i + cols]) / 4.0;
        if (now[i] - then[i]) <= tol { count += 1; }
        println!("{:?}", (&now, &then, i, j));
        if i == j * cols - 2 {
            if j == rows - 2 {
                i = cols + 1; j = 1;
                count = 0; continue
            } else { i += 3; j += 1; continue }
        } i += 1;
    }
}

fn main() {
    let stuff: Vec<f32> = vec![2.0, 3.0, 5.0, 2.0, 4.5, 2.0, 0.0, 0.0, 0.0, 5.0, 6.0, 4.0, 3.0, 5.5, 7.0];
    check(&stuff, 3, 5, 0.5);
}
