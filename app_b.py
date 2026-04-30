import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="ESG P2P Review Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    file_path = 'P2P_Review.xlsx'
    
    company_sheets = ['SW', 'PKG', 'IP', 'GPI', 'SK', 'WK']
    company_data = {}
    
    for sheet in company_sheets:
        df = pd.read_excel(file_path, sheet_name=sheet)
        company_data[sheet] = df
    
    market_cap_df = pd.read_excel(file_path, sheet_name='Market Cap')
    detailed_df = pd.read_excel(file_path, sheet_name='SW (2)')
    
    return company_data, market_cap_df, detailed_df

def extract_company_metrics(df):
    company_name = df.iloc[0, 0] if not pd.isna(df.iloc[0, 0]) else "Unknown"
    esg_score = df.iloc[1, 1] if not pd.isna(df.iloc[1, 1]) else 0
    rating = df.iloc[1, 2] if len(df.columns) > 2 and not pd.isna(df.iloc[1, 2]) else "N/A"
    
    metrics = []
    for idx in range(4, len(df)):
        row = df.iloc[idx]
        if not pd.isna(row[0]) and not pd.isna(row[3]):
            metric_name = row[0]
            weight = row[2] if not pd.isna(row[2]) else 0
            score = row[3] if not pd.isna(row[3]) else 0
            disclosure = row[4] if len(row) > 4 and not pd.isna(row[4]) else 0
            peer_rank = row[5] if len(row) > 5 and not pd.isna(row[5]) else "N/A"
            
            metrics.append({
                'Metric': metric_name,
                'Weight': weight,
                'Score': score,
                'Disclosure': disclosure,
                'Peer Rank': peer_rank
            })
    
    return company_name, esg_score, rating, pd.DataFrame(metrics)

