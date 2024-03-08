import pandas as pd
from datetime import datetime, timedelta

def rearrange_columns(df):
    date_columns = [col for col in df.columns if 'date' in col]
    sorted_date_columns = sorted(date_columns, key=lambda x: pd.to_datetime(df[x].dropna().min()))
    desired_order = [col for col in df.columns if col not in date_columns] + sorted_date_columns
    return df[desired_order]

def inherit_previous_value(data):
    last_comp = last_comp_idx = compensation = compensation_idx = None
    for i, row in enumerate(data):
        if row['Employee Code'] != data[i - 1]['Employee Code'] if i > 0 else True:
            last_comp = last_comp_idx = compensation = compensation_idx = None
        if not row['Last Compensation']:
            row['Last Compensation'] = data[last_comp_idx]['Last Compensation'] if last_comp_idx else last_comp
        else:
            last_comp, last_comp_idx = row['Last Compensation'], i
        if not row['Compensation']:
            row['Compensation'] = data[compensation_idx]['Compensation'] if compensation_idx else compensation
        else:
            compensation, compensation_idx = row['Compensation'], i
    return data

def assign_last_pay_raise_date(data):
    last_compensation = last_pay_raise_date = None
    for index, row in data.iterrows():
        if row['Compensation'] != last_compensation:
            last_pay_raise_date = row['Effective Date']
        last_compensation = row['Compensation']
        if pd.isnull(row['Last Compensation']):
            last_pay_raise_date = None
        data.at[index, 'Last Pay Raise Date'] = last_pay_raise_date
    return data

def assign_end_date(data):
    data = data.dropna(subset=['Effective Date'])
    data['Effective Date'] = pd.to_datetime(data['Effective Date'], format='%d-%m-%y')
    data['End Date'] = data['Effective Date'].shift(-1) - timedelta(days=1)
    last_employee_code = None
    for index, row in data.iterrows():
        if row['Employee Code'] != last_employee_code:
            data.at[index - 1, 'End Date'] = datetime(2100, 1, 1) if last_employee_code else None
        last_employee_code = row['Employee Code']
    data = data[:-1]
    data.loc[data['End Date'].isnull(), 'End Date'] = '01-01-00'
    return data

def process_data(input_file, output_file):
    df = pd.read_csv(input_file)
    df = rearrange_columns(df)
    
    output = []
    for index, row in df.iterrows():
        if not pd.isnull(row['Compensation']):
            last_comp = row['Compensation']
            last_perf_rating = last_engagement_score = ''
            output.append([row['Employee Code'], row['Manager Employee Code'], '', last_comp, '', '', row['Date of Joining']])
        if not pd.isnull(row['Engagement 1']):
            last_engagement_score = row['Engagement 1']
            output.append([row['Employee Code'], row['Manager Employee Code'], '', '', last_perf_rating, last_engagement_score, row['Engagement 1 date']])
        if not pd.isnull(row['Review 1']):
            last_perf_rating = row['Review 1']
            output.append([row['Employee Code'], row['Manager Employee Code'], '', '', last_perf_rating, last_engagement_score, row['Review 1 date']])
        if not pd.isnull(row['Compensation 1']):
            last_comp = row['Compensation 1']
            output.append([row['Employee Code'], row['Manager Employee Code'], row['Compensation'], last_comp, last_perf_rating, last_engagement_score, row['Compensation 1 date']])
        if not pd.isnull(row['Engagement 2']):
            last_engagement_score = row['Engagement 2']
            output.append([row['Employee Code'], row['Manager Employee Code'], '', '', last_perf_rating, last_engagement_score, row['Engagement 2 date']])
        if not pd.isnull(row['Review 2']):
            last_perf_rating = row['Review 2']
            output.append([row['Employee Code'], row['Manager Employee Code'], '', '', last_perf_rating, last_engagement_score, row['Review 2 date']])
        if not pd.isnull(row['Compensation 2']):
            last_comp = row['Compensation 2']
            output.append([row['Employee Code'], row['Manager Employee Code'], row['Compensation 1'], last_comp, last_perf_rating, last_engagement_score, row['Compensation 2 date']])
    
    output_df = pd.DataFrame(output, columns=['Employee Code', 'Manager Employee Code', 'Last Compensation', 'Compensation', 'Performance Rating', 'Engagement Score', 'Effective Date'])
    output_data = inherit_previous_value(output_df.to_dict(orient='records'))
    
    output_df_updated = pd.DataFrame(output_data)
    output_df_updated.insert(4, "Last Pay Raise Date", "")
    output_df_updated = assign_last_pay_raise_date(output_df_updated)
    output_df_updated = assign_end_date(output_df_updated)
    
    output_df_updated.to_csv(output_file, index=False)

process_data('input.csv', 'output.csv')
