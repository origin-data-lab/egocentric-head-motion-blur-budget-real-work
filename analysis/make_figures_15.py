import os, numpy as np, pandas as pd, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT = 'out'; FIG = f'{OUT}/figures'; os.makedirs(FIG, exist_ok=True)
INK, GR, C1, C2, C3 = '#1d232b', '#8a8f98', '#1f5fbf', '#d9622b', '#2e9e6a'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10.5, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.color': '#e7eaee', 'axes.edgecolor': '#c9ced6', 'axes.axisbelow': True})
def save(fig, name): fig.savefig(f'{FIG}/{name}.png', dpi=170, bbox_inches='tight'); fig.savefig(f'{FIG}/{name}.svg', bbox_inches='tight'); plt.close(fig)
F = pd.read_csv(f'{OUT}/b2_per_frame.csv.gz'); n = len(F)
# 1 blur distribution
fig, ax = plt.subplots(figsize=(7, 3.9)); bins = np.logspace(-2, 1.7, 70)
ax.hist(F.blur_total_px.clip(lower=0.011), bins=bins, color=C1, alpha=0.85)
for thr, yy in ((1, 0.97), (3, 0.82), (8, 0.67)):
    ax.axvline(thr, color=INK, lw=0.8, ls='--'); ax.text(thr * 1.08, ax.get_ylim()[1] * yy, f'>{thr} px: {(F.blur_total_px > thr).mean()*100:.0f}%', fontsize=8.5, bbox=dict(fc='white', ec='none', pad=1))
ax.set_xscale('log'); ax.set_xlabel('Predicted motion blur per frame (px, log scale)'); ax.set_ylabel('Frames')
ax.set_title(f'Real produce-portioning work, ~10 ms exposure ({n:,} frames, 2 h 25 min)', loc='left', fontsize=11)
save(fig, 'fn15_blur_distribution')
# 2 what-if exposure
SH = pd.read_csv(f'{OUT}/b2_blur_shares.csv'); SH = SH[SH.threshold_px.isin([1, 2, 3, 5])]
fig, ax = plt.subplots(figsize=(7, 3.9)); x = np.arange(len(SH)); w = 0.2
for o, col, lab, c in [(-1.5 * w, 'actual', 'Recorded (~10 ms)', C2), (-0.5 * w, 'if_6ms', '6 ms', '#e9a07a'), (0.5 * w, 'if_4ms', '4 ms', '#7aa6e0'), (1.5 * w, 'if_2ms', '2 ms', C1)]:
    v = SH[col].values * 100; ax.bar(x + o, v, w, color=c, label=lab)
    for xi, vi in zip(x + o, v): ax.text(xi, vi + 1, f'{vi:.0f}', ha='center', fontsize=7.5)
ax.set_xticks(x); ax.set_xticklabels([f'> {t:g} px' for t in SH.threshold_px]); ax.set_ylabel('Share of frames (%)'); ax.grid(axis='x', visible=False)
ax.set_title('Same head motion, shorter exposure: share of blurred frames', loc='left', fontsize=11); ax.legend(frameon=False, fontsize=9, title='Exposure', title_fontsize=9)
save(fig, 'fn15_exposure_whatif')
# 3 validation
B = pd.read_csv(f'{OUT}/b2b_sharpness_by_blur.csv')
lab = ['0–0.5', '0.5–1', '1–2', '2–3', '3–5', '5–8', '>8']
fig, ax = plt.subplots(figsize=(7, 3.6)); ax.bar(range(len(B)), B.rel_sharpness_median, color=[C1] * 4 + [C2] * 3)
for i, (v, nn) in enumerate(zip(B.rel_sharpness_median, B.frames)): ax.text(i, v + 0.02, f'{v:.2f}\n(n={nn})', ha='center', fontsize=8)
ax.axhline(1, color=INK, lw=0.8, ls='--'); ax.set_xticks(range(len(B))); ax.set_xticklabels(lab); ax.set_ylim(0, 1.3); ax.grid(axis='x', visible=False)
ax.set_xlabel('Predicted blur from gyro (px)'); ax.set_ylabel('Image sharpness relative to\nneighbouring frames (median)')
ax.set_title('Check against the images: six 30 s clips, 5,400 frames', loc='left', fontsize=11)
save(fig, 'fn15_sharpness_validation')
print('ok')
