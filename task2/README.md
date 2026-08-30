## 1. Task Assignment

* Create a simulation of a satellite orbiting a central body (Kepler's problem) in a gravitational field and analyze the conservation of total mechanical energy.

* The program must produce two visualization plots:
  * a) Trajectory plot in the 2D plane $(x_1, x_2)$ comparing the orbits computed by four different methods.
  * b) Energy deviation plot showing the change in total energy $E(t) - E(0)$ over time $t$ for all four methods. This plot will demonstrate the presence or absence of energy drift.

## 2. Selected Cauchy Problem (CP)

* We solve a nonlinear system of 4 coupled first-order ordinary differential equations representing the motion of a satellite under a central gravitational force (with dimensionless parameters $GM = 1$):

* State Vector:
  
  $$X = [x_1, x_2, x_3, x_4]^T = [x, y, u_x, u_y]^T$$

* System of Equations:
  
  $$\frac{dx_1}{dt} = x_3$$

  $$\frac{dx_2}{dt} = x_4$$

  $$\frac{dx_3}{dt} = -\frac{x_1}{(x_1^2 + x_2^2)^{3/2}}$$

  $$\frac{dx_4}{dt} = -\frac{x_2}{(x_1^2 + x_2^2)^{3/2}}$$

* Initial Conditions (Elliptical Orbit):
  
  $$t_{start} = 0, \quad t_{end} = 20, \quad h = 0.01$$

  $$x_1(0) = 1.0, \quad x_2(0) = 0.0, \quad x_3(0) = 0.0, \quad x_4(0) = 0.85$$

* Analytical First Integral (Total Mechanical Energy):
  
  $$E(t) = \frac{1}{2}(x_3^2 + x_4^2) - \frac{1}{\sqrt{x_1^2 + x_2^2}}$$

  The exact solution satisfies $\frac{dE}{dt} = 0$, so the total mechanical energy is conserved along the true trajectory.

## 3. Selected Schemes (applied to our CP)

Let $r_k = \sqrt{x_{1,k}^2 + x_{2,k}^2}$. We use a constant step size $h$.

* Explicit Euler (1st order):

  $$x_{1,k+1} = x_{1,k} + h x_{3,k}$$
  
  $$x_{2,k+1} = x_{2,k} + h x_{4,k}$$
  
  $$x_{3,k+1} = x_{3,k} - h \frac{x_{1,k}}{r_k^3}$$
  
  $$x_{4,k+1} = x_{4,k} - h \frac{x_{2,k}}{r_k^3}$$

* Collatz method (2nd order, RK2):

  First, compute the midpoint predictor:
  
  $$x_{1,k+0.5} = x_{1,k} + \frac{h}{2}x_{3,k}$$
  
  $$x_{2,k+0.5} = x_{2,k} + \frac{h}{2}x_{4,k}$$
  
  $$x_{3,k+0.5} = x_{3,k} - \frac{h}{2}\frac{x_{1,k}}{r_k^3}$$
  
  $$x_{4,k+0.5} = x_{4,k} - \frac{h}{2}\frac{x_{2,k}}{r_k^3}$$

  Evaluate the midpoint distance:
  
  $$r_{k+0.5} = \sqrt{x_{1,k+0.5}^2 + x_{2,k+0.5}^2}$$

  Then, perform the full step:
  
  $$x_{1,k+1} = x_{1,k} + h x_{3,k+0.5}$$
  
  $$x_{2,k+1} = x_{2,k} + h x_{4,k+0.5}$$
  
  $$x_{3,k+1} = x_{3,k} - h \frac{x_{1,k+0.5}}{r_{k+0.5}^3}$$
  
  $$x_{4,k+1} = x_{4,k} - h \frac{x_{2,k+0.5}}{r_{k+0.5}^3}$$

