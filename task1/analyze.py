import subprocess
import sys
from math import exp
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import typing as npt

SCRIPT_DIR: Path = Path(__file__).parent.absolute()
BIN_DIR: Path = SCRIPT_DIR / "target" / "release"
EULER_BIN: Path = BIN_DIR / "euler"
COLLATZ_BIN: Path = BIN_DIR / "collatz"
RK4_DOUBLE_BIN: Path = BIN_DIR / "rk4_double"
RK4_SINGLE_BIN: Path = BIN_DIR / "rk4_single"


def check_binaries() -> None:
    """Check if all binaries exist"""
    for path in [EULER_BIN, COLLATZ_BIN, RK4_DOUBLE_BIN, RK4_SINGLE_BIN]:
        if not path.exists():
            print(f"Error: Binary not found: {path}")
            print("Please build with: cargo build --release")
            sys.exit(1)


def main() -> None:
    check_binaries()

    y_exact: float = exp(-1)
    n_values: npt.NDArray[np.int64] = np.unique(np.logspace(1, 9, 100).astype(int))
    step_values: npt.NDArray[np.float64] = 1.0 / n_values

    print("Running method comparison...")
    method_comparison(n_values, step_values, y_exact)

    n_values: np.ndarray = np.unique(np.logspace(np.log10(2), 6, 100).astype(int))
    step_values: npt.NDArray[np.float64] = 1.0 / n_values

    print("\nRunning accuracy comparison...")
    accuracy_comparison(n_values, step_values, y_exact)

    print("\nDone!")


def method_comparison(
    n_values: npt.NDArray[np.int64],
    step_values: npt.NDArray[np.float64],
    y_exact: float,
) -> None:
    results1: list[dict[str, float]] = []
    for n, h in zip(n_values, step_values):
        print(f"Running for step size h = {h:.2e}")

        # Euler method
        try:
            euler_out = subprocess.run(
                [str(EULER_BIN), "1.0", str(h), str(n)],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if euler_out.returncode != 0:
                print(f"  Euler failed: {euler_out.stderr}")
                continue
            euler_val: float = float(euler_out.stdout.strip())
            euler_error: float = abs(euler_val - y_exact)
        except subprocess.TimeoutExpired:
            print("  Euler timeout")
            continue

        # Collatz method
        try:
            collatz_out = subprocess.run(
                [str(COLLATZ_BIN), "1.0", str(h), str(n)],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if collatz_out.returncode != 0:
                print(f"  Collatz failed: {collatz_out.stderr}")
                continue
            collatz_val: float = float(collatz_out.stdout.strip())
            collatz_error: float = abs(collatz_val - y_exact)
        except subprocess.TimeoutExpired:
            print("  Collatz timeout")
            continue

        # RK4 method
        try:
            rk4_out = subprocess.run(
                [str(RK4_DOUBLE_BIN), "1.0", str(h), str(n)],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if rk4_out.returncode != 0:
                print(f"  RK4 failed: {rk4_out.stderr}")
                continue
            rk4_val: float = float(rk4_out.stdout.strip())
            rk4_error: float = abs(rk4_val - y_exact)
        except subprocess.TimeoutExpired:
            print("  RK4 timeout")
            continue

        results1.append(
            {
                "h": h,
                "Euler_error": euler_error,
                "Collatz_error": collatz_error,
                "RK4_error": rk4_error,
            }
        )

    df1: pd.DataFrame = pd.DataFrame(results1)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.loglog(
        df1["h"], df1["Euler_error"], "o-", label="Euler (1st order)", markersize=3
    )
    plt.loglog(
        df1["h"], df1["Collatz_error"], "s-", label="Collatz (2nd order)", markersize=3
    )
    plt.loglog(df1["h"], df1["RK4_error"], "^-", label="RK4 (4th order)", markersize=3)
    plt.xlabel("Step size h", fontsize=12)
    plt.ylabel("Global error |Y_N - y(1)|", fontsize=12)
    plt.title("Method Comparison (Double Precision)", fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        SCRIPT_DIR / "method_comparison.png",
        dpi=150,
    )
    print("Saved: method_comparison.png")


def accuracy_comparison(
    n_values: npt.NDArray[np.int64],
    step_values: npt.NDArray[np.float64],
    y_exact: float,
) -> None:
    results2: list[dict[str, float]] = []
    for n, h in zip(n_values, step_values):
        print(f"Running for step size h = {h:.2e}")

        # Run RK4 (double)
        try:
            rk4_double_out = subprocess.run(
                [str(RK4_DOUBLE_BIN), "1.0", str(h), str(n)],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if rk4_double_out.returncode != 0:
                print(f"  RK4 double failed: {rk4_double_out.stderr}")
                continue
            rk4_double_val: float = float(rk4_double_out.stdout.strip())
            rk4_double_error: float = abs(rk4_double_val - y_exact)
        except subprocess.TimeoutExpired:
            print("  RK4 double timeout")
            continue

        # Run RK4 (single)
        try:
            # convert to 32-bit float for single precision
            h_single: float = np.float32(h).item()
            n_single: int = int(np.float32(n).item())

            rk4_single_out = subprocess.run(
                [str(RK4_SINGLE_BIN), "1.0", str(h_single), str(n_single)],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if rk4_single_out.returncode != 0:
                print(f"  RK4 single failed: {rk4_single_out.stderr}")
                continue
            rk4_single_val: float = float(rk4_single_out.stdout.strip())
            rk4_single_error: float = abs(rk4_single_val - y_exact)
        except subprocess.TimeoutExpired:
            print("  RK4 single timeout")
            continue

        results2.append(
            {
                "h": h,
                "RK4_double_error": rk4_double_error,
                "RK4_single_error": rk4_single_error,
            }
        )

    df2: pd.DataFrame = pd.DataFrame(results2)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.loglog(
        df2["h"],
        df2["RK4_double_error"],
        "o-",
        label="RK4 (Double precision)",
        markersize=3,
    )
    plt.loglog(
        df2["h"],
        df2["RK4_single_error"],
        "s-",
        label="RK4 (Single precision)",
        markersize=3,
    )
    plt.xlabel("Step size h", fontsize=12)
    plt.ylabel("Global error |Y_N - y(1)|", fontsize=12)
    plt.title("Accuracy Comparison (RK4)", fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        SCRIPT_DIR / "accuracy_comparison.png",
        dpi=150,
    )
    print("Saved: accuracy_comparison.png")


if __name__ == "__main__":
    main()
