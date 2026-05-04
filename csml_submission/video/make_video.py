#!/usr/bin/env python3
"""Build the CSML presentation video from presentation.pdf and TTS narration."""

from __future__ import annotations

import asyncio
import json
import math
import re
import shlex
import subprocess
from pathlib import Path

import edge_tts
import fitz


ROOT = Path(__file__).resolve().parent
PDF = ROOT / "presentation.pdf"
BUILD = ROOT / "build_video"
OUT = ROOT / "presentation_video.mp4"
SRT = ROOT / "presentation_subtitles.srt"
SCRIPT = ROOT / "presentation_script.txt"
VOICE = "en-US-GuyNeural"
RATE = "+0%"


SLIDES = [
    {
        "title": "Title",
        "text": (
            "This presentation describes polynomial input preconditioning for "
            "zero-shot time-series forecasting."
        ),
    },
    {
        "title": "USP Preliminaries",
        "text": (
            "The key preliminary is Universal Sequence Preconditioning, proposed "
            "by Marsden and Hazan for online prediction in marginally stable "
            "linear dynamical systems. Their insight is that instead of asking "
            "a learner to infer a potentially large hidden state directly, one "
            "can first transform the observed sequence with a fixed polynomial "
            "convolution. Chebyshev-style coefficients are useful because they "
            "uniformly damp the difficult modes of the hidden dynamics across "
            "a broad spectral range. The intuition for this project is to use "
            "that same fixed, theory-guided signal as information given to a "
            "patch-based transformer before tokenization."
        ),
    },
    {
        "title": "Problem",
        "text": (
            "The starting point is a common design in modern time-series foundation "
            "models like Moirai 2.0. These models split the input sequence into "
            "fixed-length patches, embed each patch independently, and then run a "
            "transformer over the resulting tokens. This is efficient, but it creates "
            "a bottleneck: before attention, each token only sees its own local patch. "
            "If important structure spans multiple patches, the transformer has to "
            "discover that structure later."
        ),
    },
    {
        "title": "Method",
        "text": (
            "My idea is to expose a small amount of cross-patch information before "
            "tokenization. I use a fixed polynomial convolution motivated by Universal "
            "Sequence Preconditioning. In the default setting, the residual channel is "
            "r sub t equals negative x sub t minus thirty two, plus one eighth times "
            "x sub t minus sixty four. This is computed from the normalized input "
            "series, split into patches, and concatenated alongside the raw input "
            "patch and observation mask. The only architectural change is that the "
            "first projection layer gets wider, from two patch channels to three. "
            "The transformer decoder, output head, and forecast target are unchanged. "
            "The overhead is only twelve thousand parameters, or about zero point "
            "one one percent of Moirai 2.0 Small."
        ),
    },
    {
        "title": "Architecture",
        "text": (
            "This diagram shows the full architectural change. The orange boxes are "
            "the new parts: compute the Chebyshev residual, optionally apply hint "
            "dropout during training, concatenate the raw input, mask, and residual, "
            "and widen the input projection. Everything inside the Moirai 2.0 decoder "
            "block and the autoregressive quantile output head stays the same."
        ),
    },
    {
        "title": "Main Result",
        "text": (
            "The main result is on GIFT-Eval, which has ninety-seven dataset-by-horizon "
            "forecasting configurations. Across five seeds, the preconditioned model "
            "improves geometric-mean normalized MASE by two point nine percent over "
            "the Moirai 2.0 Small baseline. After averaging each configuration across "
            "seeds, it wins seventy-two of ninety-seven configurations, with a paired "
            "sign-test p-value below ten to the minus five. The important control is "
            "capacity matching. I trained the same widened architecture with a zero "
            "third channel and with a duplicate of the input as the third channel. "
            "Those controls do not reproduce the gain, so the improvement comes from "
            "the polynomial content of the channel."
        ),
    },
    {
        "title": "Ablations and External Validation",
        "text": (
            "I also tested whether the result transfers beyond GIFT-Eval. On FEV-Bench, "
            "an independent benchmark with one hundred forecasting tasks, the same "
            "method improves MASE by two point nine percent and scaled quantile loss "
            "by three point one percent. In ablations, every tested Chebyshev degree "
            "from two through seven improves over baseline. Fixed Chebyshev coefficients "
            "also outperform learned coefficient vectors initialized either from "
            "Chebyshev coefficients or from zero."
        ),
    },
    {
        "title": "Training Dynamics",
        "text": (
            "Finally, the effect grows with training. At one hundred thousand steps, "
            "the MASE improvement reaches three point nine percent, and the "
            "preconditioned model has lower cross-seed variance than the baseline. "
            "The gains are also largest on longer-horizon forecasting tasks, where "
            "the dropout version is more robust during autoregressive decoding."
        ),
    },
    {
        "title": "Takeaways",
        "text": (
            "The takeaway is that foundation-model performance does not only come "
            "from scaling model size. A small, fixed, theory-guided transformation "
            "placed before tokenization can improve zero-shot forecasting while "
            "leaving the transformer itself almost completely unchanged. For time "
            "series models, this suggests a practical path toward more accurate and "
            "parameter-efficient forecasters."
        ),
    },
]


def run(cmd: list[str]) -> None:
    print("+", " ".join(shlex.quote(x) for x in cmd))
    subprocess.run(cmd, check=True)


