"""
Plot theoretical spectral compression vs noise gain as a function of filter degree d.

Spectral compression: ||p||_inf^2 = (2^{1-d})^2 = 4^{1-d} on [-1,1] for monic Chebyshev T_d.
Noise gain:           ||a^(d)||_2^2 -- squared l2 norm of monic Chebyshev coefficients
                      in the monomial basis.

The key qualitative point: spectral compression decays as 4^{-d} while noise gain grows
as alpha^d with alpha = ((1+sqrt(2))/2)^2 = (3+2sqrt(2))/4 ~= 1.457. So the ratio
(spectral/noise) decays as (alpha/4)^d ~= 0.364^d.
"""
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.chebyshev import cheb2poly, Chebyshev
from fractions import Fraction
import math


def monic_chebyshev_monomial_coeffs(d):
    """Return coefficient vector (a_0, a_1, ..., a_d) of T_d(x)/2^{d-1} in the monomial
    basis. Each coefficient is exact (Fraction)."""
    if d == 0:
        return [Fraction(1)]
    # Coefficients of T_d in Chebyshev basis: just [0,0,...,0,1] with 1 at position d.
    # We want monomial basis -- use cheb2poly.
    cheb_coeffs = [0] * d + [1]
    monomial = cheb2poly(np.array(cheb_coeffs, dtype=object))  # leading coeff 2^{d-1}
    # Convert to Fraction for exactness, then divide by 2^{d-1}.
    leading = 2 ** (d - 1)
    out = [Fraction(int(c)) / Fraction(leading) for c in monomial]
    return out


def noise_gain_l2sq(d):
    coeffs = monic_chebyshev_monomial_coeffs(d)
    s = sum(c * c for c in coeffs)
    return float(s)


def spectral_compression_sq(d):
    if d == 0:
        return 1.0
    return 4.0 ** (1 - d)  # = (2^{1-d})^2


def main():
    ds = list(range(0, 11))
    sc = [spectral_compression_sq(d) for d in ds]
    ng = [noise_gain_l2sq(d) for d in ds]
    ratio = [s / n for s, n in zip(sc, ng)]

    print("d  spectral_sq    noise_gain    ratio")
    for d, s, n, r in zip(ds, sc, ng, ratio):
        print(f"{d:2d}  {s:11.6f}  {n:11.6f}  {r:11.6f}")

    fig, ax = plt.subplots(1, 1, figsize=(6.0, 4.2))

    ax.plot(ds, sc, marker="o", label=r"Spectral compression $\sup_{[-1,1]}|\tilde T_d|^2 = 4^{1-d}$",
            color="C0", linewidth=2)
    ax.plot(ds, ng, marker="s", label=r"Noise gain $\|\boldsymbol{a}^{(d)}\|_2^2$",
            color="C3", linewidth=2)
    ax.plot(ds, ratio, marker="^", label=r"Ratio (spectral / noise gain)",
            color="C2", linewidth=2, linestyle="--")


    ax.set_yscale("log")
    ax.set_xlabel(r"Filter degree $d$", fontsize=11)
    ax.set_ylabel("Magnitude (log scale)", fontsize=11)
    ax.set_title("Spectral compression vs. noise gain for monic Chebyshev preconditioning",
                 fontsize=11)
    ax.set_xticks(ds)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(loc="lower left", fontsize=9, framealpha=0.95)

    # Annotate the d=4 working point.
    d_star = 4
    ax.scatter([d_star], [sc[d_star]], color="C0", s=80, zorder=5, edgecolor="black")
    ax.scatter([d_star], [ng[d_star]], color="C3", s=80, zorder=5, edgecolor="black")
    ax.annotate("$d=4$ (default)", xy=(d_star, sc[d_star]),
                xytext=(d_star + 0.5, sc[d_star] * 0.25),
                fontsize=9, color="black",
                arrowprops=dict(arrowstyle="-", color="grey", lw=0.5))

    fig.tight_layout()
    out = "/scratch/gpfs/EHAZAN/jh1161/ts-usp-paper/junior_paper/figures/spectral_noise_tradeoff.pdf"
    fig.savefig(out, bbox_inches="tight")
    print(f"Wrote {out}")
    out_png = out.replace(".pdf", ".png")
    fig.savefig(out_png, dpi=200, bbox_inches="tight")
    print(f"Wrote {out_png}")


if __name__ == "__main__":
    main()
