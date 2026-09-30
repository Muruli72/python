import matplotlib.pyplot as plt


def hotel_booking_chart(df):

    df['hotel'].value_counts().plot(kind='bar')

    plt.title('Hotel Booking Count')
    plt.xlabel('Hotel Type')
    plt.ylabel('Bookings')

    plt.show()


def adr_histogram(df):

    plt.hist(df['adr'])

    plt.title('ADR Distribution')
    plt.xlabel('ADR')
    plt.ylabel('Frequency')

    plt.show()


def scatter_plot(df):

    plt.scatter(df['total_guests'], df['adr'])

    plt.title('Guests vs ADR')
    plt.xlabel('Total Guests')
    plt.ylabel('ADR')

    plt.show()


def pie_chart(df):

    df['hotel'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Hotel Booking Percentage')

    plt.show()