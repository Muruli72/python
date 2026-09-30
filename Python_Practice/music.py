import tkinter as tk
from tkinter import filedialog
import pygame
import os
import random

pygame.mixer.init()

playlist = []
current_index = 0
repeat_mode = False

# Load saved playlist
def load_playlist():
    if os.path.exists("songs.txt"):
        with open("songs.txt", "r") as f:
            for line in f:
                song = line.strip()
                playlist.append(song)
                listbox.insert(tk.END, os.path.basename(song))

# Save playlist
def save_playlist():
    with open("songs.txt", "w") as f:
        for song in playlist:
            f.write(song + "\n")

# Add song
def add_song():
    songs = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
    for song in songs:
        playlist.append(song)
        listbox.insert(tk.END, os.path.basename(song))
    save_playlist()

# Play selected song
def play_song():
    global current_index
    if not playlist:
        return
    current_index = listbox.curselection()[0]
    song = playlist[current_index]
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    label.config(text="Playing: " + os.path.basename(song))

# Pause
def pause_song():
    pygame.mixer.music.pause()

# Resume
def resume_song():
    pygame.mixer.music.unpause()

# Next song
def next_song():
    global current_index
    if repeat_mode:
        play_song()
        return

    current_index += 1
    if current_index >= len(playlist):
        current_index = 0

    listbox.selection_clear(0, tk.END)
    listbox.selection_set(current_index)
    play_song()

# Previous song
def prev_song():
    global current_index
    current_index -= 1
    if current_index < 0:
        current_index = len(playlist) - 1

    listbox.selection_clear(0, tk.END)
    listbox.selection_set(current_index)
    play_song()

# Shuffle
def shuffle_song():
    global current_index
    if not playlist:
        return

    current_index = random.randint(0, len(playlist) - 1)
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(current_index)
    play_song()

# Toggle repeat
def toggle_repeat():
    global repeat_mode
    repeat_mode = not repeat_mode
    status = "ON" if repeat_mode else "OFF"
    label.config(text="Repeat Mode: " + status)

# GUI
root = tk.Tk()
root.title("🎵 MelodyFlow Music Player")
root.geometry("400x500")

label = tk.Label(root, text="Welcome to Music Player", font=("Arial", 12))
label.pack(pady=10)

listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(pady=10)

btn_add = tk.Button(root, text="Add Songs", command=add_song)
btn_add.pack()

btn_play = tk.Button(root, text="Play", command=play_song)
btn_play.pack()

btn_pause = tk.Button(root, text="Pause", command=pause_song)
btn_pause.pack()

btn_resume = tk.Button(root, text="Resume", command=resume_song)
btn_resume.pack()

btn_next = tk.Button(root, text="Next", command=next_song)
btn_next.pack()

btn_prev = tk.Button(root, text="Previous", command=prev_song)
btn_prev.pack()

btn_shuffle = tk.Button(root, text="Shuffle", command=shuffle_song)
btn_shuffle.pack()

btn_repeat = tk.Button(root, text="Toggle Repeat", command=toggle_repeat)
btn_repeat.pack()

# Load saved songs
load_playlist()

root.mainloop()