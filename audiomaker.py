import sys
import os
import math
import tempfile

from pydub import AudioSegment
import soundfile as sf
from pedalboard import Pedalboard, Reverb


# ============================================================
# 8D AUDIO PROCESSOR by SecurityBong
# ============================================================
#
# Modes:
#
# 1 = 8D + Reverb
# 2 = 8D + Slow + Reverb
#
# The 8D movement is deliberately conservative:
# - smooth left/right movement
# - no experimental elevation filtering
# - no aggressive EQ
# - original audio is never modified
#
# ============================================================


# -----------------------------
# 8D SETTINGS
# -----------------------------

# Time for one complete LEFT -> RIGHT -> LEFT cycle.
# Lower = faster movement.
# Higher = slower movement.
PAN_CYCLE_MS = 20000

# Maximum stereo position.
# 1.0 = full left/right.
# 0.85 is slightly less aggressive.
PAN_AMOUNT = 0.90

# Number of overlapping processing windows.
# Higher values create smoother movement.
PAN_WINDOW_MS = 40

# Small smoothing factor to avoid abrupt transitions.
SMOOTHING = 0.85


# -----------------------------
# SLOW SETTINGS
# -----------------------------

SLOW_SPEED = 0.92


# -----------------------------
# REVERB SETTINGS
# -----------------------------

REVERB_ROOM_SIZE = 0.80
REVERB_DAMPING = 1.0
REVERB_WIDTH = 0.50
REVERB_WET = 0.30
REVERB_DRY = 0.80


# ============================================================
# LOAD AUDIO
# ============================================================

def load_audio(input_file):

    if not os.path.isfile(input_file):
        raise FileNotFoundError(
            f"Source music file not found:\n{input_file}"
        )

    extension = os.path.splitext(input_file)[1].lower()

    if extension == ".mp3":
        return AudioSegment.from_mp3(input_file)

    if extension == ".wav":
        return AudioSegment.from_wav(input_file)

    raise ValueError(
        "Unsupported audio format.\n"
        "Supported formats: MP3 and WAV"
    )


# ============================================================
# SMOOTH PAN CURVE
# ============================================================

def smooth_pan_position(progress):
    """
    Generates a smooth LEFT -> RIGHT -> LEFT movement.

    progress:
        0.0 -> beginning
        0.5 -> opposite side
        1.0 -> beginning again

    A sine curve is used so the movement naturally slows
    near the edges and moves smoothly through the center.
    """

    return math.sin(
        progress * 2.0 * math.pi
    ) * PAN_AMOUNT


# ============================================================
# 8D EFFECT
# ============================================================

def apply_8d(audio):
    """
    Apply a smooth horizontal 8D effect.

    Instead of jumping between fixed pan positions, the pan
    position changes continuously across the song.

    The audio is processed in short windows and each window
    receives a slightly different pan position.
    """

    if audio.channels == 1:
        audio = audio.set_channels(2)

    duration = len(audio)

    if duration <= 0:
        return audio

    result = AudioSegment.empty()

    previous_pan = 0.0

    for start in range(
        0,
        duration,
        PAN_WINDOW_MS
    ):

        end = min(
            start + PAN_WINDOW_MS,
            duration
        )

        piece = audio[start:end]

        # Position in the complete song
        progress = start / duration

        # Smooth cyclic pan
        target_pan = smooth_pan_position(
            progress * (duration / PAN_CYCLE_MS)
        )

        # Additional smoothing
        current_pan = (
            previous_pan * SMOOTHING
            + target_pan * (1.0 - SMOOTHING)
        )

        previous_pan = current_pan

        # Pydub pan expects -1.0 to +1.0
        piece = piece.pan(current_pan)

        result += piece

    return result


# ============================================================
# SLOW EFFECT
# ============================================================

def apply_slow(audio):
    """
    Slow the audio without changing the final sample rate.

    0.92 = 92% playback speed.
    """

    slowed = audio._spawn(
        audio.raw_data,
        overrides={
            "frame_rate": int(
                audio.frame_rate * SLOW_SPEED
            )
        }
    )

    slowed = slowed.set_frame_rate(
        audio.frame_rate
    )

    return slowed


# ============================================================
# REVERB
# ============================================================

def apply_reverb(audio):
    """
    Apply Pedalboard reverb using the same general
    characteristics as the original project.
    """

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as temp_file:

        temp_wav = temp_file.name

    try:

        # Pydub -> WAV
        audio.export(
            temp_wav,
            format="wav"
        )

        # WAV -> numpy array
        samples, sample_rate = sf.read(
            temp_wav
        )

        # Original project's reverb characteristics
        board = Pedalboard(
            [
                Reverb(
                    room_size=REVERB_ROOM_SIZE,
                    damping=REVERB_DAMPING,
                    width=REVERB_WIDTH,
                    wet_level=REVERB_WET,
                    dry_level=REVERB_DRY
                )
            ]
        )

        processed = board(
            samples,
            sample_rate=sample_rate
        )

        return processed, sample_rate

    finally:

        if os.path.exists(temp_wav):
            os.remove(temp_wav)


