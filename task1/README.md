## 1. Task Assignment

* Create a **log-log graph** of the dependence of global error at the endpoint on the integration step $h$ used. The graph must clearly show the moment when decreasing the step, **rounding error** prevails over discretization error (curves take the shape of the letter "V").

* The graphs must contain two comparisons:
  * **a) Three methods of different order** (in double precision accuracy).
  * **b) The same method in two different arithmetics** (Single vs. Double precision).

## 2. Selected Cauchy Problem (CP)

* **Differential equation:**

$$y' = -y \quad \text{on the interval} \quad x \in [0,1].$$
$$ y (0) = 1 $$

* **Analytical solution:**

$$y(x) = e^{-x}$$

## 3. Selected Schemes (applied to our CP)

For integration with step $h$ we use these recurrence relations derived for our right-hand side $f(x,y) = -y$:

* **Explicit Euler (1st order, $p=1$):** 

  $Y_{k+1} = Y_k(1 - h)$

* **Collatz method (2nd order, $p=2$):** 

  $Y_{k+1} = Y_k\left(1 - h + \frac{h^2}{2}\right)$

* **Standard RK4 (4th order, $p=4$):** 

  $Y_{k+1} = Y_k\left(1 - h + \frac{h^2}{2} - \frac{h^3}{6} + \frac{h^4}{24}\right)$

## 4. Program Structure

* **Computational core in Rust** (`src/`):
  * `euler.rs` - Explicit Euler method (1st order)
  * `collatz.rs` - Collatz method (2nd order)
  * `rk4_double.rs` - RK4 method in double precision (4th order)
  * `rk4_single.rs` - RK4 method in single precision (4th order)

  Each binary accepts three command-line arguments:
  * `y0` - initial value (should be 1.0)
  * `h` - integration step size
  * `N` - number of integration steps

  Output: the final value $Y_N$ printed to stdout

* **Analysis and visualization** (`analyze.py`):
  * Uses logarithmically spaced numbers of steps `N` and computes the step size as `h = 1 / N`
  * Part 1: Compares three methods (Euler, Collatz, RK4) in double precision
    * Uses 100 logarithmically spaced `N` values from 10 to 10^9
    * This corresponds to step sizes from 10^-1 to 10^-9
    * Runs each method for all step sizes
    * Computes global error |Y_N - y(1)| for each step size
    * Produces log-log plot: `method_comparison.png`
  * Part 2: Compares RK4 in single vs double precision
    * Uses 100 logarithmically spaced `N` values from 2 to 10^6
    * This corresponds to step sizes from 5 * 10^-1 to 10^-6
    * Runs RK4 in both precisions for all step sizes
    * Computes global error |Y_N - y(1)| for each step size and precision
    * Produces log-log plot: `accuracy_comparison.png`

## 5. How to Run

1. **Build the Rust binaries:**
   ```bash
   cargo build --release
   ```

2. **Run the Python analysis:**
   ```bash
   uv run analyze.py
   ```

   This will generate two PNG graphs in the current directory:
   * `method_comparison.png` - compares the three methods
   * `accuracy_comparison.png` - compares single vs double precision


## 6. Results and Discussion

* **Method Comparison (`method_comparison.png`):**
  * The slopes of the error curves match the method orders:
    * **1** for Euler ( $\mathcal{O}(h)$ )
    * **2** for Collatz ( $\mathcal{O}(h^2)$ )
    * **4** for RK4 ( $\mathcal{O}(h^4)$ ).

  * Higher-order methods achieve higher accuracy with far steps.

* **Precision Comparison (`accuracy_comparison.png`):**
  * Both curves form a **"V" shape**, showing the optimal step size $h$ where truncation error and rounding error balance.
  * **Single precision (`f32`):** Hits its rounding error limit early at $h \approx 0.1$ (error $\sim 10^{-6}$), with error increasing for smaller steps.
  * **Double precision (`f64`):** Continues converging down to machine precision (error $\sim 10^{-13}$) at $h \approx 2*10^{-3}$ before rounding error begins to dominate.
