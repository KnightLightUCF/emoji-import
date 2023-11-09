import tkinter as tk
from tkinter import ttk
from emoji_library import emojis
from PIL import ImageTk, Image, ImageDraw, ImageFont
import numpy as np
import cv2
from stl import mesh


emoji_buttons = []

def update_displayed_emojis(event=None):
    # Get the current text from the input field
    search_text = input_field.get().lower()

    # Clear the existing emoji buttons
    for button in emoji_buttons:
        button.destroy()
    emoji_buttons.clear()

    # Filter emojis based on user input
    matching_emojis = [(emoji_char, description) for emoji_char, description in emojis if search_text in description.lower()]

    # Create and display buttons for emojis matching input field
    for emoji_char, description in matching_emojis:
        emoji_button = tk.Button(text=emoji_char, command=lambda e=emoji_char: insert_emoji(e))
        emoji_button.place(x=250, y=200)
        emoji_button.pack(side=tk.LEFT, padx=0, pady=100)
        emoji_buttons.append(emoji_button)

def insert_emoji(emoji_char):
    # Insert the selected emoji into the input field while erasing text
    current_text = input_field.get()
    input_field.delete(0, tk.END)
    input_field.insert(0, current_text + emoji_char)
    input_field.delete(0, tk.END)
    input_field.insert(0, emoji_char)

# Matches unicode of emoji to .ttf file and draws the emoji associated wtih input unicode.
def draw_emoji():
    def emoji_format(emoji_text):

        emoji_size = 200
    # Set the font file that supports emoji font
        emoji_font = ImageFont.truetype('/Users/stevenholmes/OneDrive/Knight_Light 11.1.2023/emoji-import/emoji-import/NotoEmoji-VariableFont_wght.ttf', size=emoji_size)  # Adjust the font size as needed

        # emoji_width, emoji_height = emoji_font.getsize(emoji_text)

        width, height = 400, 400
        background_color = (255, 255, 255)
        image = Image.new('RGB', (width, height), background_color)

        draw = ImageDraw.Draw(image)

        # centers emoji (will update with calculation)
        x = 70
        y = 80

        # Set the text color (black) - plan to add color selection feature
        text_color = (0, 0, 0)
        width = int(.1)
        # Draw the emoji onto the image canvas
        draw.text((x, y), emoji_text, font=emoji_font, stroke_width=width, fill=text_color)

        # Save image as png output
        image.save('emoji_image.png')
        # Opens new png file for conversion
        image=Image.open('emoji_image.png')
        image = image.convert('L')
        image_array = np.array(image)
        
        # Detects edges within image to, the lower the threshold the sharper the image
        edges = cv2.Canny(image_array, threshold1=10, threshold2=10)

        vertices = []
        height = 0.0
        # Calculates vertices and creates a mesh from the x,y values.
        for y in range(edges.shape[0]):
            for x in range(edges.shape[1]):
                if edges[y,x]>0:
                    vertices.append((x,y,height))
        emoji_mesh = mesh.Mesh(np.zeros(len(vertices), dtype=mesh.Mesh.dtype))
                        
        for i, vertex in enumerate(vertices):
            emoji_mesh.vectors[i] = [vertex]
        # Saves stl file
        emoji_mesh.save('emoji.stl')

    emoji_text = input_field.get()
    emoji_format(emoji_text)
  


# Creates the GUI window
root = tk.Tk()
root.geometry("800x600")
root.title("Knight Light Drone Emojis")
root.iconbitmap('UCF_Logo.ico')

# Importing image for GUI
image_UCF = Image.open('/Users/stevenholmes/OneDrive/Knight_Light 11.1.2023/emoji-import/emoji-import/Knightlight_MD_1.png').resize((450,325))
image_tk = ImageTk.PhotoImage(image_UCF)
label = ttk.Label(root, text = "UCF Logo", image = image_tk)
label.pack()

# Create an input field for typing emoji names
input_field = tk.Entry(root)
input_field.pack()

# Define a list of emojis and their descriptions directly within the code
emojis

# Bind a callback function to the input field to update displayed emojis on text change
input_field.bind("<KeyRelease>", update_displayed_emojis)

# Creates a "Draw Emoji" button, when selected emoji is drawn and program closes
draw_button = tk.Button(root, text="Draw Emoji", command=lambda:[draw_emoji(), root.quit()])
draw_button.place(x=275, y=370)

# Creates the "Exit Program" button
button_quit = tk.Button(root, text="Exit Program", command=root.quit)
button_quit.place(x=400, y=370)

# Starts GUI main loop
root.mainloop()

#side=tk.RIGHT, padx=0, pady=0)
#side=tk.LEFT, padx=190
#side=tk.LEFT, padx=0
#frame1=tk.Frame(root,width=50,height=0,bg='#d9d9d9')
#frame1.place(x=370, y=300)
#frame1.pack(side=tk.LEFT)

