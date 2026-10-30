# Visual polish and overlap fixes

Studio keeps its existing layout and visual identity.

- Mic meter: 22 proportional grid columns instead of minimum-width flex bars. Bars remain inside their meter at all amplitudes.
- Dedicated grid columns for mic power, status, meter and Stop all sounds; responsive stop-button row on phones.
- Studio: consistent neutral charcoal surfaces in normal, performance, low-power and no-glow modes. Amber, violet and album accents remain available.
- Classic: warm glass and serif headings preserved; emergency stop has a restrained coral accent.
- Wrapped device/setting actions, remote controls, long labels and compact player tools. Fixed Classic mute/virtual-mic collision at 320px.
- Mic content no longer fades underneath a decorative mask; normal scrolling remains available.

Validation: 141 layout states checked at 1920x1080, 1280x720, 1024x768, 800x600, 390x844 and 320x740, including appearance and performance states. No detected control/text-group overlaps, meter overflow or page overflow. Production slider saves, stop availability and noise clean-up default verified. Python compiles; Python backend and all JavaScript are unchanged.

Screenshots use sample tracks and simulated audio-device listings. Native Windows audio and EXE builds were not tested in this environment. Rebuild an installed EXE with this version's build_exe.bat.
