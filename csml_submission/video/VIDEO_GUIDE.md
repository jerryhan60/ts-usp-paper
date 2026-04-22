# CSML IW Video — Script & Slide Outline

**Target length:** 3:30 (well within the 2–5 min window)
**Delivery:** informal, conversational. Slides advance roughly every 25–30 sec.
**Recording tip:** record each slide separately, stitch with iMovie / OBS; keep camera overlay small so slides are readable.

---

## Slide deck outline (8 slides)

### Slide 1 — Title (0:00–0:12)
Content:
- **Polynomial Hint Preconditioning for Universal Time Series Forecasting**
- Jerry Han · Dept. of Mathematics + SML minor · Princeton University
- Advisor: Prof. Elad Hazan · Second Reader: Prof. Amit Singer
- Spring 2026

### Slide 2 — The problem (0:12–0:40)
Content:
- Image of patch-based transformer input pipeline (use `fig_architecture.pdf` left panel)
- Headline: **"Patch transformers have a cross-patch bottleneck."**
- Bullet: Each 16-step patch is embedded *independently* before any attention layer
- Bullet: A daily cycle in 15-min data = 96 steps = 6 patches — attention alone must discover this

### Slide 3 — Our fix in one line (0:40–1:10)
Content:
- The hint-channel equation: `h[t] = x[t] − x[t−32] + (1/8) x[t−64]` (big font)
- Cartoon of the concatenated-channel architecture (right panel of `fig_architecture.pdf`)
- Bullet: Fixed Chebyshev FIR filter, no learned parameters
- Callout: **+12K parameters = 0.11% overhead**

### Slide 4 — Why Chebyshev? (1:10–1:50)
Content:
- LEFT: Chebyshev minimax theorem statement (mini version)
  - $\tilde T_d$ minimises $\sup_{[-1,1]}|q|$ over monic degree-$d$
- RIGHT: Your `synth_lds_spectrum.pdf`
- Headline: **"The filter has notches exactly where the theorem predicts."**

### Slide 5 — Main result (1:50–2:25)
Content:
- Main table (`fig1_capacity_ablation.pdf`)
- Three bullets underneath:
  - **−2.9% geomean MASE** over baseline
  - **329 of 485 paired wins**, $p < 10^{-14}$ (Holm-corrected)
  - Effect of this size needs only 65 comparisons for 80% power; we ran 485

### Slide 6 — Why it's not just capacity (2:25–2:55)
Content:
- `fig1_capacity_ablation.pdf` (the capacity-control bars)
- Headline: **"Duplicating the input hurts. Zero channel is neutral. Only the polynomial content helps."**
- Bullet: HD vs Duplicate: 336/485 wins, $p = 6 × 10^{-18}$

### Slide 7 — Theory meets practice (2:55–3:20)
Content:
- Scatter plot: spectral passband fraction vs per-dataset improvement (39 GIFT-Eval datasets)
- Headline: **"Datasets whose spectrum aligns with the filter's passband benefit more."**
- Pearson $r = +0.10$, slope $+2.3%$ per unit passband fraction
- Takeaway: mechanism consistent with theory, effect is modest

### Slide 8 — Takeaways (3:20–3:30)
Content (3 bullets, big font):
- Classical approximation theory + modern foundation models, 0.11% parameter cost.
- Capacity-controlled: the **polynomial content** drives the gain, not the width.
- Submitted concurrently to ICML 2026 FMSD workshop.

---

## Script (spoken; ~450 words, 3:30 at conversational pace)

**[Slide 1]** Hi, I'm Jerry Han. For my junior paper in math and my SML IW, I studied what I call "polynomial hint preconditioning" for patch-based time-series forecasters. My advisor is Professor Elad Hazan and my second reader is Professor Amit Singer.

**[Slide 2]** The problem starts with how modern universal forecasters — Moirai, Chronos, TimesFM — process their input. They chop the time series into non-overlapping patches of sixteen steps, and embed each patch independently, before any attention happens. That works great for throughput, but it creates a bottleneck: if you have a daily cycle in fifteen-minute data, that cycle spans six patches, and the model has to rediscover that dependency purely through attention. Smaller foundation models, with fewer heads and layers, really struggle with this.

**[Slide 3]** My fix is one line of math: I compute a fixed FIR filter — this polynomial — of the raw series, and concatenate it as an extra input channel before patching. So the only thing that gets wider is the first linear layer. The transformer is untouched. And the overhead is twelve thousand parameters, about a tenth of a percent of an eleven-million-parameter Moirai-2 Small.

**[Slide 4]** The coefficients come from the monic Chebyshev polynomial. Two reasons: first, Chebyshev's classical minimax theorem says this is the unique monic polynomial that minimises the sup norm on minus-one to one — so it's the right worst-case choice. Second, Annie Marsden and Elad Hazan's recent preconditioning paper shows Chebyshev applied to an LDS observation sequence compresses its effective spectral radius, yielding improved regret bounds. I verified the frequency-response prediction on synthetic LDS data: the filter has notches at exactly the frequencies the theorem predicts, with depths matching the two-to-the-one-minus-d constant.

**[Slide 5]** On GIFT-Eval — ninety-seven dataset-horizon configurations with five seeds — my method improves geometric-mean MASE by two-point-nine percent over the Moirai-2 Small baseline, winning three-hundred-twenty-nine of four-hundred-eighty-five paired comparisons. After Holm-Bonferroni correction the p-value is under ten-to-the-minus-fourteen.

**[Slide 6]** The key methodological move is these capacity controls. I ran the exact same architecture with a "zero channel" and a "duplicate of the input" instead of the Chebyshev hint. Duplicating the input actually *hurts* — it wins only forty-five percent of comparisons. Zero is neutral. So the extra parameters alone don't explain the improvement — it really is the polynomial content.

**[Slide 7]** I also tested the spectral mechanism directly: for each dataset, I asked whether its power spectral density has more mass in the filter's "passband" frequencies. Datasets with more passband mass did benefit more, with a Pearson correlation of positive-point-one-oh. The effect is small but in the direction the theory predicts.

**[Slide 8]** Three takeaways: classical approximation theory plugs cleanly into modern foundation models; the effect is capacity-efficient, driven by polynomial content not extra width; and the same work appears concurrently at the ICML 2026 Structured Foundation Models workshop. Thanks.

---

## Recording checklist

- [ ] Slides exported as PDF (use `ts-usp-paper/junior_paper/figures/` + the poster panels)
- [ ] Camera + screen-share set up (e.g., OBS Studio, Zoom "Record to this Computer")
- [ ] Quiet room, external mic if available
- [ ] Final video: mp4 or mov, under 500 MB (Canvas cap)
- [ ] Upload via the "Record/Upload Media" option in the **CSML Undergraduate Poster Session 2026** Canvas assignment
- [ ] Submission deadline: **Friday, May 1, 2026, 9:00 AM EST**
