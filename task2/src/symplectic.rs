use std::env;

fn energy(x1: f64, x2: f64, x3: f64, x4: f64) -> f64 {
    0.5 * (x3 * x3 + x4 * x4) - 1.0 / (x1 * x1 + x2 * x2).sqrt()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let x1: f64 = args[1].parse().unwrap();
    let x2: f64 = args[2].parse().unwrap();
    let x3: f64 = args[3].parse().unwrap();
    let x4: f64 = args[4].parse().unwrap();
    let h: f64 = args[5].parse().unwrap();
    let n: usize = args[6].parse().unwrap();
    let stride: usize = args[7].parse().unwrap();

    let mut x1_cur = x1;
    let mut x2_cur = x2;
    let mut x3_cur = x3;
    let mut x4_cur = x4;

    for k in 0..n {
        let r = (x1_cur * x1_cur + x2_cur * x2_cur).sqrt();
        let x3_next = x3_cur - h * (x1_cur / (r * r * r));
        let x4_next = x4_cur - h * (x2_cur / (r * r * r));

        x1_cur = x1_cur + h * x3_next;
        x2_cur = x2_cur + h * x4_next;
        x3_cur = x3_next;
        x4_cur = x4_next;

        if (k + 1) % stride == 0 {
            println!(
                "{} {} {} {} {} {}",
                (k + 1) as f64 * h,
                x1_cur,
                x2_cur,
                x3_cur,
                x4_cur,
                energy(x1_cur, x2_cur, x3_cur, x4_cur)
            );
        }
    }
}
