import os
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.io as pio
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class data:
    def generate_combined_plotly_graphs(file_path):
        # Load data
        name = str(file_path)
        name = name.split("\\")[-1]
        name = name[0:-5]
        df = pd.read_excel(file_path)
        
        # Clean data
        df = df[df['AGE'] >= 18]
        df = df[["AGE", "GENDER"]]
        
        # Plot gender by age
        grouped_df = df.groupby(['AGE', 'GENDER']).size().unstack(fill_value=0)
        fig1 = make_subplots(rows=1, cols=2, subplot_titles=('MALE', 'FEMALE'))
        fig1.add_trace(go.Bar(x=grouped_df.index, y=grouped_df['MALE'], name='MALE'), row=1, col=1)
        fig1.add_trace(go.Bar(x=grouped_df.index, y=grouped_df['FEMALE'], name='Female'), row=1, col=2)
        fig1.update_layout(title='Count of Gender by Age', xaxis=dict(title='Age'), yaxis=dict(title='Count'), template='plotly_dark', bargap=0.2)
        
        # Plot gender lines
        gender_counts = df.groupby(['AGE', 'GENDER']).size().unstack(fill_value=0)
        male_counts = gender_counts['MALE'].values
        female_counts = gender_counts['FEMALE'].values
        ages = gender_counts.index.values
        male_trace = go.Scatter(x=male_counts, y=ages, mode='lines+markers', name='Male', line=dict(color='blue'))
        female_trace = go.Scatter(x=female_counts, y=ages, mode='lines+markers', name='Female', line=dict(color='red'))
        layout = go.Layout(title='Count of Male and Female by Age', yaxis=dict(title='Age'), template='plotly_dark')
        fig2_male = go.Figure(data=[male_trace], layout=layout)
        fig2_female = go.Figure(data=[female_trace], layout=layout)
        
        # Plot gender histograms
        fig3 = make_subplots(rows=1, cols=2, subplot_titles=('Male', 'Female'))
        fig3.add_trace(go.Histogram(x=male_counts, name='Male', marker=dict(color='blue'), opacity=0.4), row=1, col=1)
        fig3.add_trace(go.Histogram(x=female_counts, name='Female', marker=dict(color='red'), opacity=0.4), row=1, col=2)
        fig3.update_layout(title='Count of Male and Female by Age', xaxis=dict(title='Count'), yaxis=dict(title='Frequency'), barmode='overlay', template='plotly_dark')
        
        # Convert figures to HTML content
        html_content1 = pio.to_html(fig1, full_html=False)
        html_content2_male = pio.to_html(fig2_male, full_html=False)
        html_content2_female = pio.to_html(fig2_female, full_html=False)
        html_content3 = pio.to_html(fig3, full_html=False)
        
        # Generate combined HTML content
        combined_html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dash_data</title>
        </head>
        <body>
            <h1> Data of {name}</h1>
            <div> {html_content1} </div>
            <div> {html_content2_male} </div>
            <div> {html_content2_female} </div>
            <div> {html_content3} </div>
        </body>
        </html>
        """
        
        # Save the combined HTML content to a single file with UTF-8 encoding
        with open(os.path.join(BASE_DIR,'templates/main.html'), 'w', encoding='utf-8') as f:
            f.write(combined_html_content)
        
        #print("Combined HTML file 'main.html' generated successfully.")
