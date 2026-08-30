use std::env;

fn energy(x1: f64, x2: f64, x3: f64, x4: f64) -> f64 {
    0.5 * (x3 * x3 + x4 * x4) - 1.0 / (x1 * x1 + x2 * x2).sqrt()
}

fn f(x1: f64, x2: f64, x3: f64, x4: f64) -> (f64, f64, f64, f64) {
    let r = (x1 * x1 + x2 * x2).sqrt();
    let r3 = r * r * r;
    (x3, x4, -x1 / r3, -x2 / r3)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut x1: f64 = args[1].parse().unwrap();
    let mut x2: f64 = args[2].parse().unwrap();
    let mut x3: f64 = args[3].parse().unwrap();
    let mut x4: f64 = args[4].parse().unwrap();
    let h: f64 = args[5].parse().unwrap();
    let n: usize = args[6].parse().unwrap();
    let stride: usize = args[7].parse().unwrap();

    for k in 0..n {
        let (k1x1, k1x2, k1x3, k1x4) = f(x1, x2, x3, x4);

        let (k2x1, k2x2, k2x3, k2x4) = f(
            x1 + 0.5 * h * k1x1,
            x2 + 0.5 * h * k1x2,
            x3 + 0.5 * h * k1x3,
            x4 + 0.5 * h * k1x4,
        );

        let (k3x1, k3x2, k3x3, k3x4) = f(
            x1 + 0.5 * h * k2x1,
            x2 + 0.5 * h * k2x2,
            x3 + 0.5 * h * k2x3,
            x4 + 0.5 * h * k2x4,
        );

        let (k4x1, k4x2, k4x3, k4x4) = f(
            x1 + h * k3x1,
            x2 + h * k3x2,
            x3 + h * k3x3,
            x4 + h * k3x4,
        );

        x1 = x1 + (h / 6.0) * (k1x1 + 2.0 * k2x1 + 2.0 * k3x1 + k4x1);
        x2 = x2 + (h / 6.0) * (k1x2 + 2.0 * k2x2 + 2.0 * k3x2 + k4x2);
        x3 = x3 + (h / 6.0) * (k1x3 + 2.0 * k2x3 + 2.0 * k3x3 + k4x3);
        x4 = x4 + (h / 6.0) * (k1x4 + 2.0 * k2x4 + 2.0 * k3x4 + k4x4);

        if (k + 1) % stride == 0 {
            println!(
                "{} {} {} {} {} {}",
                (k + 1) as f64 * h,
                x1,
                x2,
                x3,
                x4,
                energy(x1, x2, x3, x4)
            );
        }
    }
}
