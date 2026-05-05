"""
Radar Chart (Spider Web) for Country Archetypes
Plots the top 5 and bottom 5 happiest countries on a circular grid
across all 6 "explained" happiness metrics.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

METRICS = [
    'explained_log_gdp_per_capita',
    'explained_social_support',
    'explained_healthy_life_expectancy',
    'explained_freedom',
    'explained_generosity',
    'explained_corruption',
]

METRIC_LABELS = [
    'GDP per Capita',
    'Social Support',
    'Life Expectancy',
    'Freedom',
    'Generosity',
    'Low Corruption',
]

def draw_radar(ax, values, color, label):
    """Draw a single radar polygon on the given axes."""
    N = len(values)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    # Close the polygon
    values  = values + [values[0]]
    angles  = angles + [angles[0]]
    ax.plot(angles, values, color=color, linewidth=2, linestyle='solid', label=label)
    ax.fill(angles, values, color=color, alpha=0.15)

def create_radar_charts():
    # 1. Load data
    df = pd.read_csv('world_happiness_report_2005_2025.csv')

    # 2. Get the most recent year for each country
    df_sorted = df.sort_values('year')
    df_latest = df_sorted.groupby('country', as_index=False).last()

    # 3. Drop rows with missing metric data
    df_latest = df_latest.dropna(subset=METRICS)
    df_latest = df_latest.sort_values('happiness_score', ascending=False)

    top5    = df_latest.head(5)
    bottom5 = df_latest.tail(5)

    N = len(METRIC_LABELS)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

    # --- Figure with two subplots ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8),
                                    subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#1a1a2e')

    colors_top    = ['#00d4aa', '#4ecdc4', '#44a8b3', '#3a86ff', '#8338ec']
    colors_bottom = ['#ff6b6b', '#ff8e53', '#ffbe0b', '#fb5607', '#e63946']

    for ax, group, colors, title in [
        (ax1, top5,    colors_top,    'Top 5 Happiest Countries'),
        (ax2, bottom5, colors_bottom, 'Bottom 5 Least Happy Countries'),
    ]:
        ax.set_facecolor('#0f3460')
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        # Set category labels
        ax.set_xticks(angles)
        ax.set_xticklabels(METRIC_LABELS, color='white', fontsize=10)

        # Set radial ticks and hide labels
        ax.set_rlabel_position(30)
        ax.tick_params(colors='white')
        ax.yaxis.set_tick_params(labelcolor='grey', labelsize=8)
        ax.grid(color='white', alpha=0.2)
        ax.spines['polar'].set_color('white')

        for i, (_, row) in enumerate(group.iterrows()):
            vals = [row[m] for m in METRICS]
            draw_radar(ax, vals, colors[i], row['country'])

        ax.set_title(title, color='white', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1),
                  labelcolor='white', facecolor='#0f3460', edgecolor='white',
                  fontsize=9)

    fig.suptitle('Country Happiness Archetypes — Spider Web Comparison',
                 color='white', fontsize=18, fontweight='bold', y=1.02)

    # 4. Save
    output_path = "radar_chart_archetypes.png"
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"Radar chart saved to {output_path}!")

if __name__ == '__main__':
    create_radar_charts()
