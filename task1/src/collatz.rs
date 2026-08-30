use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let y0: f64 = args[1].parse().unwrap();
    let h: f64 = args[2].parse().unwrap();
    let n: u64 = args[3].parse().unwrap();

    let mut y = y0;
    for _ in 0..n {
        y = y * (1.0 - h + h * h / 2.0);
    }

    println!("{}", y);
}
