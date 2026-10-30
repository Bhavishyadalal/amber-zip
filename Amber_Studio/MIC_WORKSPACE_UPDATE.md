# Virtual mic workspace update — 10 October 2026

The virtual mic now has six directly accessible tabs: Mixer, Soundboard, Devices,
Hotkeys, Phone remote and Setup. Power and Stop all sounds remain available in
all tabs. The Mixer shows routing and all five volume controls together and fits
1280x720 desktop windows. Each version uses its own established UI styling:
Classic retains warm glass, rounded controls and album accents; Studio retains
its quieter dashboard and sidebar.

Use the update
--------------
Close the running app before updating. Extract the matching version into its
own folder. Run amber_app.py for Classic or amber_studio.py for Studio from the
01_Amber_Desktop_App folder. To update an installed EXE, rebuild that version
with its existing build_exe.bat, then install the resulting build.

The existing backend, audio processing, ducking, optional voice clean-up,
installer identities, phone controller and showcase files are retained.
Voice clean-up still starts OFF until the user explicitly configures it.
The separate transparent-audio and Spotify experiments remain separate.

Validation
----------
The mic control bindings, volume saving, keyboard tab navigation, accessible
panels, default clean-up state, existing ducking, device choices, and viewport
layout were checked in the production HTML/JavaScript for both versions.
The Python AST outside the embedded frontend is identical to the previous final
source. Original mic audio JavaScript is identical. The UI tests use simulated
Windows audio devices and backend data; native Windows audio and EXE builds
were not tested in this environment. Historical reports remain historical.

Screenshots are supplied as a separate ZIP, grouped by version and device size.
They show sample soundboard entries and simulated devices, with numbered files
for further scroll positions. They are previews, not recordings of real audio.
