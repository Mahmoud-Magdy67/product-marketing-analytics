from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
PROCESSED = ROOT / 'data' / 'processed'
TABLES = {
    'mql': 'olist_marketing_qualified_leads_dataset.csv',
    'deals': 'olist_closed_deals_dataset.csv',
    'orders': 'olist_orders_dataset.csv',
    'items': 'olist_order_items_dataset.csv',
    'customers': 'olist_customers_dataset.csv',
    'reviews': 'olist_order_reviews_dataset.csv',
    'payments': 'olist_order_payments_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
}

def prepare():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    audit = []
    for name, filename in TABLES.items():
        frame = pd.read_csv(RAW / filename, low_memory=False)
        frame.columns = frame.columns.str.strip().str.lower().str.replace(r'[^a-z0-9]+', '_', regex=True).str.strip('_')
        frame = frame.drop_duplicates()
        for column in frame.columns:
            if column.endswith('_date') or column.endswith('_timestamp'):
                frame[column] = pd.to_datetime(frame[column], errors='coerce')
        frame.to_parquet(PROCESSED / f'{name}.parquet', index=False)
        audit.append((name, len(frame), int(frame.isna().sum().sum())))
    print('table,rows,null_cells')
    for row in audit: print(','.join(map(str, row)))
    print('order_date_range', pd.read_parquet(PROCESSED / 'orders.parquet')['order_purchase_timestamp'].agg(['min','max']).to_dict())

def load(name):
    return pd.read_parquet(PROCESSED / f'{name}.parquet')

if __name__ == '__main__': prepare()
