import numpy as np
import librosa
from scipy.signal import savgol_filter
from scipy.stats import linregress


def analyze_audio(file_path):

    # ===============================
    # 6️⃣ Smooth Tempo Curve
    # ===============================
    # Window must be odd and <= len(instant_tempo)
    window = min(7, len(instant_tempo) if len(instant_tempo) % 2 == 1 else len(instant_tempo)-1)

    if window >= 3:
        smoothed_tempo = savgol_filter(
            instant_tempo,
            window_length=window,
            polyorder=2
        )
    else:
        smoothed_tempo = instant_tempo

    # ===============================
    # 7️⃣ Loudness (RMS Energy)
    # ===============================
    rms = librosa.feature.rms(y=y)[0]
    rms_times = librosa.frames_to_time(
        np.arange(len(rms)),
        sr=sr
    )

    # ===============================
    # 8️⃣ Summary Dictionary
    # ===============================
    summary = {
        "mean_bpm": float(mean_bpm),
        "global_bpm_estimate": float(tempo_global),
        "tempo_std": float(tempo_std),
        "tempo_cv": float(tempo_cv),
        "tempo_range": float(tempo_range),
        "tempo_drift_slope": float(slope),
        "pause_count": pause_count
    }

    # final JSON-Ready Output
    return {
        "tempo_curve": smoothed_tempo.tolist(),
        "tempo_time": tempo_time[:len(smoothed_tempo)].tolist(),
        "loudness_curve": rms.tolist(),
        "loudness_time": rms_times.tolist(),
        "summary": summary
    }