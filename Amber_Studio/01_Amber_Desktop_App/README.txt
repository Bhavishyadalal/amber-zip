# Amber Studio desktop app

Run from source: `python amber_studio.py` (Python dependencies install on first run).
To build the Windows installer, run `build_exe.bat` on Windows. It installs the
build dependencies, builds the app folder, then runs Inno Setup when available.
The output is `dist/AmberStudioSetup.exe`.

Read `../README_FINAL.md` for coexistence, storage paths and the current logic
update. `../UX_AND_COEXISTENCE_UPDATE.txt` describes validation and its limits.
No compiled EXE is supplied in this source package. Rebuild old EXEs to apply
the fixes. Install Classic and Studio using their own default folders.


Virtual microphone audio update (2026-10-10)
See ../VIRTUAL_MIC_AUDIO_UPDATE.txt (project root) for the fix and checks.
If you use an EXE, rebuild using build_exe.bat; replacing the source does not update an old EXE.
