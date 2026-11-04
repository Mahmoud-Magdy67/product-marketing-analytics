import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from statsmodels.stats.power import TTestIndPower
from src.funnel import analyze as funnel_analysis
from src.ab_test import analyze as ab_analysis
from src.cohort import analyze as cohort_analysis
from src.data_load import load

st.set_page_config(layout='wide', page_title='Product & Marketing Analytics Sandbox')
st.title('Product & Marketing Analytics Sandbox')
st.caption('Marketing funnel, A/B testing, and cohort retention on Brazilian e-commerce data')
st.sidebar.info('Source: public Olist Brazilian E-Commerce and Marketing Funnel datasets. The SQL stage is an attribution-completeness proxy. The A/B comparison is observational.')
mql = load('mql')
min_date = mql.first_contact_date.min().date(); max_date = mql.first_contact_date.max().date()
dates = st.sidebar.date_input('MQL date range', (min_date,max_date), min_value=min_date,max_value=max_date)
start,end = (dates[0],dates[1]) if isinstance(dates,tuple) and len(dates)==2 else (min_date,max_date)
tabs = st.tabs(['Marketing Funnel','A/B Test','Cohort Retention'])

with tabs[0]:
    funnel,segment,median_days = funnel_analysis(start,end)
    a,b,c = st.columns(3)
    a.metric('MQLs',f'{funnel.iloc[0]["count"]:,}')
    b.metric('First-order conversion',f'{funnel.iloc[-1]["overall_conversion"]:.1%}')
    c.metric('Median MQL to first order',f'{median_days:.0f} days' if median_days is not None else 'N/A')
    fig=go.Figure(go.Funnel(y=funnel.stage,x=funnel['count'],textinfo='value+percent initial'))
    fig.update_layout(title='Seller acquisition funnel',height=390)
    st.plotly_chart(fig,use_container_width=True)
    display=funnel.copy()
    for col in ['step_conversion','overall_conversion','drop_off']: display[col]=display[col].map(lambda x:f'{x:.1%}')
    st.dataframe(display,width='stretch',hide_index=True)
    st.caption('SQL proxy: MQLs with both landing page and origin populated. Olist does not supply an observed SQL event. First order means the seller’s earliest marketplace order occurred after first contact.')
    if not segment.empty:
        st.subheader('By business segment')
        st.dataframe(segment.sort_values('closed_deals',ascending=False),width='stretch',hide_index=True)

with tabs[1]:
    r=ab_analysis()
    st.info(f'Quasi-experiment: treatment = sellers with a first recorded sale after the median ({r["cutoff_date"]}); control = sellers on or before it. First sale is a proxy for onboarding date. No actual platform update or flow assignment is recorded, so this is an observational comparison, not a true randomized trial or causal estimate.')
    left,right=st.columns([1,1])
    with left:
        fig=px.bar(x=['Earlier sellers (control)','Later sellers (proxy treatment)'],y=[r['mean_control'],r['mean_treatment']],
                   error_y=[1.96*r['sd_control']/np.sqrt(r['n_control']),1.96*r['sd_treatment']/np.sqrt(r['n_treatment'])],
                   labels={'x':'Group','y':'Mean seller review score'},title='Seller-level mean review score')
        fig.update_yaxes(range=[0,5]); st.plotly_chart(fig,use_container_width=True)
    with right:
        stats_table=pd.DataFrame({'Metric':['Control n','Treatment n','Control mean','Treatment mean','Difference','Welch t','p-value','Cohen d','95% CI','Observed-effect power','Design power at 0.2 points'],
          'Value':[r['n_control'],r['n_treatment'],f'{r["mean_control"]:.3f}',f'{r["mean_treatment"]:.3f}',f'{r["difference"]:+.3f}',f'{r["t_stat"]:.3f}',f'{r["p_value"]:.2g}',f'{r["cohens_d"]:+.3f}',f'[{r["ci_low"]:.3f}, {r["ci_high"]:.3f}]',f'{r["power"]:.1%}',f'{r["design_power_0_2"]:.1%}']})
        stats_table['Value'] = stats_table['Value'].astype(str)
        st.dataframe(stats_table,hide_index=True,width='stretch')
    verdict=('Statistically significant' if r['significant'] else 'No statistically significant difference')
    (st.success if r['significant'] else st.info)(f'{verdict} at α = 0.05. Observed difference: {r["difference"]:+.3f} review points. The illustrative practical threshold is 0.2 points; this estimate falls below it. The comparison does not establish an onboarding effect.')
    st.caption('Observed-effect power is descriptive and should not be treated as independent evidence. Design power at a prespecified 0.2-point difference is more useful for planning. Calendar time, seller mix, order volume, and other factors may confound this comparison.')
    effects=np.linspace(.02,.5,50)
    powers=[TTestIndPower().power(x,nobs1=r['n_treatment'],ratio=r['n_control']/r['n_treatment'],alpha=.05) for x in effects]
    fig=px.line(x=effects,y=powers,labels={'x':'Assumed absolute Cohen d','y':'Power'},title='Design power across assumed effect sizes')
    fig.add_hline(y=.8,line_dash='dash'); st.plotly_chart(fig,use_container_width=True)

with tabs[2]:
    retention,revenue,size=cohort_analysis()
    st.caption('Cohorts use the first purchase of each unique customer. Month 0 is acquisition; months 1–12 show repeat purchase in each calendar month. Recent cohorts have incomplete follow-up.')
    show=retention.tail(18)
    fig=px.imshow(show,labels={'x':'Months since first order','y':'First-order cohort','color':'Retention'},
                  color_continuous_scale='Blues',zmin=0,aspect='auto',title='Monthly repeat purchase retention')
    st.plotly_chart(fig,use_container_width=True)
    line=retention.iloc[:-3].tail(8).T
    st.plotly_chart(px.line(line,markers=True,labels={'index':'Month since first order','value':'Retention','variable':'Cohort'},title='Retention curves: recent mature cohorts'),use_container_width=True)
    rev=revenue.sum(axis=1).sort_values(ascending=False).head(12)
    st.plotly_chart(px.bar(x=rev.index,y=rev.values,labels={'x':'Cohort','y':'Total payment revenue (BRL)'},title='Top cohorts by observed revenue'),use_container_width=True)
    st.dataframe(pd.concat([size,retention[[1,3]].rename(columns={1:'month_1',3:'month_3'}),revenue.sum(axis=1).rename('revenue_brl')],axis=1),width='stretch')

st.divider()
st.caption('Built by Mahmoud Magdy · GitHub link: add repository URL after publishing')
