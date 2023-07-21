import os
import threading
import time
import tkinter as tk
import tkinter.messagebox
import urllib.request
from tkinter import ttk

import pyautogui
import screeninfo
from dotenv import load_dotenv, set_key
from pynput import keyboard


def startup_checks():
    if not os.path.exists("ForgivePrompt.png"):  # Automatically Generate Forgive Prompt Image
        tkinter.messagebox.showinfo(title="Missing File Warning",
                                    message="It appears that the image file needed for this to work is not present. "
                                            "It will be created now.")
        req = urllib.request.Request("https://cdn.discordapp.com/attachments/1132078977436090378/1132079030275940432"
                                     "/ForgivePrompt.png", headers={'User-Agent': 'Mozilla/5.0'})
        with open("ForgivePrompt.png", "wb") as f:
            with urllib.request.urlopen(req) as r:
                f.write(r.read())
        f.close()

    if not os.path.exists("MAFSettings.env"):  # Automatically Generate the file containing the settings
        tkinter.messagebox.showinfo(title="Missing File Warning",
                                    message="It appears that the Settings file needed for this to work is not "
                                            "present. It will be created now.")
        set_key("MAFSettings.env", "FORGIVE_KEY", "PAGEUP")
        set_key("MAFSettings.env", "SHUTDOWN_KEY", "F5")
        set_key("MAFSettings.env", "MINIMIZE_WINDOW", "False")


def start_application():
    start_button.place_forget()  # Hide the "Start" button
    quit_button.grid(row=6, column=0, columnspan=2)  # Show the "Manually Quit" button on top of the "Start" button
    program_status_label.config(text="Program Status: Running")

    set_key("MAFSettings.env", "FORGIVE_KEY", forgive_key_choice.get())
    set_key("MAFSettings.env", "SHUTDOWN_KEY", shutdown_key_choice.get())
    set_key("MAFSettings.env", "MINIMIZE_WINDOW", minimize_window_choice.get())

    if minimize_window_choice.get() == "true":
        root.iconify()

    threading.Thread(target=key_press_checker).start()  # Start the key press checker
    threading.Thread(target=background_function).start()  # Start the background function


def on_key_press(key):
    shutdown_key = shutdown_key_choice.get()

    shutdown_key_string = str(key)
    conversion_fkeys = "Key." + shutdown_key.lower()

    # Check if the selected key matches the key value
    # this is the only way I could figure out how to make F keys work
    # Will need to remake at some point
    try:
        if key.char.lower() == shutdown_key.lower():
            close_program()
    except AttributeError:
        if shutdown_key_string == conversion_fkeys:
            close_program()  # Quit program


def key_press_checker():
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()


def background_function():
    forgive_key = forgive_key_choice.get()
    base_width, base_height = 1920, 1080

    print("adjusting box based on resolution")

    screen = screeninfo.get_monitors()[0]  # Assuming the first monitor
    screen_width = screen.width
    screen_height = screen.height

    scale_width = screen_width / base_width
    scale_height = screen_height / base_height

    search_area_width = int(scale_width * 360)
    search_area_height = int(scale_width * 360)
    search_area_left = int(scale_width * 1560)
    search_area_top = int(scale_height * 180)

    print(f"Final Calculation\n"
          f"search_area_left: {search_area_left}\n"
          f"search_area_top: {search_area_top}\n"
          f"search_area_width: {search_area_width}\n"
          f"search_area_height: {search_area_height}\n")

    team_kill_count = 0

    while True:
        while pyautogui.locateCenterOnScreen('ForgivePrompt.png',
                                             confidence=0.7,
                                             region=(search_area_left,
                                                     search_area_top,
                                                     search_area_width,
                                                     search_area_height)) is not None:  # finds "forgive"

            pyautogui.press(forgive_key)
            print("HID THE MENU")

            team_kill_count = team_kill_count + 1
            tk_count_label.config(text=f"Team Kills This Session: {team_kill_count}")

            time.sleep(1)  # hardcoded sleep!!!!!!!!!!!!! (prevents spamming the key)


def close_program():
    os.kill(os.getpid(), 9)  # Quits program


# -----------------------------------------------------------------------------------------

startup_checks()

load_dotenv("MAFSettings.env")
forgive_key_setting = os.getenv("FORGIVE_KEY")
shutdown_key_setting = os.getenv("SHUTDOWN_KEY")
minimize_window_setting = os.getenv("MINIMIZE_WINDOW")

char_list = ['PAGEUP', 'PAGEDOWN', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
             'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
             'F10']  # Full list of keys, page up as default

# Start of GUI code
root = tk.Tk()
root.title("Mordhau-Auto-Forgiver")
root.geometry("350x200")
root.resizable(False, False)

top_label = tk.Label(root, text="MAF - by cbass", font=("Arial", 14))
top_label.grid(row=0, column=0, columnspan=3, pady=10, padx=115)

forgive_key_label = tk.Label(root, text="Forgive Key:")
forgive_key_label.grid(row=1, column=0, pady=5)

# Populate the forgive_key_choice combobox with all the keys
forgive_key_choice = ttk.Combobox(root, values=char_list, state="readonly")
forgive_key_choice.current(char_list.index(forgive_key_setting))
forgive_key_choice.grid(row=1, column=1, pady=5)

shutdown_key_label = tk.Label(root, text="Shutdown Key:")
shutdown_key_label.grid(row=2, column=0, pady=5)

shutdown_key_choice = ttk.Combobox(root, values=char_list, state="readonly")
shutdown_key_choice.current(char_list.index(shutdown_key_setting))
shutdown_key_choice.grid(row=2, column=1)

minimize_window_label = tk.Label(root, text="Minimize Window After Start?")
minimize_window_label.grid(row=3, column=0)

minimize_window_choice = tk.StringVar()
minimize_window_choice.set(minimize_window_setting)
minimize_window_choice_box = ttk.Checkbutton(root, variable=minimize_window_choice, onvalue="true", offvalue="false")
minimize_window_choice_box.grid(row=3, column=1)

program_status_label = tk.Label(root, text="Program Status: Ready!")
program_status_label.grid(row=7, column=0, pady=13, sticky="w")

tk_count_label = tk.Label(root, text="Team Kills This Session: 0")
tk_count_label.grid(row=7, column=1, pady=13, sticky="e")

start_button = tk.Button(root, text="Start", command=start_application)
start_button.grid(row=6, column=0, columnspan=2, pady=5)

quit_button = tk.Button(root, text="Manually Quit", command=close_program)

root.protocol("WM_DELETE_WINDOW", close_program)  # Bind the window close event to close the processes

root.mainloop()
