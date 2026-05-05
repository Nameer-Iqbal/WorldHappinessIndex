"""
Joyplot (Ridgeline Plot) of Global Happiness
Shows the distribution of happiness scores across all countries for each year,
stacked vertically to reveal polarization or global trends over time.
Built with matplotlib + scipy KDE (avoids joypy compatibility issues).
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from scipy.stats import gaussian_kde

def create_joyplot():
    # 1. Load the dataset
    df = pd.read_csv('world_happiness_report_2005_2025.csv')
    df = df[['year', 'happiness_score']].dropna()

    years = sorted(df['year'].unique())
    n_years = len(years)

    # 2. Build figure
    fig, ax = plt.subplots(figsize=(12, 14))
    fig.patch.set_facecolor('#0d0d1a')
    ax.set_facecolor('#0d0d1a')
    ax.set_xlim(2, 9)
    ax.set_xlabel('Happiness Score', color='white', fontsize=13)
    ax.set_yticks([])
    ax.spines[:].set_visible(False)
    ax.tick_params(colors='white')
    for t in ax.get_xticklabels():
        t.set_color('white')

    x_grid = np.linspace(2, 9, 500)
    colormap = cm.coolwarm
    spacing = 0.6          # vertical offset per year
    alpha_fill = 0.65

    for i, year in enumerate(reversed(years)):
        scores = df[df['year'] == year]['happiness_score'].values
        if len(scores) < 3:
            continue

        kde = gaussian_kde(scores, bw_method=0.3)
        density = kde(x_grid)
        density = density / density.max() * spacing   # normalise height

        base = i * spacing * 0.55
        color = colormap(i / n_years)

        ax.fill_between(x_grid, base, base + density,
                        color=color, alpha=alpha_fill)
        ax.plot(x_grid, base + density,
                color='white', linewidth=0.8, alpha=0.7)
        ax.axhline(base, color='white', linewidth=0.3, alpha=0.2)

        # Year label on the left
        ax.text(1.95, base + density.max() * 0.4,
                str(int(year)),
                color='white', fontsize=9, ha='right', va='center',
                fontweight='bold')

    ax.set_title(
        'Global Distribution of Happiness Scores by Year (2005–2025)\n'
        'Each ridge = one year  |  Width = density of countries at that score',
        color='white', fontsize=14, fontweight='bold', pad=18
    )

    plt.tight_layout()

    # 3. Save
    output_path = "joyplot_happiness.png"
    plt.savefig(output_path, dpi=200, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    print(f"Joyplot saved to {output_path}!")

if __name__ == '__main__':
    create_joyplot()
