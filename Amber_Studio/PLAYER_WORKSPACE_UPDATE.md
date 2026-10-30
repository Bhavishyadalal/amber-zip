# Player and queue polish

Classic and Studio retain their own visual identities and the previous mic/colour fixes.

- Studio now follows Classic's player structure: playback left, queue right on wide screens.
- Queue owns its scrollbar. Up next, Auto Queue and Clear stay at the top, and playback controls stay visible.
- Narrow screens use Now playing / Up next buttons instead of placing the queue below playback. Selected buttons fill themselves; no sliding overlay or pane fade.
- Cover size and spacing adapt to shorter windows. Long titles are limited to two lines; queue titles ellipsize.
- Reserved space for track duration and Remove prevents hover collisions. Queue rows and controls have consistent spacing.
- Extreme windows shorter than 440px allow internal playback-panel scrolling so controls remain accessible; the page still stays fixed.

Validation: 194 layout/state checks, including 9 screen sizes from 1920x1080 to 320x568, long titles and 45 queue tracks. Playback panel fits, outer player does not scroll, queue stays contained, no detected control/text overlaps or horizontal overflow. Production wheel scrolling, fixed queue header and track removal passed. Other screens and mic controls rechecked.

All Python backend and JavaScript remain unchanged, including audio processing. Original package files retained byte-for-byte except the embedded frontend CSS in the main Python source.

Screenshots use sample music and simulated device listings. Native Windows audio and EXE builds were not tested here. Rebuild installed EXEs with each version's build_exe.bat.
