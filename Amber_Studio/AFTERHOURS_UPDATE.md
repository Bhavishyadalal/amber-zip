# Amber Studio — Afterhours update

30 October 2026

The Studio desktop has a new home composition and a refreshed visual shell. The home screen combines an original inline vector illustration with recent listening, collection/voice/download shortcuts and selectable recommendation shelves. Artwork is embedded; no external image-generation service or runtime image dependency is required.

Home discovery now handles shelves containing zero items, malformed recommendation items, failed refreshes, and late responses from superseded requests. Existing results remain available when a refresh fails. Recent listening remains usable independently of discovery. Recommendation labels describe related listening rather than claiming chart rankings.

Home playback resumes a paused current track without resetting its position or replacing its queue. Automatic related-track fetching respects the autoplay switch; explicitly requesting similar tracks still works. Programmatic queue scrolling follows reduced-motion preferences. The global request helper enforces timeouts even when a caller supplies its own cancellation signal.

The interface uses short entrance/hover transitions, clear focus outlines, native buttons for recommendation actions and separate controls rather than nested button roles. Motion is suppressed by reduced-motion preferences, with performance/low-power modes avoiding the new entrance animations.

Download pause/resume now reads the JSON response and HTTP status before reporting success. The local API rejects null-origin and cross-site browser requests. Embedded third-party relay credentials were removed from the desktop and controller. Public STUN remains configured; restrictive networks need a deployment-owned TURN configuration, as described in the repository README.

Studio's executable name, installer identity, default port, app data paths, saved-state format, desktop audio/backend implementation and bundled vendor dependencies are retained. Amber Classic was not edited. The controller and showcase retain their existing designs; the controller additionally supports a deployment-owned RTC configuration file.

Build a new Windows installer to apply this source update to an installed EXE. Replacing Python source does not change an already-built executable. No website has been deployed by this source update.

Current validation is recorded in `docs/VALIDATION.md` in the repository. Earlier verification JSON files and earlier release notes are historical; they are not evidence that Windows hardware or live network services were tested for this update.
