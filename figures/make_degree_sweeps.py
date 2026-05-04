import matplotlib.pyplot as plt
import numpy as np


plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8,
        "legend.fontsize": 7,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def plot_degree_sweep(
    path_base,
    degrees,
    means,
    stds,
    baseline,
    baseline_std,
    ylabel,
    highlight_best=True,
):
    degrees = np.asarray(degrees)
    means = np.asarray(means)
    stds = np.asarray(stds)

    fig, ax = plt.subplots(figsize=(3.25, 2.45))
    ax.axhspan(
        baseline - baseline_std,
        baseline + baseline_std,
        color="#d8d8d8",
        alpha=0.75,
        linewidth=0,
        label="Baseline ± std",
    )
    ax.axhline(baseline, color="#555555", linestyle="--", linewidth=1.0)
    ax.errorbar(
        degrees,
        means,
        yerr=stds,
        fmt="o-",
        color="#2f6fb0",
        ecolor="#2f6fb0",
        elinewidth=1.0,
        capsize=3,
        markersize=4,
        linewidth=1.25,
        label="Chebyshev",
    )
    if highlight_best:
        best = int(np.argmin(means))
        ax.scatter(
            [degrees[best]],
            [means[best]],
            s=52,
            color="#d07a00",
            edgecolor="white",
            linewidth=0.8,
            zorder=4,
            label="Best",
        )
    ax.set_xlabel("Polynomial degree", labelpad=2)
    ax.set_ylabel(ylabel, labelpad=2)
    ax.set_xticks(degrees)
    ax.grid(axis="y", color="#e6e6e6", linewidth=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    handles, labels = ax.get_legend_handles_labels()
    order = [0, 2, 1] if highlight_best else [0, 1]
    ax.legend(
        [handles[i] for i in order],
        [labels[i] for i in order],
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.20),
        ncol=3,
        columnspacing=1.1,
        handlelength=1.5,
    )
    fig.subplots_adjust(left=0.17, right=0.98, top=0.96, bottom=0.34)
    fig.savefig(f"{path_base}.pdf", bbox_inches="tight")
    fig.savefig(f"{path_base}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


plot_degree_sweep(
    "degree_sweep_line",
    degrees=[2, 3, 4, 5, 6, 7],
    means=[0.8502, 0.8422, 0.8368, 0.8423, 0.8400, 0.8470],
    stds=[0.0125, 0.0053, 0.0092, 0.0078, 0.0105, 0.0110],
    baseline=0.8617,
    baseline_std=0.0062,
    ylabel="Normalized MASE",
)

plot_degree_sweep(
    "fev_degsweep",
    degrees=[2, 3, 4, 5, 6, 7],
    means=[1.2780, 1.2609, 1.2532, 1.2639, 1.2521, 1.2564],
    stds=[0.0039, 0.0173, 0.0064, 0.0069, 0.0068, 0.0114],
    baseline=1.2908,
    baseline_std=0.0,
    ylabel="Geometric mean MASE",
    highlight_best=False,
)
