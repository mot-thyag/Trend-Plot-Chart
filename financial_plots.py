import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

class FinancialPlotter:
    def __init__(self, theme="dark"):
        self.theme = theme
        self.colors = {
            'background': '#1e1e1e',
            'text': '#ffffff',
            'primary': '#00b3ff',
            'secondary': '#ff7f0e',
            'tertiary': '#2ca02c',
            'quaternary': '#d62728'
        }
        
        # Common layout settings
        self.layout_template = {
            'paper_bgcolor': self.colors['background'],
            'plot_bgcolor': '#2d2d2d',
            'font': {'color': self.colors['text']},
            'xaxis': {
                'showgrid': True,
                'gridcolor': '#3d3d3d',
                'gridwidth': 0.5
            },
            'yaxis': {
                'showgrid': True,
                'gridcolor': '#3d3d3d',
                'gridwidth': 0.5
            }
        }

    def create_market_plot(self, data):
        """
        Creates a dual-axis plot with price line and volume bars
        """
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Price line
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data['price'],
                name="Price",
                line=dict(color=self.colors['primary'], width=2),
                hovertemplate="Price: $%{y:.2f}<br>Date: %{x}<extra></extra>"
            ),
            secondary_y=False
        )
        
        # Volume bars
        fig.add_trace(
            go.Bar(
                x=data['date'],
                y=data['volume'],
                name="Volume",
                marker_color=self.colors['secondary'],
                opacity=0.5,
                hovertemplate="Volume: %{y:,.0f}<br>Date: %{x}<extra></extra>"
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title="Market Performance",
            **self.layout_template,
            height=600,
            width=800,
            margin=dict(l=50, r=50, t=50, b=50),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )
        
        fig.update_xaxes(tickangle=0, dtick=1)
        fig.update_yaxes(automargin=True, tickformat=',d')
        
        return fig

    def create_income_statement_plot(self, data):
        """
        Creates a line plot for financial metrics with growth percentages
        """
        fig = go.Figure()
        
        metrics = ['revenue', 'gross_profit', 'operating_profit', 'net_income', 'operating_cash_flow']
        colors = [self.colors[c] for c in ['primary', 'secondary', 'tertiary', 'quaternary', 'primary']]
        
        for metric, color in zip(metrics, colors):
            # Calculate YoY growth
            growth = [(data[metric][i] - data[metric][i-1])/data[metric][i-1] * 100 
                     if i > 0 else 0 for i in range(len(data[metric]))]
            
            fig.add_trace(
                go.Scatter(
                    x=data['date'],
                    y=data[metric],
                    name=metric.replace('_', ' ').title(),
                    line=dict(color=color, width=2),
                    text=[f"{g:+.1f}%" if i > 0 else '' for i, g in enumerate(growth)],
                    textposition='top center',
                    hovertemplate="%{y:,.0f}<br>Growth: %{text}<extra></extra>"
                )
            )
        
        fig.update_layout(
            title="Income Statement Metrics",
            **self.layout_template,
            height=600,  # Increased height
            width=800,   # Set specific width
            margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )
        
        # Update axes to make plot more compact
        fig.update_xaxes(
            tickangle=0,
            dtick=1
        )
        
        fig.update_yaxes(
            automargin=True,
            tickformat=',d'
        )
        
        return fig

    def create_revenue_breakdown_plot(self, data):
        """
        Creates a stacked area plot for revenue breakdown
        """
        fig = go.Figure()
        
        for product in data['products']:
            fig.add_trace(
                go.Scatter(
                    x=data['date'],
                    y=data[product],
                    name=product,
                    stackgroup='one',
                    hovertemplate="%{y:,.0f}<extra></extra>"
                )
            )
        
        fig.update_layout(
            title="Revenue Breakdown by Product",
            **self.layout_template,
            height=600,
            width=800,
            margin=dict(l=50, r=50, t=50, b=50),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )
        
        fig.update_xaxes(tickangle=0, dtick=1)
        fig.update_yaxes(automargin=True, tickformat=',d')
        
        return fig

    def create_metrics_plot(self, data):
        """
        Creates a line plot for EPS and DPS
        """
        fig = go.Figure()
        
        # EPS Line
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data['eps'],
                name="EPS",
                line=dict(color=self.colors['primary'], width=2),
                hovertemplate="EPS: $%{y:.2f}<extra></extra>"
            )
        )
        
        # DPS Line
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data['dps'],
                name="DPS",
                line=dict(color=self.colors['secondary'], width=2),
                hovertemplate="DPS: $%{y:.2f}<extra></extra>"
            )
        )
        
        fig.update_layout(
            title="EPS and DPS Metrics",
            **self.layout_template,
            height=600,
            width=800,
            margin=dict(l=50, r=50, t=50, b=50),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )
        
        fig.update_xaxes(tickangle=0, dtick=1)
        fig.update_yaxes(automargin=True, tickformat='.2f')
        
        return fig 