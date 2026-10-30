# AMBER — FINAL PROJECT ARCHIVE

## Showcase polish revision

The showcase has received visual, interaction and loading fixes. Read `SHOWCASE_CHANGELOG.md` and `03_Showcase_Website/README.md` for the revision details and verification limits. The desktop app and real remote source are preserved.

## Project status

This archive is the final organized Amber Studio project package. It separates the Windows desktop application, the live Website Control page, and the public showcase website so each part can be maintained or deployed independently.

## Folder structure

```text
Amber_FINAL/
├── 01_Amber_Desktop_App/
│   ├── amber_studio.py
│   ├── Amber Studio.spec
│   ├── Amber Studio.iss
│   ├── build_exe.bat
│   ├── requirements.txt
│   ├── amber.ico
│   ├── vendor/
│   └── README.md
│
├── 02_Website_Control/
│   ├── index.html
│   └── README.md
│
├── 03_Showcase_Website/
│   ├── index.html
│   ├── screenshots/
│   └── README.md
│
└── 04_Documentation/
    └── PROJECT_FINAL_README.md
```

## 1. Desktop application

The `01_Amber_Desktop_App` folder is the source/build side of Amber Studio for Windows. The source package is preserved rather than rewritten during final packaging.

The main application is `amber_studio.py`. The included build files support PyInstaller and Inno Setup workflows. See that folder's README and the original `README.txt` for source-specific instructions.

## 2. Website Control

`02_Website_Control/index.html` is the real phone/browser remote from the Amber Studio project. It connects to Amber Studio using the normal pairing workflow and is intended for the actual remote-control experience.

## 3. Showcase website

`03_Showcase_Website/index.html` is the final public-facing showcase. It is intentionally a **single HTML file**. The pairing-free interactive Remote demo is embedded inside it, so the showcase can be deployed as one file without needing a second local HTML file.

The showcase also contains the current feature tour, virtual-mic/VB-CABLE guide, installation information, FAQ, and a link to the real remote.

## 4. Visual QA

The `screenshots` folder contains desktop and phone scroll captures of the final showcase. These are reference/QA assets and are not required for the showcase itself to run.

## Recommended deployment

### Desktop application

Keep `01_Amber_Desktop_App` as the source/build archive. Build the Windows executable using the included build configuration.

### Real remote

Deploy/host `02_Website_Control/index.html` wherever you want the actual phone remote page to be reachable. The page requires a running Amber Studio instance and normal pairing.

### Public showcase

Deploy `03_Showcase_Website/index.html` as a static page. The HTML is self-contained with respect to the interactive demo.

## Final verification performed during packaging

- Source package contents were extracted from the supplied final Amber Studio ZIP.
- Desktop source/build files were copied without rewriting their contents.
- The actual Website Control page was copied into its dedicated folder.
- The showcase Remote demo was embedded directly into the final showcase HTML.
- The final showcase no longer references a local `amber-remote-demo.html` file.
- Showcase and remote HTML were parsed successfully during packaging.
- Python source syntax was checked with Python's AST parser.
- A SHA-256 manifest is included at the archive root.

## Important external dependencies/services

The project can use network services and external resources as described by the source code. The showcase intentionally links to official VB-Audio resources and the real Amber Studio Remote. These are not copied into this archive.

## Archive philosophy

This ZIP is the archival master. Keep an untouched copy of it somewhere safe before making future edits. If you create a newer Amber Studio version later, make a new versioned archive rather than overwriting this final master.