# ============================================================
# SAVE AUDIO
# ============================================================

def save_audio(
    samples,
    sample_rate,
    output_file
):

    wav_file = output_file + ".wav"
    mp3_file = output_file + ".mp3"

    try:

        # Make sure mono/stereo arrays have correct shape
        if len(samples.shape) == 1:
            channels = 1
        else:
            channels = samples.shape[1]

        # Save temporary WAV
        with sf.SoundFile(
            wav_file,
            "w",
            samplerate=sample_rate,
            channels=channels
        ) as file:

            file.write(samples)

        # WAV -> MP3
        AudioSegment.from_wav(
            wav_file
        ).export(
            mp3_file,
            format="mp3"
        )

    finally:

        if os.path.exists(wav_file):
            os.remove(wav_file)


# ============================================================
# MODE SELECTION
# ============================================================

def choose_mode():

    print()
    print("========================================")
    print("          SELECT PROCESSING MODE")
    print("========================================")
    print()
    print("1. 8D + Reverb")
    print("   Recommended for love / romantic / chill songs")
    print()
    print("2. 8D + Slow + Reverb")
    print("   Recommended for sad / emotional songs")
    print()
    print("========================================")
    print()

    while True:

        choice = input(
            "Enter choice [1-2]: "
        ).strip()

        if choice in ("1", "2"):
            return choice

        print()
        print("Please enter 1 or 2.")
        print()


# ============================================================
# MAIN
# ============================================================

def main():

    if len(sys.argv) < 2:

        print()
        print("========================================")
        print("  8D AUDIO PROCESSOR by SecurityBong")
        print("========================================")
        print()
        print("Usage:")
        print()
        print('python main.py "song.mp3"')
        print()
        print("Example:")
        print()
        print('python main.py "Tera Mera.mp3"')
        print()

        sys.exit(1)

    # Input file
    input_file = os.path.abspath(
        sys.argv[1]
    )

    if not os.path.isfile(input_file):

        print()
        print("ERROR: File not found!")
        print()
        print(input_file)
        print()

        sys.exit(1)

    # Select mode
    mode = choose_mode()

    # File information
    directory = os.path.dirname(
        input_file
    )

    filename = os.path.basename(
        input_file
    )

    name = os.path.splitext(
        filename
    )[0]

    # Output filename
    if mode == "1":

        output_name = (
            name
            + "_8D_Reverb"
        )

    else:

        output_name = (
            name
            + "_8D_Slow_Reverb"
        )

    output_file = os.path.join(
        directory,
        output_name
    )

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    print()
    print("========================================")
    print("  8D AUDIO PROCESSOR by SecurityBong")
    print("========================================")
    print()

    print("Input:")
    print(input_file)

    print()

    if mode == "1":

        print("Mode:")
        print("8D + Reverb")

    else:

        print("Mode:")
        print("8D + Slow + Reverb")

    print()

    print("Output:")
    print(output_file + ".mp3")

    print()
    print("========================================")
    print()

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    print("[1/4] Loading audio...")

    audio = load_audio(
        input_file
    )

    print(
        f"      Duration: {len(audio) / 1000:.1f} seconds"
    )

    print(
        f"      Channels: {audio.channels}"
    )

    # --------------------------------------------------------
    # 8D
    # --------------------------------------------------------

    print()
    print("[2/4] Applying smooth 8D movement...")

    audio_8d = apply_8d(
        audio
    )

    # --------------------------------------------------------
    # Optional slow
    # --------------------------------------------------------

    if mode == "2":

        print()
        print(
            "[3/4] Applying slow processing "
            f"({SLOW_SPEED}x)..."
        )

        audio_processed = apply_slow(
            audio_8d
        )

    else:

        print()
        print(
            "[3/4] Slow processing skipped."
        )

        audio_processed = audio_8d

    # --------------------------------------------------------
    # Reverb
    # --------------------------------------------------------

    print()
    print("[4/4] Applying reverb...")

    final_audio, sample_rate = apply_reverb(
        audio_processed
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    print()
    print("Saving MP3...")

    save_audio(
        final_audio,
        sample_rate,
        output_file
    )

    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    print()
    print("========================================")
    print("              SUCCESS")
    print("========================================")
    print()

    print(
        "Created:"
    )

    print(
        output_file + ".mp3"
    )

    print()


if __name__ == "__main__":
    main()

