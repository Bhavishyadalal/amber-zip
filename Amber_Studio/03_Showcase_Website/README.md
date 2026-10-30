# Amber Studio Showcase — polished edition

Open `index.html` in a current browser, or upload it as the index page on any static host. It is a single self-contained HTML file: fonts, gallery images, the desktop sample and the interactive phone-remote sample are embedded. The screenshot files are optional reference material.

## What changed

- Stable desktop navigation; no shrinking navbar or clipped Download button.
- Responsive mobile menu with Escape, outside-click and keyboard support.
- Refined purple layout, spacing, typography, cards and touch targets.
- Fixed horizontal page movement, incomplete section markup and hidden content.
- One desktop preview with seven working tour areas and sample interactions.
- Sample track search, player controls, queue, likes and keyboard seeking.
- Seven fresh gallery views, including Mic + Pads, with keyboard navigation.
- Phone demo runs without real pairing or a connection library. Fixed simulated pause/skip position handling.
- Removed the missing background-audio dependency, unexpected autoplay, custom-cursor loops and particle rendering.
- Lazy demo loading, shared embedded fonts, smaller WebP images and reduced-motion support.

## Demo behaviour

The desktop and phone views are offline simulations. Sample player controls do not stream audio. Downloads, virtual microphone routing, device access and live search require the Windows app. Demo switches change preview state only.

The download, Telegram, official VB-Audio and real remote links retain their original destinations. These external destinations were not validated for availability in this revision.

## Performance

The showcase HTML is approximately 918 KB, compared with 1,804,581 bytes in the supplied archive: about 49% smaller. This is a file-size comparison, not a speed benchmark. Viewing the showcase requires no external network requests; following an external link does.

## Verification

Checked in Chromium at 320, 390, 768, 1024, 1100, 1101, 1280 and 1440 pixels. No page or navbar overflow, broken section targets, JavaScript errors or failed image loads were found. Menu, tour, sample search, queue, gallery keyboard navigation, remote playback/voice/pads, FAQ and reduced-motion controls were exercised. This does not validate the Windows executable or actual device pairing.

See `screenshots/` for desktop and phone previews and `QA_RESULTS.json` for recorded checks.
