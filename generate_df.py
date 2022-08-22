import pandas as pd


def get_clean_df(db_name):
    """ Get the df """
    df = pd.read_csv(db_name)
    df['word_count'] = df.post_text.str.replace('\n', ' ').str.count(' ') + 1
    df['full_time'] = pd.to_datetime(df.time, infer_datetime_format=True)
    df['hour'] = df.full_time.dt.hour
    base_month_fmt = '{}-{:02d}-25 00:00:00'
    df['base_month'] = [base_month_fmt.format(y, m)
                        for y, m in zip(df.full_time.dt.year, df.full_time.dt.month)]
    df['base_month'] = pd.to_datetime(df.base_month)

    return df
