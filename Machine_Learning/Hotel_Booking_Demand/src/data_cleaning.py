import pandas as pd


def load_data():

    df = pd.read_csv('data_set/hotel_bookings.csv')

    return df


def clean_data(df):

    df['children'] = df['children'].fillna(0)

    df['country'] = df['country'].fillna('Unknown')

    df['agent'] = df['agent'].fillna(0)

    df['company'] = df['company'].fillna(0)

    df.drop_duplicates(inplace=True)

    df['total_guests'] = (
        df['adults'] +
        df['children'] +
        df['babies']
    )

    return df