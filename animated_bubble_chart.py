import pandas as pd
import plotly.express as px
import numpy as np

def create_animated_bubble_chart():
    # 1. Load the dataset
    df = pd.read_csv('world_happiness_report_2005_2025.csv')
    
    # 2. Select relevant columns
    cols = [
        'year', 'country', 'happiness_score', 
        'explained_log_gdp_per_capita', 'explained_healthy_life_expectancy',
        'explained_freedom'
    ]
    df = df[cols].copy()
    
    # 3. Clean and prepare data for animation
    # Sort by country and year to prepare for filling missing values
    df = df.sort_values(['country', 'year'])
    
    # To ensure smooth animation, we forward-fill and then backward-fill missing values per country
    fill_cols = ['happiness_score', 'explained_log_gdp_per_capita', 'explained_healthy_life_expectancy', 'explained_freedom']
    for col in fill_cols:
        df[col] = df.groupby('country')[col].transform(lambda x: x.ffill().bfill())
    
    # Remove rows that still have NaNs (e.g. if a country has no data at all for a column)
    df = df.dropna(subset=['explained_log_gdp_per_capita', 'happiness_score', 'explained_healthy_life_expectancy'])
    
    # Sort by year so animation frames are in correct chronological order
    df = df.sort_values('year')
    
    # To avoid negative sizes, ensure 'explained_healthy_life_expectancy' is strictly positive
    # Some early years might have tiny or zero values, let's clip them at a small positive minimum
    df['explained_healthy_life_expectancy'] = df['explained_healthy_life_expectancy'].clip(lower=0.01)
    
    # Calculate fixed axis ranges to prevent the axes from jumping around during animation
    x_min = df['explained_log_gdp_per_capita'].min() - 0.2
    x_max = df['explained_log_gdp_per_capita'].max() + 0.2
    y_min = df['happiness_score'].min() - 0.5
    y_max = df['happiness_score'].max() + 0.5

    # 4. Create the animated scatter plot
    fig = px.scatter(
        df,
        x="explained_log_gdp_per_capita",
        y="happiness_score",
        animation_frame="year",
        animation_group="country",
        size="explained_healthy_life_expectancy",
        color="country",
        hover_name="country",
        size_max=40,
        range_x=[x_min, x_max],
        range_y=[y_min, y_max],
        title="Evolution of Happiness, Wealth, and Health (2005 - 2025)",
        labels={
            "explained_log_gdp_per_capita": "GDP per Capita (Log)",
            "happiness_score": "Happiness Score",
            "explained_healthy_life_expectancy": "Healthy Life Expectancy"
        }
    )
    
    # Hide the legend because there are too many countries, it makes the chart unreadable
    fig.update_layout(showlegend=False)

    # 5. Save the interactive chart as an HTML file
    output_filename = 'animated_bubble_chart.html'
    fig.write_html(output_filename)
    print(f"Animated bubble chart successfully saved to {output_filename}!")

if __name__ == '__main__':
    create_animated_bubble_chart()
