# 🌍 World Happiness Index — Data Visualizations (2005–2025)

A collection of Python data visualizations built on the **World Happiness Report** dataset spanning 2005 to 2025. Each script is self-contained and produces a high-quality chart.

## 📊 Visualizations

| Script | Output | Description |
|---|---|---|
| `static_visualizer.py` | `happiness_plot.png` | Top 20 & Bottom 20 happiest countries (bar charts) |
| `eda_analysis.py` | `happiness_map.html` | Folium choropleth world map |
| `animated_bubble_chart.py` | `animated_bubble_chart.html` | Hans Rosling-style animated bubble chart (Plotly) |
| `joyplot_happiness.py` | `joyplot_happiness.png` | Ridgeline / Joyplot of happiness distribution by year |
| `radar_chart_archetypes.py` | `radar_chart_archetypes.png` | Spider-web radar chart for top & bottom 5 countries |
| `streamgraph_happiness.py` | `streamgraph_United_States.png` | Stacked area chart of happiness drivers over time |
| `pca_happiness_projection.py` | `pca_happiness_projection.png` | PCA 2D projection clustering countries by socioeconomic profile |

## 🗂️ Dataset

`world_happiness_report_2005_2025.csv` — contains the following columns:

- `year`, `rank_in_year`, `country`, `happiness_score`
- `explained_log_gdp_per_capita`
- `explained_social_support`
- `explained_healthy_life_expectancy`
- `explained_freedom`
- `explained_generosity`
- `explained_corruption`
- `dystopia_plus_residual`

## 🚀 Setup

```bash
pip install pandas matplotlib seaborn plotly scipy scikit-learn folium
```

Then run any script directly:

```bash
python animated_bubble_chart.py
python joyplot_happiness.py
python radar_chart_archetypes.py
python streamgraph_happiness.py
python pca_happiness_projection.py
```
