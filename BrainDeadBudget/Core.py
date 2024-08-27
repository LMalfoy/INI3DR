'''
TODO:
- Archive: Look at past months. Show stacked bar graph to show how spending has changed in each category.
- View the complete list of spendings (chronologically and sorted by category, smallest to largest).

DONE:
- Visualization of spending in each category (pie chart).
- Daily Budget Counter (number of days in positive, total sum accumulated).
- Total spending.
- On a PER MONTH basis.
- Add functionality so that app knows the date and in which monthly cycle it is.
- Create one dataset per week and add the weeks to the monthly dataset.
- Save past entries into the database.
- Load database.
'''

# Import Libraries
# GUI
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Data Analysis
import pandas as pd
import matplotlib.pyplot as plt
import io
from datetime import datetime

# Database
import json
import os

# Initialize the DataFrame for storing entries
df = pd.DataFrame(columns=['EntryID', 'Kategorie', 'Label', 'Betrag', 'Timestamp'])
next_entry_id = 0  # Variable to keep track of the next EntryID


# Function to add a new entry to the DataFrame
def add_entry(kategorie, label, betrag):
    global df, next_entry_id
    timestamp = datetime.now()  # Get the current timestamp
    new_entry = pd.DataFrame({
        'EntryID': [next_entry_id],
        'Kategorie': [kategorie],
        'Label': [label],
        'Betrag': [betrag],
        'Timestamp': [timestamp]
    })
    df = pd.concat([df, new_entry], ignore_index=True)  # Append the new entry to the DataFrame
    next_entry_id += 1  # Increment the EntryID for the next entry
    print("New entry added:", new_entry)  # Print confirmation
    save_data_to_json()  # Save the updated DataFrame to JSON


# Function to remove an entry by EntryID
def remove_entry(entry_id):
    global df
    if entry_id in df['EntryID'].values:
        df = df[df['EntryID'] != entry_id]  # Drop the row with the specified EntryID
        print(f"Entry {entry_id} removed successfully.")
    else:
        print(f"Entry {entry_id} does not exist.")


# Saving the DataFrame to a JSON file
def save_data_to_json():
    data_dict = df.copy()
    data_dict['Timestamp'] = data_dict['Timestamp'].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
    data_dict = data_dict.to_dict(orient='records')

    with open('budget_data.json', 'w') as json_file:
        json.dump(data_dict, json_file)
    print("Data saved to budget_data.json")


# Loading the DataFrame from a JSON file
def load_data_from_json():
    global df
    if os.path.exists('budget_data.json'):
        with open('budget_data.json', 'r') as json_file:
            data_dict = json.load(json_file)
            df = pd.DataFrame(data_dict)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        print("Data loaded from budget_data.json")
    else:
        print("No data file found. Starting with an empty DataFrame.")


# Functions to calculate statistics
def get_total_spending_for_day(date):
    date = pd.to_datetime(date)
    day_entries = df[df['Timestamp'].dt.date == date.date()]
    total_spending = day_entries['Betrag'].sum()
    return total_spending


def get_total_spending_for_week(date):
    date = pd.to_datetime(date)
    start_of_week = date - pd.Timedelta(days=date.weekday())
    end_of_week = start_of_week + pd.Timedelta(days=6)
    week_entries = df[(df['Timestamp'] >= start_of_week) & (df['Timestamp'] <= end_of_week)]
    total_spending = week_entries['Betrag'].sum()
    return total_spending


def get_total_spending_for_month(year, month):
    month_entries = df[(df['Timestamp'].dt.year == year) & (df['Timestamp'].dt.month == month)]
    total_spending = month_entries['Betrag'].sum()
    return total_spending


def calculate_budget_counter(daily_budget):
    global df
    current_date = datetime.now()
    first_of_month = current_date.replace(day=1)
    days_elapsed = (current_date - first_of_month).days + 1

    if df.empty:
        return days_elapsed

    current_month_entries = df[df['Timestamp'].dt.month == current_date.month]
    total_spending_month = current_month_entries['Betrag'].sum()
    expected_spending = days_elapsed * daily_budget
    budget_counter = (expected_spending - total_spending_month) / daily_budget
    return round(budget_counter)


daily_budget = 25  # Set the daily budget
budget_counter = calculate_budget_counter(daily_budget)
print("Budget Counter for the current month:", budget_counter)


