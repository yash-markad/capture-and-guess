import pyautogui
import easyocr
import openai
from pynput import mouse

# Set up API key for OpenAI
openai.api_key = "opeanai api"

# Initialize EasyOCR reader for English language
reader = easyocr.Reader(['en'])

# Define function to handle mouse clicks and take screenshot
def on_click(x, y, button, pressed):
    global clicks
    if pressed:
        print("pressed")
        clicks.append((x,y))
        if len(clicks) == 4:
            # Sort the clicks into top-left, top-right, bottom-left, bottom-right order
            clicks.sort()
            # Determine the leftmost and rightmost clicks
            left_click = clicks[0] if clicks[0][0] < clicks[1][0] else clicks[1]
            right_click = clicks[2] if clicks[2][0] > clicks[3][0] else clicks[3]
            # Determine the topmost and bottommost clicks
            top_click = clicks[0] if clicks[0][1] < clicks[2][1] else clicks[2]
            bottom_click = clicks[1] if clicks[1][1] > clicks[3][1] else clicks[3]
            # Calculate the coordinates of the rectangular window
            x_start = left_click[0]
            y_start = top_click[1]
            x_end = right_click[0]
            y_end = bottom_click[1]
            # Calculate the width and height of the screenshot region
            width = abs(x_end - x_start)
            height = abs(y_end - y_start)
            if width > 0 and height > 0:
                # Take the screenshot
                screenshot = pyautogui.screenshot(region=(x_start, y_start, width, height))
                screenshot.save('screenshot.png')
                print("Screenshot saved as screenshot.png")
                # Perform image-to-text conversion on the screenshot
                result = reader.readtext('screenshot.png', detail=0)
                formatted_text = ' '.join(result)
                print("Text extracted from image:", formatted_text)
                # Search for a prompt using OpenAI's API
                prompt = formatted_text
                completions = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.7)
                message = completions.choices[0].text.strip()
                print("Answer:", message)
            else:
                print("Error: Screenshot region has invalid dimensions.")
            # Reset the clicks list
            clicks = []

# Initialize the clicks list
clicks = []

# Create a mouse listener
with mouse.Listener(on_click=on_click) as listener:
    print("Please select the window to capture.")
    listener.join()
