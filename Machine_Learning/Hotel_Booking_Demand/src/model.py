from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def train_model(df):

    # Fill missing values
    df['children'] = df['children'].fillna(0)
    df['country'] = df['country'].fillna('Unknown')
    df['agent'] = df['agent'].fillna(0)
    df['company'] = df['company'].fillna(0)

    # Remove useless columns
    df = df.drop(columns=[
        'reservation_status',
        'reservation_status_date'
    ], errors='ignore')

    # Feature Engineering
    df['total_guests'] = (
        df['adults'] +
        df['children'] +
        df['babies']
    )

    df['total_nights'] = (
        df['stays_in_weekend_nights'] +
        df['stays_in_week_nights']
    )

    # Remove extreme ADR outliers
    df = df[df['adr'] < 500]

    # Encode categorical columns
    le = LabelEncoder()

    categorical_columns = [
        'hotel',
        'meal',
        'country',
        'market_segment',
        'distribution_channel',
        'reserved_room_type',
        'assigned_room_type',
        'deposit_type',
        'customer_type',
        'arrival_date_month'
    ]

    for col in categorical_columns:
        df[col] = le.fit_transform(df[col].astype(str))

    # Features
    X = df[[
        'lead_time',
        'arrival_date_week_number',
        'arrival_date_day_of_month',
        'stays_in_weekend_nights',
        'stays_in_week_nights',
        'adults',
        'children',
        'babies',
        'is_repeated_guest',
        'previous_cancellations',
        'previous_bookings_not_canceled',
        'booking_changes',
        'days_in_waiting_list',
        'adr',
        'required_car_parking_spaces',
        'total_of_special_requests',
        'total_guests',
        'total_nights',
        'booking_changes',
        'hotel',
        'meal',
        'country',
        'market_segment',
        'distribution_channel',
        'reserved_room_type',
        'assigned_room_type',
        'deposit_type',
        'customer_type',
        'arrival_date_month'
    ]]

    # Target
    y = df['is_canceled']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.1,
        random_state=42,
        stratify=y
    )

    # Random Forest
    model = RandomForestClassifier(
        n_estimators=1500,
        max_depth=40,
        min_samples_split=2,
        min_samples_leaf=1,
        bootstrap=False,
        random_state=42,
        n_jobs=-1
    )

    # Train
    model.fit(X_train, y_train)

    # Predict
    predictions = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, predictions)

    print("\nModel Accuracy:", accuracy)

    print("\nClassification Report:\n")
    print(classification_report(y_test, predictions))

    return model