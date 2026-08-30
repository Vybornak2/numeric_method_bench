import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR: Path = Path(__file__).parent.absolute()
BIN_DIR: Path = SCRIPT_DIR / "target" / "release"
EULER_BIN: Path = BIN_DIR / "euler"
COLLATZ_BIN: Path = BIN_DIR / "collatz"
RK4_BIN: Path = BIN_DIR / "rk4"
SYMPLECTIC_BIN: Path = BIN_DIR / "symplectic"

# Initial conditions (elliptical orbit)
X1_0, X2_0, X3_0, X4_0 = 1.0, 0.0, 0.0, 0.85
H = 0.01


def check_binaries() -> None:
    """Check if all binaries exist"""
    for path in [EULER_BIN, COLLATZ_BIN, RK4_BIN, SYMPLECTIC_BIN]:
        if not path.exists():
            print(f"Error: Binary not found: {path}")
            print("Please build with: cargo build --release")
            sys.exit(1)


def run_orbit(binary: Path, n: int, stride: int) -> np.ndarray:
    """Run a method binary and parse its output into an (rows, 6) array of
    columns: t, x1, x2, x3, x4, energy"""
    out = subprocess.run(
        [str(binary), str(X1_0), str(X2_0), str(X3_0), str(X4_0), str(H), str(n), str(stride)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if out.returncode != 0:
        print(f"  {binary.name} failed: {out.stderr}")
        sys.exit(1)

    return np.loadtxt(out.stdout.splitlines())


def main() -> None:
    check_binaries()

    print("Running trajectory comparison...")
    trajectory_comparison()

    print("\nRunning Euler vs Symplectic energy drift...")
    euler_symplectic_drift()

    print("\nRunning Collatz vs RK4 energy drift...")
    collatz_rk4_drift()

    print("\nDone!")


def trajectory_comparison() -> None:
    # Short run so Explicit Euler hasn't diverged yet, keeping all four
    # orbits comparable on the same plot.
    n = 2000
    stride = 1

    euler = run_orbit(EULER_BIN, n, stride)
    collatz = run_orbit(COLLATZ_BIN, n, stride)
    rk4 = run_orbit(RK4_BIN, n, stride)
    symplectic = run_orbit(SYMPLECTIC_BIN, n, stride)

    plt.figure(figsize=(8, 6))
    plt.plot(euler[:, 1], euler[:, 2], label="Euler")
    plt.plot(collatz[:, 1], collatz[:, 2], label="Collatz")
    plt.plot(rk4[:, 1], rk4[:, 2], label="RK4")
    plt.plot(symplectic[:, 1], symplectic[:, 2], label="Symplectic Euler")
    plt.xlim(-2.5, 2.5)
    plt.ylim(-2.5, 2.5)
    plt.xlabel("x1", fontsize=12)
    plt.ylabel("x2", fontsize=12)
    plt.title("Orbital Trajectories", fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(SCRIPT_DIR / "orbit_trajectories.png", dpi=150)
    print("Saved: orbit_trajectories.png")


def euler_symplectic_drift() -> None:
    # Short run - Explicit Euler blows up almost immediately, so there is no
    # point running it any longer.
    n = 2000
    stride = 1

    euler = run_orbit(EULER_BIN, n, stride)
    symplectic = run_orbit(SYMPLECTIC_BIN, n, stride)

    euler_t, euler_e = euler[:, 0], euler[:, 5]
    symplectic_t, symplectic_e = symplectic[:, 0], symplectic[:, 5]

    plt.figure(figsize=(10, 6))
    plt.plot(euler_t, euler_e - euler_e[0], label="Euler")
    plt.plot(symplectic_t, symplectic_e - symplectic_e[0], label="Symplectic Euler")
    plt.xlabel("time t", fontsize=12)
    plt.ylabel("E(t) - E(0)", fontsize=12)
    plt.title("Energy Drift: Explicit Euler vs Symplectic Euler", fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(SCRIPT_DIR / "energy_drift_euler_symplectic.png", dpi=150)
    print("Saved: energy_drift_euler_symplectic.png")


def collatz_rk4_drift() -> None:
    # Much longer run - the secular drift of these higher-order methods is
    # far smaller and needs more elapsed time to become visible.
    n = 1_000_000
    stride = 100

    collatz = run_orbit(COLLATZ_BIN, n, stride)
    rk4 = run_orbit(RK4_BIN, n, stride)

    collatz_t, collatz_e = collatz[:, 0], collatz[:, 5]
    rk4_t, rk4_e = rk4[:, 0], rk4[:, 5]

    plt.figure(figsize=(10, 6))
    plt.semilogy(collatz_t, np.abs(collatz_e - collatz_e[0]), label="Collatz")
    plt.semilogy(rk4_t, np.abs(rk4_e - rk4_e[0]), label="RK4")
    plt.xlabel("time t", fontsize=12)
    plt.ylabel("|E(t) - E(0)|", fontsize=12)
    plt.title("Energy Drift: Collatz vs RK4", fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(SCRIPT_DIR / "energy_drift_collatz_rk4.png", dpi=150)
    print("Saved: energy_drift_collatz_rk4.png")


if __name__ == "__main__":
    main()