# Function to generate the pie chart visualization
def generate_pie_chart(width, height):
    categories = df['Kategorie'].unique()
    spending = [df[df['Kategorie'] == category]['Betrag'].sum() for category in categories]
    dpi = 100
    fig_width = width / dpi
    fig_height = height / dpi

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    wedges, texts, autotexts = ax.pie(
        spending,
        labels=categories,
        autopct='%1.1f%%',
        startangle=90,
        textprops=dict(color='white', fontsize=15),
    )

    for text in texts:
        text.set_color('white')
        text.set_fontsize(15)

    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(15)

    ax.axis('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf


# Custom popup class for adding a new entry
class EntryPopup(Popup):
    def __init__(self, category, on_submit, **kwargs):
        super().__init__(**kwargs)
        self.title = f'Add Entry to {category}'
        self.on_submit = on_submit
        self.category = category
        self.size_hint = (0.8, 0.4)

        layout = GridLayout(cols=2, padding=5, spacing=5)
        layout.add_widget(Label(text='Label'))
        self.label_input = TextInput(multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.label_input)

        layout.add_widget(Label(text='Amount'))
        self.amount_input = TextInput(multiline=False, input_filter='float', size_hint_y=None, height=40)
        layout.add_widget(self.amount_input)

        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        submit_button = Button(text='Submit', on_press=self.submit_entry)
        cancel_button = Button(text='Cancel', on_press=self.dismiss)
        button_layout.add_widget(submit_button)
        button_layout.add_widget(cancel_button)

        main_layout = BoxLayout(orientation='vertical', spacing=10)
        main_layout.add_widget(layout)
        main_layout.add_widget(button_layout)

        self.content = main_layout

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
            self.on_submit()  # Call update function without arguments
            self.dismiss()

    def cancel_entry(self, instance):
        self.dismiss()


# Popup class to view all entries
class ViewEntriesPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "All Entries"
        self.size_hint = (0.8, 0.8)

        scroll_view = ScrollView()
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Add entries from the DataFrame to the layout
        for index, row in df.iterrows():
            entry_label = Label(
                text=f"ID: {row['EntryID']} | Kategorie: {row['Kategorie']} | Label: {row['Label']} | Betrag: {row['Betrag']} | Timestamp: {row['Timestamp']}",
                size_hint_y=None,
                height=40
            )
            layout.add_widget(entry_label)

        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)


# Main application class
class BudgetApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.top_layout = BoxLayout(orientation='vertical', size_hint_y=0.2)

        self.total_spending_label = Label(text="Total Spending: $0")
        self.budget_counter_label = Label(text="Budget Counter: 0")

        self.top_layout.add_widget(self.total_spending_label)
        self.top_layout.add_widget(self.budget_counter_label)

        self.pie_chart_image = Image(size_hint_y=0.6)
        self.pie_chart_image.bind(size=self.on_resize)

        self.bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)

        categories = ["Rent", "Groceries", "Transport", "Health", "Entertainment"]

        for i, category in enumerate(categories, start=1):
            button = Button(text=f"{category}")
            button.bind(on_press=lambda instance, cat=category: self.show_entry_popup(cat))
            self.bottom_layout.add_widget(button)

        main_layout.add_widget(self.top_layout)
        main_layout.add_widget(self.pie_chart_image)
        main_layout.add_widget(self.bottom_layout)

        self.update_totals_and_counters()
        return main_layout

    def on_resize(self, *args):
        """Handles window resizing and updates the pie chart size."""
        # Calculate new size of the pie chart image
        width, height = self.pie_chart_image.size

        # Ensure height adjustment maintains aspect ratio or fits within limits
        if width > 0 and height > 0:
            self.pie_chart_image.height = height
            self.update_pie_chart(width, height)

    def show_entries_popup(self, instance):
        """Displays all entries in a popup."""
        popup = ViewEntriesPopup()
        popup.open()

    def show_entry_popup(self, category):
        """Displays a popup to add a new entry for the selected category."""
        popup = EntryPopup(category, self.update_totals_and_counters)
        popup.open()

    def update_totals_and_counters(self):
        """Updates the total spending and budget counter labels."""
        total_spending = df['Betrag'].sum()
        daily_budget = 25  # Example daily budget
        days_in_month = datetime.now().day
        expected_spending = daily_budget * days_in_month
        budget_counter = (expected_spending - total_spending) / daily_budget

        # Update label text
        self.total_spending_label.text = f"Total Spending: ${total_spending:.2f}"
        self.budget_counter_label.text = f"Budget Counter: {budget_counter:.2f}"

        # Update pie chart
        self.update_pie_chart(self.pie_chart_image.width, self.pie_chart_image.height)

    def update_pie_chart(self, width, height):
        """Generates and updates the pie chart image dynamically."""
        pie_chart_buf = generate_pie_chart(width, height)
        img = CoreImage(pie_chart_buf, ext='png')
        self.pie_chart_image.texture = img.texture




if __name__ == '__main__':
    load_data_from_json()
    BudgetApp().run()

