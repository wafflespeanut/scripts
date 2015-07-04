// iterate some of the nodes using finite-difference method
fn iterate(matrix: &Vec<f64>, rows: usize, cols: usize, toler: f64) -> Vec<f64> {
    let (mut i, mut j) = (cols + 1, 2);     // where to start the iteration
    let (mut new, mut old) = (matrix.clone(), matrix.clone());
    let (mut num_agreed, mut num_iter) = (0, 0);
    while num_agreed < (rows - 2) * (cols - 2) {        // actually, I'm taking a matrix as a lengthy list
        if i > j * cols - 2 {       // as it reaches the end of a column
            if j >= rows - 2 {      // if it's also near the end of all rows
                i = cols + 1; j = 2;    // then, reset it back to the start
                num_agreed = 0; num_iter += 1; continue
            } else { i += 3; j += 1; continue }     // or else, just take it to the next row
        } old = new.clone();        // to check with the previous iteration
        new[i] = (old[i - 1] + old[i + 1] + old[i - cols] + old[i + cols]) / 4.0;
        if (new[i] - old[i]).abs() <= toler { num_agreed += 1; }    // check the tolerance
        i += 1;
    } println!("\nNumber of iterations: {}\n", num_iter); new
}

fn main() {
    let stuff: Vec<f64> = vec![2.0, 3.0, 5.0, 2.0, 4.5, 2.0, 0.0, 0.0, 0.0, 5.0, 6.0, 4.0, 3.0, 5.5, 7.0];
    println!("{:?}", iterate(&stuff, 3, 5, 0.00001));       // this is a 3 X 5 matrix (with 3 nodes in the middle)
}
