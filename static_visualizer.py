import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_static_visualization():
    # 1. Load the dataset
    df = pd.read_csv('world_happiness_report_2005_2025.csv')
    
    # 2. Get the latest available happiness score for each country
    df_sorted = df.sort_values('year')
    df_latest = df_sorted.groupby('country', as_index=False).last()
    
    # 3. Sort by happiness score to get Top 20 and Bottom 20
    df_latest = df_latest.sort_values('happiness_score', ascending=False)
    top_20 = df_latest.head(20)
    bottom_20 = df_latest.tail(20)
    
    # Set the style
    sns.set_theme(style="whitegrid")
    
    # 4. Create a figure with two subplots side by side
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    
    # Plot Top 20
    sns.barplot(x='happiness_score', y='country', data=top_20, ax=axes[0], palette="Greens_r")
    axes[0].set_title('Top 20 Happiest Countries (Latest Data)', fontsize=16)
    axes[0].set_xlabel('Happiness Score', fontsize=12)
    axes[0].set_ylabel('Country', fontsize=12)
    
    # Plot Bottom 20
    sns.barplot(x='happiness_score', y='country', data=bottom_20, ax=axes[1], palette="Reds_r")
    axes[1].set_title('Bottom 20 Happiest Countries (Latest Data)', fontsize=16)
    axes[1].set_xlabel('Happiness Score', fontsize=12)
    axes[1].set_ylabel('')
    
    # Adjust layout
    plt.tight_layout()
    
    # 5. Save the figure to the scratch directory
    output_path = r"C:\Users\abcd\.gemini\antigravity\brain\93d3ec01-39c5-40e9-b243-b9e6df74a954\scratch\happiness_plot.png"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Plot successfully saved to {output_path}")

if __name__ == '__main__':
    create_static_visualization()