def main():
    company_data, market_cap_df, detailed_df = load_data()
    
    st.title("🌱 ESG Peer-to-Peer Review Dashboard")
    st.markdown("**Packaging Industry Sustainability Performance Analysis**")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "💼 Market Analysis", 
        "🔍 Company Deep Dive",
        "📈 Pillar Breakdown",
        "🎯 Peer Rankings"
    ])
    
    with tab1:
        st.header("ESG Scores Overview")
        
        company_map = {
            'SW': 'Smurfit Westrock',
            'PKG': 'Packaging Corp',
            'IP': 'International Paper',
            'GPI': 'Graphic Packaging',
            'SK': 'Smurfit Kappa',
            'WK': 'Westrock Company'
        }
        
        overview_data = []
        for ticker, df in company_data.items():
            _, esg_score, rating, _ = extract_company_metrics(df)
            overview_data.append({
                'Ticker': ticker,
                'Company': company_map.get(ticker, ticker),
                'ESG Score': esg_score,
                'Rating': rating
            })
        
        overview_df = pd.DataFrame(overview_data)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(
                overview_df.sort_values('ESG Score', ascending=True),
                x='ESG Score',
                y='Company',
                orientation='h',
                color='ESG Score',
                color_continuous_scale='RdYlGn',
                text='ESG Score',
                title='ESG Score Comparison'
            )
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig.update_layout(height=400, showlegend=False, xaxis_title="ESG Score", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Score Rankings")
            ranked = overview_df.sort_values('ESG Score', ascending=False).reset_index(drop=True)
            ranked.index = ranked.index + 1
            st.dataframe(
                ranked[['Company', 'ESG Score', 'Rating']],
                use_container_width=True,
                height=400
            )
        
        st.subheader("Performance Distribution")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_score = overview_df['ESG Score'].mean()
            st.metric("Average ESG Score", f"{avg_score:.2f}")
        
        with col2:
            top_performer = overview_df.loc[overview_df['ESG Score'].idxmax(), 'Company']
            top_score = overview_df['ESG Score'].max()
            st.metric("Top Performer", top_performer, f"{top_score:.2f}")
        
        with col3:
            score_range = overview_df['ESG Score'].max() - overview_df['ESG Score'].min()
            st.metric("Score Range", f"{score_range:.2f}")
    
    with tab2:
        st.header("Market Capitalization Analysis")
        
        market_cap_df['Market Cap (B)'] = market_cap_df['Market Capital'] / 1e9
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                market_cap_df,
                values='Market Cap (B)',
                names='Name',
                title='Market Share by Capitalization',
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            merged_df = pd.merge(
                overview_df,
                market_cap_df[['Tick', 'Market Cap (B)']],
                left_on='Ticker',
                right_on='Tick',
                how='left'
            )
            
            fig = px.scatter(
                merged_df,
                x='Market Cap (B)',
                y='ESG Score',
                size='Market Cap (B)',
                color='Company',
                hover_data=['Ticker'],
                title='ESG Score vs Market Capitalization',
                labels={'Market Cap (B)': 'Market Cap ($B)', 'ESG Score': 'ESG Score'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Market Cap Rankings")
        market_display = market_cap_df.sort_values('Market Cap (B)', ascending=False).copy()
        market_display['Market Cap ($B)'] = market_display['Market Cap (B)'].apply(lambda x: f"${x:.2f}B")
        st.dataframe(
            market_display[['Tick', 'Name', 'Market Cap ($B)']],
            use_container_width=True,
            hide_index=True
        )
    
    with tab3:
        st.header("Company Deep Dive")
        
        company_map = {
            'SW': 'Smurfit Westrock',
            'PKG': 'Packaging Corp',
            'IP': 'International Paper',
            'GPI': 'Graphic Packaging',
            'SK': 'Smurfit Kappa',
            'WK': 'Westrock Company'
        }
        
        selected_company = st.selectbox(
            "Select Company",
            options=list(company_map.keys()),
            format_func=lambda x: f"{x} - {company_map[x]}"
        )
        
        company_name, esg_score, rating, metrics_df = extract_company_metrics(
            company_data[selected_company]
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Company", company_name)
        with col2:
            st.metric("ESG Score", f"{esg_score:.2f}")
        with col3:
            st.metric("Rating", rating)
        
        st.subheader("Pillar Performance")
        
        pillars = metrics_df[metrics_df['Metric'].isin(['Environmental', 'Social', 'Governance'])].copy()
        
        if not pillars.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=pillars['Metric'],
                    y=pillars['Score'],
                    text=pillars['Score'].apply(lambda x: f'{x:.2f}'),
                    textposition='outside',
                    marker_color=['#2ecc71', '#3498db', '#9b59b6']
                ))
                fig.update_layout(
                    title='ESG Pillar Scores',
                    yaxis_title='Score',
                    xaxis_title='Pillar',
                    height=350
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(
                    pillars[['Metric', 'Score', 'Weight', 'Peer Rank']],
                    use_container_width=True,
                    hide_index=True,
                    height=350
                )
        
        st.subheader("Detailed Metrics")
        
        detailed_metrics = metrics_df[~metrics_df['Metric'].isin(['E', 'S', 'G', 'Environmental', 'Social', 'Governance'])]
        
        if not detailed_metrics.empty:
            fig = px.bar(
                detailed_metrics.sort_values('Score', ascending=True).tail(15),
                x='Score',
                y='Metric',
                orientation='h',
                color='Disclosure',
                color_continuous_scale='Blues',
                title='Top 15 Metrics by Score',
                labels={'Score': 'Score', 'Metric': 'Metric Name'}
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(
                detailed_metrics.sort_values('Score', ascending=False),
                use_container_width=True,
                hide_index=True
            )
    
    with tab4:
        st.header("ESG Pillar Breakdown Analysis")
        
        all_pillars = []
        for ticker, df in company_data.items():
            company_name, _, _, metrics_df = extract_company_metrics(df)
            pillars = metrics_df[metrics_df['Metric'].isin(['Environmental', 'Social', 'Governance'])].copy()
            pillars['Company'] = company_map.get(ticker, ticker)
            pillars['Ticker'] = ticker
            all_pillars.append(pillars)
        
        combined_pillars = pd.concat(all_pillars, ignore_index=True)
        
        pillar_options = st.multiselect(
            "Select Pillars to Compare",
            options=['Environmental', 'Social', 'Governance'],
            default=['Environmental', 'Social', 'Governance']
        )
        
        if pillar_options:
            filtered_data = combined_pillars[combined_pillars['Metric'].isin(pillar_options)]
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    filtered_data,
                    x='Company',
                    y='Score',
                    color='Metric',
                    barmode='group',
                    title='Pillar Score Comparison',
                    labels={'Score': 'Score', 'Company': 'Company'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                pivot_data = filtered_data.pivot_table(
                    values='Score',
                    index='Company',
                    columns='Metric',
                    aggfunc='first'
                ).fillna(0)
                
                fig = go.Figure()
                for pillar in pillar_options:
                    if pillar in pivot_data.columns:
                        fig.add_trace(go.Scatterpolar(
                            r=pivot_data[pillar],
                            theta=pivot_data.index,
                            fill='toself',
                            name=pillar
                        ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                    showlegend=True,
                    title='Radar Chart: Pillar Performance',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Weighted Contribution")
            
            weighted_data = filtered_data.copy()
            weighted_data['Weighted Score'] = weighted_data['Score'] * weighted_data['Weight']
            
            fig = px.sunburst(
                weighted_data,
                path=['Metric', 'Company'],
                values='Weighted Score',
                title='Weighted Score Distribution by Pillar',
                color='Score',
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("Peer Rankings Analysis")
        
        all_metrics = []
        for ticker, df in company_data.items():
            company_name, esg_score, rating, metrics_df = extract_company_metrics(df)
            metrics_df['Company'] = company_map.get(ticker, ticker)
            metrics_df['Ticker'] = ticker
            metrics_df['ESG Score'] = esg_score
            all_metrics.append(metrics_df)
        
        combined_metrics = pd.concat(all_metrics, ignore_index=True)
        
        rank_distribution = combined_metrics['Peer Rank'].value_counts().reset_index()
        rank_distribution.columns = ['Peer Rank', 'Count']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                rank_distribution,
                values='Count',
                names='Peer Rank',
                title='Distribution of Peer Rankings',
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            rank_by_company = combined_metrics.groupby(['Company', 'Peer Rank']).size().reset_index(name='Count')
            fig = px.bar(
                rank_by_company,
                x='Company',
                y='Count',
                color='Peer Rank',
                title='Peer Rank Distribution by Company',
                barmode='stack'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Leading Metrics by Company")
        
        leading_metrics = combined_metrics[combined_metrics['Peer Rank'] == 'Leading']
        
        if not leading_metrics.empty:
            leading_count = leading_metrics.groupby('Company').size().reset_index(name='Leading Metrics Count')
            leading_count = leading_count.sort_values('Leading Metrics Count', ascending=False)
            
            fig = px.bar(
                leading_count,
                x='Company',
                y='Leading Metrics Count',
                title='Number of Leading Metrics by Company',
                color='Leading Metrics Count',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(
                leading_metrics[['Company', 'Metric', 'Score', 'Disclosure', 'Weight']].sort_values(['Company', 'Score'], ascending=[True, False]),
                use_container_width=True,
                hide_index=True
            )
        
        st.subheader("Lagging Metrics Overview")
        
        lagging_metrics = combined_metrics[combined_metrics['Peer Rank'] == 'Lagging']
        
        if not lagging_metrics.empty:
            lagging_count = lagging_metrics.groupby('Company').size().reset_index(name='Lagging Metrics Count')
            lagging_count = lagging_count.sort_values('Lagging Metrics Count', ascending=False)
            
            fig = px.bar(
                lagging_count,
                x='Company',
                y='Lagging Metrics Count',
                title='Number of Lagging Metrics by Company',
                color='Lagging Metrics Count',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        """
        This dashboard provides comprehensive ESG peer-to-peer analysis 
        for the packaging industry, covering Environmental, Social, and 
        Governance metrics across leading companies.
        
        **Data Sources:** Company ESG reports and market data
        """
    )

if __name__ == "__main__":
    main()