def probe_duration(path: Path) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(path),
    ]
    out = subprocess.check_output(cmd, text=True)
    return float(json.loads(out)["format"]["duration"])


def timestamp(seconds: float) -> str:
    ms = int(round((seconds - math.floor(seconds)) * 1000))
    total = int(math.floor(seconds))
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def wrap_caption(text: str, width: int = 62) -> str:
    words = text.split()
    lines: list[str] = []
    cur: list[str] = []
    cur_len = 0
    for word in words:
        extra = len(word) + (1 if cur else 0)
        if cur and cur_len + extra > width:
            lines.append(" ".join(cur))
            cur = [word]
            cur_len = len(word)
        else:
            cur.append(word)
            cur_len += extra
    if cur:
        lines.append(" ".join(cur))
    return "\n".join(lines)


def caption_chunks(text: str) -> list[str]:
    protected = text.replace("Moirai 2.0", "Moirai 2<DOT>0")
    protected = protected.replace("zero point one one percent", "zero point one one percent")
    chunks = re.split(r"(?<=[.!?])\s+", protected)
    chunks = [chunk.replace("<DOT>", ".").strip() for chunk in chunks if chunk.strip()]
    return chunks


def render_slides() -> list[Path]:
    doc = fitz.open(PDF)
    if doc.page_count != len(SLIDES):
        raise RuntimeError(f"Expected {len(SLIDES)} slides, found {doc.page_count}")
    slide_paths: list[Path] = []
    for i, page in enumerate(doc):
        # 1920x1080 for 16:9 beamer pages.
        scale = 1920 / page.rect.width
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        path = BUILD / f"slide_{i + 1:02d}.png"
        pix.save(path)
        slide_paths.append(path)
    return slide_paths


async def synthesize_audio() -> list[Path]:
    audio_paths: list[Path] = []
    for i, slide in enumerate(SLIDES, 1):
        path = BUILD / f"audio_{i:02d}.mp3"
        if path.exists():
            path.unlink()
        communicate = edge_tts.Communicate(slide["text"], VOICE, rate=RATE)
        await communicate.save(str(path))
        audio_paths.append(path)
    return audio_paths


def build_segments(slides: list[Path], audios: list[Path]) -> list[Path]:
    segment_paths: list[Path] = []
    for i, (slide, audio) in enumerate(zip(slides, audios), 1):
        duration = probe_duration(audio) + 0.35
        segment = BUILD / f"segment_{i:02d}.mp4"
        run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-t",
                f"{duration:.3f}",
                "-i",
                str(slide),
                "-i",
                str(audio),
                "-f",
                "lavfi",
                "-t",
                f"{duration:.3f}",
                "-i",
                "anullsrc=channel_layout=stereo:sample_rate=44100",
                "-filter_complex",
                "[1:a][2:a]amix=inputs=2:duration=first:dropout_transition=0[a]",
                "-map",
                "0:v",
                "-map",
                "[a]",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-tune",
                "stillimage",
                "-pix_fmt",
                "yuv420p",
                "-r",
                "30",
                "-c:a",
                "aac",
                "-b:a",
                "160k",
                "-shortest",
                str(segment),
            ]
        )
        segment_paths.append(segment)
    return segment_paths


def write_concat_file(segments: list[Path]) -> Path:
    concat = BUILD / "segments.txt"
    with concat.open("w") as f:
        for segment in segments:
            f.write(f"file '{segment.resolve()}'\n")
    return concat


def write_srt(audios: list[Path]) -> None:
    t = 0.0
    entries: list[str] = []
    idx = 1
    for audio, slide in zip(audios, SLIDES):
        duration = probe_duration(audio) + 0.35
        chunks = caption_chunks(slide["text"])
        weights = [max(1, len(chunk.split())) for chunk in chunks]
        total_weight = sum(weights)
        start = t
        for chunk, weight in zip(chunks, weights):
            end = start + duration * weight / total_weight
            entries.append(
                f"{idx}\n{timestamp(start)} --> {timestamp(end)}\n"
                f"{wrap_caption(chunk)}\n"
            )
            start = end
            idx += 1
        t = end
    SRT.write_text("\n".join(entries))


def write_script() -> None:
    lines: list[str] = []
    for i, slide in enumerate(SLIDES, 1):
        lines.append(f"Slide {i}: {slide['title']}")
        lines.append(slide["text"])
        lines.append("")
    SCRIPT.write_text("\n".join(lines))


def mux_video(concat: Path) -> None:
    raw = BUILD / "presentation_video_no_subs.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-c",
            "copy",
            str(raw),
        ]
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(raw),
            "-i",
            str(SRT),
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-c:s",
            "mov_text",
            "-metadata:s:s:0",
            "language=eng",
            str(OUT),
        ]
    )


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    slides = render_slides()
    audios = asyncio.run(synthesize_audio())
    write_script()
    write_srt(audios)
    segments = build_segments(slides, audios)
    concat = write_concat_file(segments)
    mux_video(concat)
    print(f"Wrote {OUT}")
    print(f"Wrote {SRT}")
    print(f"Wrote {SCRIPT}")
    print(f"Duration: {probe_duration(OUT):.1f} seconds")


if __name__ == "__main__":
    main()
