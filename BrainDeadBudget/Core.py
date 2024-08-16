import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

kategorien = [
    ("Wohnen", 1),
    ("Lebensmittel & Haushaltswaren", 2),
    ("Transport", 3),
    ("Gesundheit und Pflege", 4),
    ("Freizeit", 5),
]

import pandas as pd
from datetime import datetime

# Initial empty DataFrame with EntryID column
df = pd.DataFrame(columns=['EntryID', 'Kategorie', 'Label', 'Betrag', 'Timestamp'])

# Variable to keep track of the next EntryID
next_entry_id = 0

# Function to add a new entry to the DataFrame
def add_entry(kategorie, label, betrag):
    global df, next_entry_id
    # Get the current timestamp
    timestamp = datetime.now()
    # Create a new row with the entry data, including the EntryID
    new_entry = pd.DataFrame({
        'EntryID': [next_entry_id],
        'Kategorie': [kategorie],
        'Label': [label],
        'Betrag': [betrag],
        'Timestamp': [timestamp]
    })
    # Append the new entry to the DataFrame
    df = pd.concat([df, new_entry], ignore_index=True)
    # Increment the EntryID for the next entry
    next_entry_id += 1

# Function to remove an entry by EntryID
def remove_entry(entry_id):
    global df
    # Check if the EntryID exists in the DataFrame
    if entry_id in df['EntryID'].values:
        # Drop the row with the specified EntryID
        df = df[df['EntryID'] != entry_id]
        print(f"Entry {entry_id} removed successfully.")
    else:
        print(f"Entry {entry_id} does not exist.")

# Example usage
add_entry(1, "Einkauf Grillen", 50.75)
add_entry(2, "Restaurant", 30.00)
add_entry(1, "Supermarkt", 15.20)

print("DataFrame before removal:")
print(df)

remove_entry(1)  # Remove the entry with EntryID 1

print("\nDataFrame after removal:")
print(df)


# Statistics stuff
'''
What kind of statistics are nice to have?
    - Visualization of spending in each category (pie chart)
    - Spending in each category over the months / weeks (as stacked bars?)
    - History of spending in a list
    - MAIN:
        - Daily Budget Counter (number of days in positive, total sum accumulated)
        - Total spending
    - On a PER MONTH basis
    
TODO:
    - Add functionality so that app knows the date, and in which monthly cycle it is.
    - Need to create one dataset per week, and then add the weeks to the monthly dataset
    - These monthly dataset will serve as the basis for the statistical stuff
'''

def get_total_spending_for_day(date):
    # Convert the date to a datetime object
    date = pd.to_datetime(date)
    # Filter the DataFrame for entries on the given day
    day_entries = df[df['Timestamp'].dt.date == date.date()]
    # Calculate the total spending for the day
    total_spending = day_entries['Betrag'].sum()
    return total_spending

def get_total_spending_for_week(date):
    # Convert the date to a datetime object
    date = pd.to_datetime(date)
    # Calculate the start and end of the week
    start_of_week = date - pd.Timedelta(days=date.weekday())
    end_of_week = start_of_week + pd.Timedelta(days=6)
    # Filter the DataFrame for entries in the given week
    week_entries = df[(df['Timestamp'] >= start_of_week) & (df['Timestamp'] <= end_of_week)]
    # Calculate the total spending for the week
    total_spending = week_entries['Betrag'].sum()
    return total_spending

def get_total_spending_for_month(year, month):
    # Filter the DataFrame for entries in the given month
    month_entries = df[(df['Timestamp'].dt.year == year) & (df['Timestamp'].dt.month == month)]
    # Calculate the total spending for the month
    total_spending = month_entries['Betrag'].sum()
    return total_spending


def calculate_budget_counter(daily_budget):
    global df
    # Get the current date
    current_date = datetime.now()

    # Determine the first day of the current month
    first_of_month = current_date.replace(day=1)

    # Calculate the total days elapsed in the current month including today
    days_elapsed = (current_date - first_of_month).days + 1

    # Filter the DataFrame for entries in the current month
    current_month_entries = df[df['Timestamp'].dt.month == current_date.month]

    # Calculate the total spending for the current month
    total_spending_month = current_month_entries['Betrag'].sum()

    # Calculate the expected spending based on the daily budget
    expected_spending = days_elapsed * daily_budget

    # Calculate the budget counter
    budget_counter = (expected_spending - total_spending_month) / daily_budget

    return round(budget_counter)


# Example usage
add_entry(1, "Einkauf Grillen", 50.75)
add_entry(2, "Restaurant", 30.00)
add_entry(1, "Supermarkt", 15.20)
add_entry(1, "Einkauf Grillen", 10.75)
add_entry(2, "Restaurant", 20.00)

daily_budget = 25  # Set the daily budget
budget_counter = calculate_budget_counter(daily_budget)
print("Budget Counter for the current month:", budget_counter)