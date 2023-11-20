#!/usr/bin/env python
# coding: utf-8

# # Credit Card Router for the Best PSP 

# In[ ]:


import os
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk

# Load the dataset from my local machine (data set given by IU)
data = pd.read_excel("C:/Users/neuroot.cmi/PSP_Jan_Feb_2019.xlsx")

# Create a tkinter GUI fo my dimensions
root = tk.Tk()
root.geometry("600x500")
root.title("PSP Selector")

# Load the logo image (IU LOGO)
logo_path = "C:/Users/neuroot.cmi/iu_logo.png"  
logo = Image.open(logo_path)
logo = logo.resize((200, 200), Image.ANTIALIAS)
logo_image = ImageTk.PhotoImage(logo)

# Display the logo
logo_label = tk.Label(root, image=logo_image)
logo_label.image = logo_image 
logo_label.pack()

# Function to get the input and process it
def get_input():
    try:
        selected_country = country_var.get()
        selected_card_type = card_var.get()
        user_amount = float(amount_input.get())
        user_3d_secure = int(secure_input.get())

        country_filtered_data = data[(data['country'] == selected_country) &
                                     (data['amount'] == user_amount) &
                                     (data['3D_secured'] == user_3d_secure) &
                                     (data['card'] == selected_card_type)]

        if country_filtered_data.empty:
            result_label.config(text="No data found for the given input.", fg="red")
        else:
            psp_success_probabilities = {}
            for psp in country_filtered_data['PSP'].unique():
                psp_data = country_filtered_data[country_filtered_data['PSP'] == psp]
                success_count = psp_data['success'].sum()
                total_count = len(psp_data)
                success_probability = success_count / total_count if total_count != 0 else 0
                psp_success_probabilities[psp] = success_probability

            best_psp = min(psp_success_probabilities,
                           key=lambda x: (psp_success_probabilities[x], country_filtered_data[country_filtered_data['PSP'] == x]['amount'].min()))

            # Retrieve and display fees for the selected PSP
            selected_psp_data = data[(data['country'] == selected_country) & (data['PSP'] == best_psp)].iloc[0]
            success_fee = selected_psp_data['fee_successful']
            failed_fee = selected_psp_data['fee_failed']

            result_label.config(text=f"The suggested PSP for {selected_country} with the given criteria is {best_psp}. \n"
                                     f"The credit card router will be processed to {best_psp}. \n"
                                     f"Fee on successful transactions: {success_fee} Euro \n"
                                     f"Fee on failed transactions: {failed_fee} Euro", fg="green", font=("Arial", 14, "bold"))

    except ValueError:
        result_label.config(text="Entered wrong input. Please enter a valid input.", fg="red")

# Add fee columns to the dataset
data['fee_successful'] = data.apply(lambda row: {'Moneycard': 5, 'Goldcard': 10, 'UK_Card': 3, 'Simplecard': 1}[row['PSP']], axis=1)
data['fee_failed'] = data.apply(lambda row: {'Moneycard': 2, 'Goldcard': 5, 'UK_Card': 1, 'Simplecard': 0.5}[row['PSP']], axis=1)


# GUI elements
country_label = tk.Label(root, text="Select country:", font=("Arial", 12))
country_label.pack()

# Dropdown menu for selecting the country
country_var = tk.StringVar(root)
country_dropdown = tk.OptionMenu(root, country_var, *data['country'].unique())
country_dropdown.config(font=("Arial", 12))
country_dropdown.pack()

card_label = tk.Label(root, text="Select card type:", font=("Arial", 12))
card_label.pack()

# Dropdown menu for selecting the card type
card_var = tk.StringVar(root)
card_dropdown = tk.OptionMenu(root, card_var, *data['card'].unique())
card_dropdown.config(font=("Arial", 12))
card_dropdown.pack()

amount_label = tk.Label(root, text="Enter transaction amount:", font=("Arial", 12))
amount_label.pack()
amount_input = tk.Entry(root, font=("Arial", 12))
amount_input.pack()

secure_label = tk.Label(root, text="Enter 1 for enabled 3D secure, 0 for disabled:", font=("Arial", 12))
secure_label.pack()
secure_input = tk.Entry(root, font=("Arial", 12))
secure_input.pack()

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
result_label.pack()

# Submit button
button = tk.Button(root, text="Submit", command=get_input, font=("Arial", 12))
button.pack()

# Run the GUI
root.mainloop()



# In[5]:


data.columns


# # DATA VISUALIZATION

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create a directory to save the plots if it doesn't exist
output_directory = 'C:/Users/neuroot.cmi/GRAPHS'
os.makedirs(output_directory, exist_ok=True)

# 1. Time Series Analysis
plt.figure(figsize=(8, 4))
sns.lineplot(x='tmsp', y='success', data=data, ci=None)
plt.title('Time Series Analysis of Success/Failure')
plt.savefig(os.path.join(output_directory, 'time_series_analysis.png'))
plt.close()

# 2. Country Distribution
plt.figure(figsize=(6, 4))
sns.countplot(x='country', data=data)
plt.title('Distribution of Transactions Across Countries')
plt.xticks(rotation=45)
plt.savefig(os.path.join(output_directory, 'country_distribution.png'))
plt.close()

# 3. Success/Failure Distribution
plt.figure(figsize=(4, 4))
data['success'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribution of Successful and Failed Transactions')
plt.savefig(os.path.join(output_directory, 'success_failure_distribution.png'))
plt.close()

# 4. PSP Usage
plt.figure(figsize=(6, 4))
sns.countplot(x='PSP', data=data)
plt.title('Frequency of Usage for Each Payment Service Provider')
plt.xticks(rotation=45)
plt.savefig(os.path.join(output_directory, 'psp_usage.png'))
plt.close()

# 5. 3D Secure Usage
plt.figure(figsize=(4, 4))
data['3D_secured'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Usage of 3D Secure in Transactions')
plt.savefig(os.path.join(output_directory, '3d_secure_usage.png'))
plt.close()

# 6. Card Types
plt.figure(figsize=(6, 4))
sns.countplot(x='card', data=data)
plt.title('Distribution of Transactions Based on Card Types')
plt.savefig(os.path.join(output_directory, 'card_types.png'))
plt.close()

# 7. Fee Analysis
plt.figure(figsize=(8, 4))
sns.boxplot(x='success', y='fee_successful', data=data)
plt.title('Fee Distribution for Successful and Failed Transactions')
plt.savefig(os.path.join(output_directory, 'fee_analysis.png'))
plt.close()

# 8. Correlation Heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(data[['amount', 'fee_successful', 'fee_failed']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.savefig(os.path.join(output_directory, 'correlation_heatmap.png'))
plt.close()

# 9. Transaction Amount Distribution
plt.figure(figsize=(8, 4))
sns.histplot(data['amount'], bins=30, kde=True)
plt.title('Distribution of Transaction Amounts')
plt.savefig(os.path.join(output_directory, 'transaction_amount_distribution.png'))
plt.close()

# 10. Success/Failure Over Time
plt.figure(figsize=(8, 4))
sns.lineplot(x='tmsp', y='success', data=data, ci=None)
plt.title('Success/Failure Over Time')
plt.savefig(os.path.join(output_directory, 'success_failure_over_time.png'))
plt.close()


# In[4]:


data.head(5)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




