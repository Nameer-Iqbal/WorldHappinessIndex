"""
PCA 2D Projection of World Happiness Data
Uses sklearn PCA to reduce the 6 "explained_" dimensions into 2 principal
components, then visualizes countries as a scatter plot colored by happiness score.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

METRICS = [
    'explained_log_gdp_per_capita',
    'explained_social_support',
    'explained_healthy_life_expectancy',
    'explained_freedom',
    'explained_generosity',
    'explained_corruption',
]

def create_pca_projection():
    # 1. Load the most recent year per country
    df = pd.read_csv('world_happiness_report_2005_2025.csv')
    df_sorted = df.sort_values('year')
    df_latest = df_sorted.groupby('country', as_index=False).last()

    # 2. Drop rows with any missing metric
    df_clean = df_latest.dropna(subset=METRICS + ['happiness_score']).copy()

    # 3. Standardise the features
    X = df_clean[METRICS].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. PCA → 2 components
    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(X_scaled)
    df_clean['PC1'] = components[:, 0]
    df_clean['PC2'] = components[:, 1]

    explained = pca.explained_variance_ratio_ * 100  # %

    # 5. Plot
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#0d0d1a')
    ax.set_facecolor('#0f0f23')

    cmap = plt.get_cmap('RdYlGn')
    norm = mcolors.Normalize(vmin=df_clean['happiness_score'].min(),
                             vmax=df_clean['happiness_score'].max())

    sc = ax.scatter(
        df_clean['PC1'], df_clean['PC2'],
        c=df_clean['happiness_score'],
        cmap=cmap, norm=norm,
        s=90, alpha=0.9, edgecolors='white', linewidths=0.4
    )

    # Annotate every country
    for _, row in df_clean.iterrows():
        ax.annotate(
            row['country'],
            (row['PC1'], row['PC2']),
            fontsize=5.5,
            color='white',
            alpha=0.75,
            xytext=(3, 3),
            textcoords='offset points'
        )

    # Colorbar
    cbar = plt.colorbar(sc, ax=ax, pad=0.01)
    cbar.set_label('Happiness Score', color='white', fontsize=12)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

    # PCA loading arrows (biplot)
    loading_scale = 2.5
    for i, label in enumerate(METRICS):
        dx = pca.components_[0, i] * loading_scale
        dy = pca.components_[1, i] * loading_scale
        ax.annotate(
            '', xy=(dx, dy), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color='#f4a261', lw=1.5)
        )
        ax.text(dx * 1.12, dy * 1.12,
                label.replace('explained_', '').replace('_', ' ').title(),
                color='#f4a261', fontsize=8, ha='center', va='center')

    ax.set_xlabel(f'PC1 ({explained[0]:.1f}% variance)', color='white', fontsize=12)
    ax.set_ylabel(f'PC2 ({explained[1]:.1f}% variance)', color='white', fontsize=12)
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#444')
    for t in ax.get_xticklabels() + ax.get_yticklabels():
        t.set_color('white')

    ax.set_title('PCA 2D Projection of World Happiness Factors\n'
                 'Countries clustered by socioeconomic profile — colored by Happiness Score',
                 color='white', fontsize=15, fontweight='bold', pad=16)

    ax.axhline(0, color='white', linewidth=0.4, alpha=0.3)
    ax.axvline(0, color='white', linewidth=0.4, alpha=0.3)

    plt.tight_layout()

    # 6. Save
    output_path = "pca_happiness_projection.png"
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"PCA projection saved to {output_path}!")
    print(f"Variance explained: PC1={explained[0]:.1f}%, PC2={explained[1]:.1f}%")

if __name__ == '__main__':
    create_pca_projection()
