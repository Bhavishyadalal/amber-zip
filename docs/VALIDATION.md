# Afterhours validation

Run on 30 October 2026 in the Linux workspace. **17 tests passed:** 11 Chromium browser tests and 6 real Flask endpoint tests.

## Browser checks

The tests execute the production desktop HTML/CSS/JavaScript in Chromium, with controlled API responses and artwork. They check:

- Personalized recent listening and liked-track counts; shelf filtering and queue persistence.
- Empty recommendations and a first-use library; discovery failure, retry and retention of previous results.
- Late obsolete responses cannot overwrite a newer refresh. A request with a caller-supplied cancellation signal still times out and aborts its actual fetch.
- Home resume preserves the paused playback position and queue, using an actual browser Audio element and a synthetic WAV fixture with byte-range support.
- Autoplay off does not fetch related tracks on play.
- Recommendation titles render as text rather than executable HTML.
- All seven tabs, home shortcuts, keyboard search, active navigation and reduced-motion behavior.
- No uncaught JavaScript errors during these scenarios.
- No page or main-view horizontal overflow at widths **360, 390, 700, 768, 980, 981, 1180, 1440 and 1920 pixels**, across all seven tabs.

Current desktop and phone screenshots in `previews/` use sample music metadata and generated artwork fixtures. They show the production UI, not a live music session.

## Backend checks

Flask's real test client exercises the imported app with isolated temporary storage:

- Home response with empty upstream recommendations and with a supplied seed.
- Recommendation descriptions do not claim live chart rankings.
- Null-origin and cross-site mutations are rejected; local-origin requests work.
- Older library revisions cannot overwrite newer state; corrupt main JSON recovers from the valid backup.
- Optional deployment-owned WebRTC configuration is safely embedded in HTML, and invalid configuration falls back without breaking the page.
- Studio's identity and the packaged QR vendor script are served successfully.

Python parses successfully. All **8 inline JavaScript blocks** across the desktop, controller and supplied showcase pass Node's syntax check.

## Live check and limits

The actual Flask home endpoint returned HTTP 200 during an unmocked smoke check, with four empty shelves. YouTube requests were denied by the workspace proxy with **403 Forbidden**. The app's unavailable/empty discovery UI is covered, but live YouTube discovery, streaming and downloads could not be validated in this environment.

Windows installer compilation, WebView2, physical microphone/VB-Cable routing, native hotkeys and real PC/phone WebRTC/TURN pairing remain untested. The release ZIP contains source and build instructions, not a newly compiled EXE. Networks requiring a relay need deployment-owned TURN configuration on the desktop and controller.

Earlier JSON reports shipped with the upload are retained as historical material. They do not count as runs for this update. These checks cover the listed behaviors and do not establish that every possible bug has been eliminated.
