import customtkinter as ctk
import random
import os

# Function to split number sequence into parts
def split_number_sequence(number_sequence):
    split_numbers = set()
    
    # Split the number sequence into parts, focusing on 4-digit, 3-digit, etc.
    for i in range(1, len(number_sequence)):
        for j in range(i+1, len(number_sequence)+1):
            split_numbers.add(number_sequence[i-1:j])
    
    return list(split_numbers)

# Function to generate variations based on common patterns and custom numbers
def generate_wordlist(base_strings, custom_numbers):
    wordlist = set()

    # Handle custom number sequence splitting
    if custom_numbers:
        custom_number_parts = split_number_sequence(custom_numbers)
    else:
        custom_number_parts = []

    # Symbols to combine with base strings
    symbols = ['@', '#', '$', '%', '&', '!', ',', '.', '/', '*', '<', ">", "?"]

    # Process each base string
    for user_input in base_strings:
        user_input = user_input.strip()  # Remove leading/trailing spaces

        # Original string and basic variations
        wordlist.add(user_input)
        wordlist.add(user_input.upper())
        wordlist.add(user_input.lower())
        wordlist.add(user_input.capitalize())
        wordlist.add(user_input[::-1])  # Reverse string

        # Shuffle string
        shuffled = ''.join(random.sample(user_input, len(user_input)))
        wordlist.add(shuffled)

        # Combining custom number parts with the base string
        for number in custom_number_parts:
            wordlist.add(user_input + number)  # Example2021
            wordlist.add(f"{user_input}@{number}")  # Example@2021
            wordlist.add(f"{user_input}{number}@")  # Example2021@

            for sym in symbols:
                wordlist.add(f"{user_input}{sym}{number}")  # Example@2021
                wordlist.add(f"{sym}{user_input}{number}")  # @Example2021

        # Common number sequences
        numbers = ['123', '456', '789', '012345678', '101', '69', '987']
        numbers.extend(custom_number_parts)  # Add custom numbers to the list

        # Add combinations of numbers and symbols to the base string
        for number in numbers:
            wordlist.add(user_input + number)
            wordlist.add(number + user_input)
            wordlist.add(f"{user_input[:len(user_input)//2]}{number}{user_input[len(user_input)//2:]}")

            for sym1 in symbols:
                wordlist.add(f"{user_input}{sym1}{number}")  # Example@123
                wordlist.add(f"{user_input}{sym1}{sym1}{number}")  # Example@@123

        # Add symbol combinations like "Example@#", "Example,./"
        for sym1 in symbols:
            for sym2 in symbols:
                wordlist.add(f"{user_input}{sym1}{sym2}")  # Example@#
                wordlist.add(f"{user_input}{sym1}{sym2}{number}")  # Example@#123
                wordlist.add(f"{user_input}{sym1}{sym2},{sym2}{number}")  # Example@#,./123
        
        # Break up and recombine the string
        for i in range(1, len(user_input)):
            wordlist.add(f"{user_input[:i]}_{user_input[i:]}")
            wordlist.add(f"{user_input[:i]}-{user_input[i:]}")

    return list(wordlist)

# Function to save the wordlist to a file without overwriting
def save_wordlist_to_file(wordlist, filename="wordlist1.txt"):
    with open(filename, "a") as file:  # Append mode
        for word in wordlist:
            file.write(word + "\n")
    return filename

# Function to generate and display wordlist in the GUI
def generate_and_display():
    base_strings_input = entry.get("1.0", "end-1c")  # Get all base strings from Text widget
    custom_numbers = numbers_entry.get()

    # Process base strings (split by new lines or commas)
    base_strings = [s.strip() for s in base_strings_input.split('\n') if s.strip()]

    if base_strings:
        wordlist = generate_wordlist(base_strings, custom_numbers)
        save_file_path = save_wordlist_to_file(wordlist)

        result_text.set(f"Wordlist appended to {save_file_path}")
    else:
        result_text.set("Please enter one or more base strings!")

# Initialize CustomTkinter GUI
app = ctk.CTk()
app.title("Wordlist Generator")
app.geometry("400x600")

# Multi-line Entry widget for base string input
entry_label = ctk.CTkLabel(app, text="Enter base strings (one per line) Combination of Target Name:")
entry_label.pack(pady=10)

entry = ctk.CTkTextbox(app, width=300, height=100)  # Textbox for multiple strings
entry.pack(pady=5)

# Entry widget for custom number sequences input
numbers_label = ctk.CTkLabel(app, text="Enter custom number sequences (phone no, roll no, etc ):")
numbers_label.pack(pady=10)

numbers_entry = ctk.CTkEntry(app, width=300)
numbers_entry.pack(pady=5)

# Button to generate wordlist
generate_button = ctk.CTkButton(app, text="Generate Wordlist", command=generate_and_display)
generate_button.pack(pady=10)

# Label to display result or file path
result_text = ctk.StringVar()
result_label = ctk.CTkLabel(app, textvariable=result_text)
result_label.pack(pady=10)

# Run the application
app.mainloop()
