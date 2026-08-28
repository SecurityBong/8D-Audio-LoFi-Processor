# 🎧 8D Audio LoFi Processor

A simple Python-based audio processor that transforms your songs into immersive **8D audio** with **reverb**, with an optional **slow-down effect** for emotional and atmospheric tracks.

Built with a focus on keeping the processing simple, controlled, and easy to use.

---

## ✨ Features

* 🎧 Smooth 8D left-to-right audio movement
* 🌊 Reverb processing
* 🐌 Optional slow-down processing
* 🎵 Supports MP3 and WAV input
* 📁 Automatically generates output files
* 📝 No need to rename your songs
* 💻 Runs locally on Windows
* 🧩 Everything is contained in a single Python script
* 🎛️ Two processing modes for different music styles

---

## 🎶 Processing Modes

When you run the program, you can choose between two modes.

### 1. 8D + Reverb

Recommended for:

* ❤️ Love songs
* 💕 Romantic songs
* 🌙 Chill songs
* ✨ Dreamy / atmospheric songs

Processing chain:

```text
Original Song
     ↓
Smooth 8D Movement
     ↓
Reverb
     ↓
8D + Reverb
```

Example output:

```text
My Song_8D_Reverb.mp3
```

---

### 2. 8D + Slow + Reverb

Recommended for:

* 😔 Sad songs
* 💔 Breakup songs
* 🖤 Emotional songs
* 🌧️ Late-night / atmospheric songs

Processing chain:

```text
Original Song
     ↓
Smooth 8D Movement
     ↓
Slow Down (0.92x)
     ↓
Reverb
     ↓
8D + Slow + Reverb
```

Example output:

```text
My Song_8D_Slow_Reverb.mp3
```

---

# 🛠️ Requirements

* Windows
* Python 3.x
* FFmpeg
* Python virtual environment
* The following Python packages:

```text
pydub
soundfile
pedalboard
audioop-lts
```

---

# 📥 Installation

## 1. Clone the repository

```bash
git clone https://github.com/SecurityBong/8D-Audio-LoFi-Processor.git
cd 8D-Audio-LoFi-Processor
```

Or download the repository as a ZIP and extract it.

---

## 2. Make sure Python is installed

Check your Python installation:

```bash
python --version
```

---

## 3. Create the virtual environment

Create the virtual environment **once**:

```bash
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

After activation, you should see:

```text
(venv)
```

at the beginning of your terminal.

---

## 4. Install dependencies

Install the required packages:

```bash
pip install pydub soundfile pedalboard audioop-lts
```

### Why `audioop-lts`?

Recent Python versions removed the old built-in `audioop` module.

`pydub` requires audioop functionality, so `audioop-lts` provides compatibility for newer Python versions.

---

# 🎬 FFmpeg Installation

FFmpeg is required by Pydub for audio conversion.

Check whether FFmpeg is already installed:

```bash
ffmpeg -version
```

If FFmpeg is installed correctly, you should see information similar to:

```text
ffmpeg version ...
```

If Windows says:

```text
'ffmpeg' is not recognized...
```

install FFmpeg and add its `bin` directory to the Windows PATH.

For example:

```text
C:\ffmpeg\bin
```

After adding it to PATH, open a new terminal and run:

```bash
ffmpeg -version
```

again.

---

# 🚀 Usage

Activate the existing virtual environment:

```cmd
venv\Scripts\activate
```

Then run:

```cmd
python main.py "your-song.mp3"
```

The program will display:

```text
========================================
          SELECT PROCESSING MODE
========================================

1. 8D + Reverb
   Recommended for love / romantic / chill songs

2. 8D + Slow + Reverb
   Recommended for sad / emotional songs

========================================

Enter choice [1-2]:
```

Enter:

```text
1
```

or:

```text
2
```

depending on the desired result.

---

# 📁 Output

The original song is **never overwritten**.

The processed file is automatically created in the same directory as the original.

For example:

```text
Original:
random.mp3

Mode 1:
random_8D_Reverb.mp3

Mode 2:
random_8D_Slow_Reverb.mp3
```

Long filenames and filenames containing spaces, commas, brackets, etc. are supported.

Example:

```cmd
python main.py "random and more randomness as this just an example to understand.mp3"
```

---

# 🎛️ Current Processing Settings

The processor uses conservative settings intended to preserve the character of the original song.

### 8D

```text
Pan cycle: 20 seconds
Maximum pan: 90%
Smooth movement: enabled
```

### Slow mode

```text
Playback speed: 0.92x
```

### Reverb

```text
Room size: 0.80
Damping: 1.00
Width: 0.50
Wet level: 0.30
Dry level: 0.80
```

These values can be adjusted directly at the beginning of `main.py`.

---

# 🧠 Design Philosophy

This project intentionally avoids excessive audio processing.

The goal is not to stack as many effects as possible, but to create an enjoyable spatial effect while keeping the original song recognizable.

The 8D processing focuses primarily on:

* Smooth stereo movement
* Controlled panning
* Moderate spatial width
* Reverb
* Optional subtle slowdown

Experimental elevation filtering, aggressive EQ, and other potentially destructive processing are intentionally avoided.

---

# 🔄 Processing Flow

### Mode 1

```text
              ┌──────────────┐
              │ Original     │
              │ Audio        │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │ Smooth 8D    │
              │ Movement     │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │ Reverb       │
              └──────┬───────┘
                     ↓
          8D + Reverb MP3
```

### Mode 2

```text
              ┌──────────────┐
              │ Original     │
              │ Audio        │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │ Smooth 8D    │
              │ Movement     │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │ Slow 0.92x   │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │ Reverb       │
              └──────┬───────┘
                     ↓
       8D + Slow + Reverb MP3
```

---

# 📂 Project Structure

The project is intentionally kept simple:

```text
8D-Audio-Processor/
│
├── main.py
├── README.md
├── requirements.txt
└── venv/
```

The `venv` directory is a local Python environment and generally should **not** be committed to GitHub.

Add this to `.gitignore`:

```text
venv/
__pycache__/
*.pyc
```

---

# 📦 Recommended requirements.txt

Create a file named:

```text
requirements.txt
```

with:

```text
pydub
soundfile
pedalboard
audioop-lts
```

Then installation becomes:

```bash
pip install -r requirements.txt
```

---

# ⚠️ Notes

* Use headphones for the intended 8D experience.
* Processing time depends on the length and format of the song.
* MP3 conversion may involve a small amount of additional compression.
* The original input file is not modified.
* The processor works locally; your audio files do not need to be uploaded to a server.
* This project is intended for personal/legitimate audio processing.

---

# 🙏 Inspiration & References

This project was developed by studying different approaches to 8D audio processing and experimenting with how stereo movement, slowdown, and reverb can be combined.

Two repositories that were useful for understanding different approaches to 8D processing:

* `dashroshan/8d-slow-reverb`
* `maxgillham/8D-Audio`

This project does **not** aim to be a direct copy of either implementation. The processing approach has been independently adapted and simplified with an emphasis on controlled stereo movement and usability.

---

# 👨‍💻 Author

Created by **SecurityBong A.K.A Rahul**

🎧 Built for experimenting with immersive audio and creating different moods from music.

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

Suggestions, improvements, and constructive feedback are welcome.

```
```
