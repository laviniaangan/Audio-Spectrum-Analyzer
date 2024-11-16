import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pygame
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox


# Funcții principale
def load_audio(file_path):
    try:
        audio, sr = librosa.load(file_path, sr=None)
        print(f"Fișier încărcat: {file_path}")
        print(f"Rata de eșantionare: {sr} Hz")
        return audio, sr
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la încărcarea fișierului: {e}")
        return None, None


def generate_spectrogram(audio, sr):
    try:
        spectrogram = librosa.stft(audio)
        spectrogram_db = librosa.amplitude_to_db(np.abs(spectrogram), ref=np.max)
        return spectrogram_db
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la generarea spectrogramei: {e}")
        return None


def plot_spectrogram(spectrogram_db, sr, title="Spectrograma Audio", save_path=None):
    try:
        plt.figure(figsize=(10, 6))
        librosa.display.specshow(
            spectrogram_db,
            sr=sr,
            x_axis='time',
            y_axis='log',
            cmap='magma'
        )
        plt.colorbar(format="%+2.0f dB")
        plt.title(title)
        plt.xlabel("Timp (s)")
        plt.ylabel("Frecvență (Hz)")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            messagebox.showinfo("Succes", f"Spectrograma a fost salvată la: {save_path}")
        else:
            plt.show()
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la afișarea/salvarea spectrogramei: {e}")


# Funcții pentru interfață
def select_file():
    global audio_path
    audio_path = filedialog.askopenfilename(
        title="Selectează un fișier audio",
        filetypes=(("Fișiere audio", "*.wav *.mp3"), ("Toate fișierele", "*.*"))
    )
    if audio_path:
        file_label.config(text=f"Fișier selectat: {audio_path}")
        process_file(audio_path)


def process_file(file_path):
    global audio, sr, spectrogram_db
    audio, sr = load_audio(file_path)
    if audio is not None:
        spectrogram_db = generate_spectrogram(audio, sr)
        messagebox.showinfo("Succes", "Fișierul a fost procesat cu succes!")


def show_spectrogram():
    if spectrogram_db is not None and sr is not None:
        plot_spectrogram(spectrogram_db, sr)
    else:
        messagebox.showwarning("Atenție", "Nu există o spectrogramă de afișat. Încarcă mai întâi un fișier.")


def save_spectrogram():
    if spectrogram_db is not None and sr is not None:
        save_path = filedialog.asksaveasfilename(
            title="Salvează spectrograma",
            defaultextension=".png",
            filetypes=(("Fișiere imagine", "*.png"), ("Toate fișierele", "*.*"))
        )
        if save_path:
            plot_spectrogram(spectrogram_db, sr, save_path=save_path)
    else:
        messagebox.showwarning("Atenție", "Nu există o spectrogramă de salvat. Încarcă mai întâi un fișier.")


def play_audio():
    if audio_path:
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            messagebox.showinfo("Info", "Redarea audio a început!")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la redarea audio: {e}")
    else:
        messagebox.showwarning("Atenție", "Niciun fișier selectat pentru redare.")


def stop_audio():
    try:
        pygame.mixer.music.stop()
        messagebox.showinfo("Info", "Redarea audio s-a oprit!")
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la oprirea audio: {e}")


# Interfață grafică cu ttkbootstrap
root = ttk.Window(themename="darkly")
root.title("Analizator de Spectru Audio")
root.geometry("600x400")

# Variabile globale
audio = None
sr = None
spectrogram_db = None
audio_path = None

# Elemente UI
title_label = ttk.Label(root, text="Analizator de Spectru Audio", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

file_label = ttk.Label(root, text="Niciun fișier selectat", font=("Arial", 10), wraplength=500)
file_label.pack(pady=5)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

select_button = ttk.Button(button_frame, text="Selectează fișier audio", command=select_file)
select_button.grid(row=0, column=0, padx=10)

show_button = ttk.Button(button_frame, text="Afișează spectrograma", command=show_spectrogram)
show_button.grid(row=0, column=1, padx=10)

save_button = ttk.Button(button_frame, text="Salvează spectrograma", command=save_spectrogram)
save_button.grid(row=0, column=2, padx=10)

play_button = ttk.Button(button_frame, text="Redă audio", command=play_audio)
play_button.grid(row=1, column=0, padx=10, pady=5)

stop_button = ttk.Button(button_frame, text="Oprește audio", command=stop_audio)
stop_button.grid(row=1, column=1, padx=10, pady=5)

exit_button = ttk.Button(button_frame, text="Ieșire", command=root.quit)
exit_button.grid(row=1, column=2, padx=10, pady=5)

# Pornire aplicație
root.mainloop()
