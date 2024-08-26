from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image

import io

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
    - Add functionality so that app knows the date, and in which monthly cycle it is. DONE
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

    if df.empty:
        return days_elapsed

    # Filter the DataFrame for entries in the current month
    current_month_entries = df[df['Timestamp'].dt.month == current_date.month]

    # Calculate the total spending for the current month
    total_spending_month = current_month_entries['Betrag'].sum()

    # Calculate the expected spending based on the daily budget
    expected_spending = days_elapsed * daily_budget

    # Calculate the budget counter
    budget_counter = (expected_spending - total_spending_month) / daily_budget

    return round(budget_counter)


daily_budget = 25  # Set the daily budget
budget_counter = calculate_budget_counter(daily_budget)
print("Budget Counter for the current month:", budget_counter)

# Visualizations
def generate_pie_chart():
    # Example data for the pie chart
    categories = df['Kategorie'].unique()
    spending = [df[df['Kategorie'] == category]['Betrag'].sum() for category in categories]

    # Create a larger pie chart with transparent background
    fig, ax = plt.subplots(figsize=(6, 6))  # Adjust figsize for larger image

    # Generate pie chart with larger font size and no border
    wedges, texts, autotexts = ax.pie(
        spending,
        labels=categories,
        autopct='%1.1f%%',
        startangle=90,
        textprops=dict(fontsize=14),  # Increase font size
    )

    for text in texts:
        text.set_fontsize(14)  # Set font size for labels

    for autotext in autotexts:
        autotext.set_fontsize(14)  # Set font size for percentages

    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

    # Save the pie chart to a BytesIO object with transparent background
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')  # Transparent background and no extra border
    buf.seek(0)
    plt.close(fig)  # Close the figure to free memory

    return buf

# GUI stuff
# Custom popup class to get amount and label
class EntryPopup(Popup):
    def __init__(self, category, on_submit, **kwargs):
        super().__init__(**kwargs)
        self.title = f'Add Entry to {category}'
        self.on_submit = on_submit
        self.category = category
        self.size_hint = (0.8, 0.4)

        # Layout
        layout = GridLayout(cols=2, padding=5, spacing=5)

        # Label and TextInput for 'Label'
        layout.add_widget(Label(text='Label'))
        self.label_input = TextInput(multiline=False, size_hint_y=None, height=40)  # Single-line text input
        layout.add_widget(self.label_input)

        # Label and TextInput for 'Amount'
        layout.add_widget(Label(text='Amount'))
        self.amount_input = TextInput(multiline=False, input_filter='float', size_hint_y=None, height=40)  # Single-line text input
        layout.add_widget(self.amount_input)

        # Buttons for Submit and Cancel
        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        submit_button = Button(text='Submit', on_press=self.submit_entry)
        cancel_button = Button(text='Cancel', on_press=self.dismiss)
        button_layout.add_widget(submit_button)
        button_layout.add_widget(cancel_button)

        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=10)
        main_layout.add_widget(layout)
        main_layout.add_widget(button_layout)

        self.content = main_layout

        # Bind keyboard events
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, window, key, *args):
        if key == 9:  # Tab key
            if self.label_input.focus:
                self.label_input.focus = False
                self.amount_input.focus = True
            elif self.amount_input.focus:
                self.amount_input.focus = False
                self.label_input.focus = True
            return True
        elif key == 306:  # Shift+Tab key
            if self.amount_input.focus:
                self.amount_input.focus = False
                self.label_input.focus = True
            elif self.label_input.focus:
                self.label_input.focus = False
                self.amount_input.focus = True
            return True
        return False

    def submit_entry(self, instance):
        label = self.label_input.text
        amount = self.amount_input.text
        if label and amount:
            add_entry(self.category, label, float(amount))
            self.on_submit()  # Call without arguments
            self.dismiss()

    def cancel_entry(self, instance):
        self.dismiss()

# Main layout with buttons for each category
class BudgetApp(App):
    def build(self):
        # Main layout of the app
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Layout for the top section (totals and counters)
        self.top_layout = BoxLayout(orientation='vertical', size_hint_y=0.3)

        # Create labels for total spending and budget counter
        self.total_spending_label = Label(text="Total Spending: $0")
        self.budget_counter_label = Label(text="Budget Counter: 0")

        # Add labels to the top layout
        self.top_layout.add_widget(self.total_spending_label)
        self.top_layout.add_widget(self.budget_counter_label)

        # Layout for the pie chart
        self.pie_chart_image = Image(size_hint_y=0.4)
        self.update_pie_chart()

        # Layout for the buttons at the bottom
        self.bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)

        # Categories
        categories = ["Rent",
                      "Groceries",
                      "Transport",
                      "Health",
                      "Entertainment"]

        # Create buttons for each category
        for i, category in enumerate(categories, start=1):
            button = Button(text=f"{category}")
            button.bind(on_press=lambda instance, cat=category: self.show_entry_popup(cat))
            self.bottom_layout.add_widget(button)

        # Add all widgets to the main layout
        main_layout.add_widget(self.top_layout)
        main_layout.add_widget(self.pie_chart_image)
        main_layout.add_widget(Widget())  # Spacer in the middle
        main_layout.add_widget(self.bottom_layout)

        # Update totals and counters
        self.update_totals_and_counters()
        return main_layout

    def show_entry_popup(self, category):
        # Create and open the popup for data entry
        popup = EntryPopup(category, self.update_totals_and_counters)
        popup.open()

    def update_totals_and_counters(self):
        # Calculate the total spending
        total_spending = df['Betrag'].sum()

        # Calculate the budget counter (you might need to adjust this based on your logic)
        # For now, let's assume a simple budget logic
        daily_budget = 25  # Example daily budget
        days_in_month = datetime.now().day
        expected_spending = daily_budget * days_in_month
        budget_counter = (expected_spending - total_spending) / daily_budget

        # Update the labels
        self.total_spending_label.text = f"Total Spending: ${total_spending:.2f}"
        self.budget_counter_label.text = f"Budget Counter: {budget_counter:.2f}"

    def update_pie_chart(self):
        pie_chart_buf = generate_pie_chart()
        img = CoreImage(pie_chart_buf, ext='png')
        self.pie_chart_image.texture = img.texture

    def update_totals_and_counters(self):
        # Calculate the total spending
        total_spending = df['Betrag'].sum()

        # Calculate the budget counter (you might need to adjust this based on your logic)
        daily_budget = 25  # Example daily budget
        days_in_month = datetime.now().day
        expected_spending = daily_budget * days_in_month
        budget_counter = (expected_spending - total_spending) / daily_budget

        # Update the labels
        self.total_spending_label.text = f"Total Spending: ${total_spending:.2f}"
        self.budget_counter_label.text = f"Budget Counter: {budget_counter:.2f}"

        # Update the pie chart
        self.update_pie_chart()

if __name__ == '__main__':
    BudgetApp().run()