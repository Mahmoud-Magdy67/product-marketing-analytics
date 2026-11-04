import pandas as pd
from .data_load import load

def analyze(start=None, end=None):
    mql = load('mql')
    deals = load('deals')
    orders = load('orders')
    items = load('items')
    mql['first_contact_date'] = pd.to_datetime(mql['first_contact_date'])
    if start is not None: mql = mql[mql.first_contact_date >= pd.Timestamp(start)]
    if end is not None: mql = mql[mql.first_contact_date <= pd.Timestamp(end)]
    # No sales-qualified lead table exists. Complete attribution fields are an explicit proxy.
    sql = mql[mql['landing_page_id'].notna() & mql['origin'].notna()]
    deal = deals[deals.mql_id.isin(sql.mql_id)].drop_duplicates('mql_id').merge(sql[['mql_id','first_contact_date']],on='mql_id',how='left')
    seller_first = items.merge(orders[['order_id','order_purchase_timestamp']], on='order_id').groupby('seller_id', as_index=False)['order_purchase_timestamp'].min()
    converted = deal.merge(seller_first, on='seller_id', how='inner')
    converted = converted[converted.order_purchase_timestamp >= converted.first_contact_date]
    converted = converted.drop_duplicates('mql_id')
    counts = [mql.mql_id.nunique(), sql.mql_id.nunique(), deal.mql_id.nunique(), converted.mql_id.nunique()]
    stages = ['MQL', 'SQL proxy', 'Closed deal', 'First order']
    table = pd.DataFrame({'stage': stages, 'count': counts})
    table['step_conversion'] = [1.0] + [counts[i]/counts[i-1] if counts[i-1] else 0 for i in range(1,4)]
    table['overall_conversion'] = [x/counts[0] if counts[0] else 0 for x in counts]
    table['drop_off'] = 1-table['step_conversion']
    median_days = (converted.order_purchase_timestamp - converted.first_contact_date).dt.total_seconds().div(86400).median()
    segment = pd.DataFrame()
    if 'business_segment' in deal:
        segment = deal.groupby('business_segment').agg(closed_deals=('mql_id','nunique')).reset_index()
        first = converted.groupby('business_segment').agg(first_orders=('mql_id','nunique')).reset_index()
        segment = segment.merge(first, how='left').fillna({'first_orders':0})
        segment['deal_to_order'] = segment.first_orders / segment.closed_deals
    return table, segment, float(median_days) if pd.notna(median_days) else None

if __name__ == '__main__':
    print(analyze()[0].to_string(index=False))
