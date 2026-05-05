import pandas as pd
import folium
import requests

def create_happiness_map():
    # 1. Load the dataset
    df = pd.read_csv('world_happiness_report_2005_2025.csv')
    
    # 2. Get the latest available happiness score for each country
    # Sort by year so that the last entry for each country is the most recent
    df_sorted = df.sort_values('year')
    df_latest = df_sorted.groupby('country', as_index=False).last()
    
    # URL for the GeoJSON data containing world country boundaries
    geo_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
    
    # Rename some countries in the dataframe to match the GeoJSON keys (common mismatches)
    country_mapping = {
        'United States': 'United States of America',
        'Taiwan Province of China': 'Taiwan',
        'Russian Federation': 'Russia',
        'Congo (Brazzaville)': 'Republic of the Congo',
        'Congo (Kinshasa)': 'Democratic Republic of the Congo',
        'DR Congo': 'Democratic Republic of the Congo',
        'Congo': 'Republic of the Congo',
        'Tanzania': 'United Republic of Tanzania',
        'Serbia': 'Republic of Serbia',
        'North Macedonia': 'Macedonia',
        'Somaliland Region': 'Somaliland'
    }
    df_latest['country'] = df_latest['country'].replace(country_mapping)
    
    # 3. Create a Folium map centered around the world
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='cartodb positron')
    
    # 4. Create the choropleth map
    folium.Choropleth(
        geo_data=geo_url,
        name='choropleth',
        data=df_latest,
        columns=['country', 'happiness_score'],
        key_on='feature.properties.name',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Happiness Score',
        nan_fill_color='white'
    ).add_to(m)
    
    # Add a title
    title_html = '''
             <h3 align="center" style="font-size:20px"><b>World Happiness Score (Latest Available Data)</b></h3>
             '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # 5. Save the map to an HTML file
    m.save('happiness_map.html')
    print("Map successfully generated and saved to happiness_map.html!")

if __name__ == '__main__':
    create_happiness_map()
