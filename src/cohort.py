import pandas as pd
from .data_load import load

def analyze(start=None, end=None):
    orders = load('orders')[['order_id','customer_id','order_purchase_timestamp']]
    customers = load('customers')[['customer_id','customer_unique_id']]
    payments = load('payments').groupby('order_id',as_index=False)['payment_value'].sum()
    frame = orders.merge(customers,on='customer_id').merge(payments,on='order_id',how='left')
    frame['month'] = frame.order_purchase_timestamp.dt.to_period('M')
    first = frame.groupby('customer_unique_id')['month'].min().rename('cohort')
    frame = frame.join(first,on='customer_unique_id')
    # Cohort membership is assigned on the full history before the display filter.
    if start is not None: frame = frame[frame.cohort >= pd.Timestamp(start).to_period('M')]
    if end is not None: frame = frame[frame.cohort <= pd.Timestamp(end).to_period('M')]
    frame['age'] = (frame.month.dt.year-frame.cohort.dt.year)*12 + frame.month.dt.month-frame.cohort.dt.month
    frame = frame[(frame.age >= 0)&(frame.age <= 12)]
    size = frame.groupby('cohort')['customer_unique_id'].nunique().rename('customers')
    active = frame.groupby(['cohort','age'])['customer_unique_id'].nunique().unstack(fill_value=0).reindex(columns=range(13),fill_value=0)
    retention = active.div(size,axis=0)
    # Do not display unobserved future months as zero retention.
    last_month = orders.order_purchase_timestamp.max().to_period('M')
    for cohort in retention.index:
        for age in retention.columns:
            if cohort + age > last_month: retention.loc[cohort,age] = float('nan')
    revenue = frame.groupby(['cohort','age'])['payment_value'].sum().unstack(fill_value=0).reindex(columns=range(13),fill_value=0)
    retention.index = retention.index.astype(str); revenue.index = revenue.index.astype(str); size.index = size.index.astype(str)
    return retention, revenue, size

if __name__ == '__main__':
    r,v,s=analyze(); print(pd.concat([s,r[[1,3]]],axis=1).head(6).to_string())