* Standard RK4 (4th order):

  Implemented using the vector state $X = [x_1, x_2, x_3, x_4]^T$ and the derivative function:

  $$F(X) = \left[x_3, x_4, -\frac{x_1}{r^3}, -\frac{x_2}{r^3}\right]^T$$

  Then:
  
  $$K_1 = F(X_k)$$
  
  $$K_2 = F\left(X_k + \frac{h}{2}K_1\right)$$
  
  $$K_3 = F\left(X_k + \frac{h}{2}K_2\right)$$
  
  $$K_4 = F(X_k + hK_3)$$
  
  $$X_{k+1} = X_k + \frac{h}{6}(K_1 + 2K_2 + 2K_3 + K_4)$$

* Symplectic Euler (1st order):

  Forces and velocities are updated first, and the newly computed velocities are immediately used to update positions:
  
  $$x_{3,k+1} = x_{3,k} - h \frac{x_{1,k}}{r_k^3}$$
  
  $$x_{4,k+1} = x_{4,k} - h \frac{x_{2,k}}{r_k^3}$$
  
  $$x_{1,k+1} = x_{1,k} + h x_{3,k+1}$$
  
  $$x_{2,k+1} = x_{2,k} + h x_{4,k+1}$$

## 4. Program Structure

* Computational core in Rust (`src/`):
  * `euler.rs` - Explicit Euler method (1st order)
  * `collatz.rs` - Collatz method (2nd order)
  * `rk4.rs` - RK4 method (4th order)
  * `symplectic.rs` - Symplectic Euler method (1st order)

  Each binary accepts the same standardized command-line arguments:
  * `x1, x2, x3, x4` - initial state
  * `h` - integration step size
  * `N` - number of integration steps
  * `stride` - number of steps between two printed lines (so long runs don't have to print every step)

  Output: one line per recorded step, in the format `t x1 x2 x3 x4 energy`.

* Analysis and visualization (`analyze.py`):
  * `trajectory_comparison()` - runs all four methods for a short duration ($t_{end} = 20$) and plots the orbits in the $(x_1, x_2)$ plane
  * `euler_symplectic_drift()` - runs Explicit Euler and Symplectic Euler for the same short duration ($t_{end} = 20$) and plots their energy deviation $E(t) - E(0)$ on a linear scale
  * `collatz_rk4_drift()` - runs Collatz and RK4 for a much longer duration ($t_{end} = 10^4$), since their secular drift is far smaller and needs more elapsed time to become visible, and plots $|E(t) - E(0)|$ on a logarithmic scale

## 5. How to Run

1. **Build the Rust binaries:**
   ```bash
   cargo build --release
   ```

2. **Run the Python analysis:**
   ```bash
   uv run analyze.py
   ```

   This will generate three PNG graphs in the current directory:
   * `orbit_trajectories.png` - compares the four orbital trajectories
   * `energy_drift_euler_symplectic.png` - Explicit Euler vs Symplectic Euler
   * `energy_drift_collatz_rk4.png` - Collatz vs RK4

## 6. Results and Discussion

* **Trajectory comparison (`orbit_trajectories.png`):**
  * Explicit Euler quickly drifts away from the expected closed ellipse and spirals outward.
  * Collatz, RK4, and Symplectic Euler all stay tightly on the correct ellipse over this short duration.

* **Explicit Euler vs Symplectic Euler (`energy_drift_euler_symplectic.png`):**
  * Explicit Euler's energy grows rapidly and without bound - the instability quickly pushes the orbit onto an unbound trajectory.
  * Symplectic Euler's energy only oscillates once per orbit around zero, with a small, bounded amplitude - no long-term growth, even though it is only 1st order.

* **Collatz vs RK4 (`energy_drift_collatz_rk4.png`):**
  * Both methods show a clear secular drift: $|E(t) - E(0)|$ grows steadily over time instead of staying bounded.
  * RK4's drift stays about four orders of magnitude below Collatz's throughout the run, consistent with its higher order.

  This shows that Collatz and RK4, despite being far more accurate per step, still accumulate a slow secular energy error because they are not symplectic - while Symplectic Euler, despite being only 1st order, conserves energy without long-term drift.
