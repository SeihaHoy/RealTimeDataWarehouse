import random
from datetime import datetime, timedelta
import pandas as pd


num_rows = 50
output_file = './account_dim_large_data.csv'

account_ids = []
account_types = []
statuses = []
customer_ids = []
balances = []
opening_dates = []


def generate_account_dim(row_num):
    account_id = f'A{row_num:05d}' # A00001, A00002, ...
    account_type = random.choice(['SAVINGS', 'CHECKING'])
    status = random.choice(['ACTIVE', 'INACTIVE'])
    customer_id = f'C{random.randint(1, 1000):05d}' # C00001, C00002, ...
    balance = round(random.uniform(100.00, 10000.00), 2)
    
    # Generate a random date between 2010-01-01 and 2024-09-01
    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 365))
    opening_date_millis = int(random_date.timestamp() * 1000)
    
    return account_id, account_type, status, customer_id, balance, opening_date_millis

def generate_account_dim_data():
    row_num = 1
    while row_num <= num_rows:
        account_id, account_type, status, customer_id, balance, opening_date_millis = generate_account_dim(row_num)
        account_ids.append(account_id)
        account_types.append(account_type)
        statuses.append(status)
        customer_ids.append(customer_id)
        balances.append(balance)
        opening_dates.append(opening_date_millis)
        row_num += 1
        
    df = pd.DataFrame({
        'account_id': account_ids,
        'account_type': account_types,
        'status': statuses,
        'customer_id': customer_ids,
        'balance': balances,
        'opening_date': opening_dates
    })

    df.to_csv(output_file, index=False)

    print(f'Generated {num_rows} rows of account dimension data in {output_file}')