# CSML IW Video Guide

Generated video: `presentation_video.mp4`.

Runtime: 4:13, within the required 2-5 minute window.

Build inputs and outputs:
- `presentation.pdf` is rendered as the slide background.
- `presentation_script.txt` is the narration script.
- `make_video.py` generates text-to-speech narration with `edge-tts`, sentence-level SRT captions, and the final MP4.
- `presentation_subtitles.srt` is also provided separately; the MP4 includes the same captions as an embedded English subtitle track.
- Upload `presentation_video.mp4` through the Canvas "Record/Upload Media" option.

## Slide Outline

1. Title and project framing.
2. USP preliminaries: fixed polynomial preconditioning.
3. Problem: patch-based forecasters have a cross-patch bottleneck.
4. Method: add a fixed Chebyshev residual channel before patching.
5. Architecture: highlight the changed preconditioning/input-projection path.
6. Main result: GIFT-Eval improvement and capacity controls.
7. External validation and ablations: FEV-Bench, degree sweep, learned coefficients.
8. Training dynamics and horizon effects.
9. Takeaways and impact.

## Spoken Script

See `presentation_script.txt`, which is the exact script used for text-to-speech generation.

## Recording Checklist

- `poster.pdf` exported and checked.
- `paper.pdf` exported and checked.
- `presentation.pdf` exported and used for the video background.
- `presentation_video.mp4` generated and checked.
- Video length between 2 and 5 minutes.
- Title and abstract copied from `title_abstract.txt`.
- All materials uploaded before Friday, May 1, 2026 at 9:00 AM EST.
