"""
Stacked Area Streamgraph of Happiness Drivers
For a specific country (default: United States) and the global average,
plots how each explained happiness factor contributed to the total
happiness score from 2005 to 2025.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

PALETTE = ['#4cc9f0', '#4361ee', '#3a0ca3', '#7209b7', '#f72585', '#f4a261']

def plot_streamgraph(ax, df_country, title):
    """Plot a stacked area chart for one country/group on the given axes."""
    df_agg = df_country.groupby('year')[METRICS].mean().reset_index()
    df_agg = df_agg.dropna()

    years = df_agg['year'].values

    # Stack from bottom
    bottom = np.zeros(len(years))
    for i, (col, label) in enumerate(zip(METRICS, METRIC_LABELS)):
        vals = df_agg[col].values
        ax.fill_between(years, bottom, bottom + vals,
                        color=PALETTE[i], alpha=0.85, label=label)
        ax.plot(years, bottom + vals, color='white', linewidth=0.4, alpha=0.5)
        bottom += vals

    ax.set_title(title, fontsize=14, fontweight='bold', color='white', pad=12)
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors='white')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.set_xlabel('Year', color='white', fontsize=11)
    ax.set_ylabel('Happiness Score (Stacked Components)', color='white', fontsize=10)
    ax.spines[:].set_color('#444')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color('white')

def create_streamgraph(country='United States'):
    # 1. Load data
    df = pd.read_csv('world_happiness_report_2005_2025.csv')
    df = df.sort_values('year')

    # --- Country-specific ---
    df_country = df[df['country'] == country].copy()

    # --- Global average ---
    df_global = df.copy()

    # 2. Build figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    fig.patch.set_facecolor('#0d0d1a')

    plot_streamgraph(ax1, df_country, f'{country} — Happiness Driver Composition (2005–2025)')
    plot_streamgraph(ax2, df_global,  'Global Average — Happiness Driver Composition (2005–2025)')

    # Shared legend at the bottom
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=6,
               facecolor='#1a1a2e', edgecolor='white', labelcolor='white',
               fontsize=10, bbox_to_anchor=(0.5, -0.02))

    fig.suptitle('Stacked Happiness Driver Streamgraph', color='white',
                 fontsize=18, fontweight='bold', y=1.01)

    plt.tight_layout()

    # 3. Save
    output_path = f"streamgraph_{country.replace(' ', '_')}.png"
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"Streamgraph saved to {output_path}!")

if __name__ == '__main__':
    create_streamgraph('United States')
