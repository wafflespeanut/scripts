use std::fmt;
use std::fs::File;
use std::io::{BufRead, BufReader};
mod triangle;

struct Point {
    x: f64,
    y: f64,
}

// just for displaying points as tuples
impl fmt::Debug for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

// reads the file contents into a vector of 'Points'
fn get_points(path: &str) -> Vec<Point> {
    // a hell lot of unwraps! (assuming that no errors occur along the way)
    let file = BufReader::new(File::open(path).unwrap());
    file.lines().map(|points| {
        let points = points.unwrap();
        let mut point = points.split_whitespace();
        let x_val = point.next().unwrap();
        let y_val = point.next().unwrap();
        Point { x: x_val.parse::<f64>().unwrap(), y: y_val.parse::<f64>().unwrap() }
    }).collect()
}

fn main() {
    let data_file = "target/sample";            // input sample (generated from Python)
    println!("{:?}", get_points(data_file));
}
