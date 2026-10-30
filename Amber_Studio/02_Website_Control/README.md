# Control website update — Amber and Amber Studio

The old saved-code attempt can no longer lock the Connect button. Editing the
code cancels the old attempt and its timers immediately. While connecting,
the button stays enabled as Cancel. Missing PCs, stalled connections and
approval waits have finite timeouts and leave the code editable.

Reconnecting when reopening the page is OFF by default. Check "Reconnect to
this code when I reopen" to opt in. Saved approval for each code is retained;
switching codes does not send the old PC's token to an unrelated PC. During
an active session, network recovery and returning from browser history resync
the PC. The connected PC's app name and code are shown. Change PC / code,
Disconnect, Forget this PC code and Refresh from PC are in the menu.

New and completed controls:

- Filter Queue, Liked and Recent while preserving the correct source indices.
- Queue options: play next, move up, move down, and remove the intended ID.
- Clear queue with confirmation; reject it if the PC queue changed meanwhile.
- Add a playlist/search list to the queue as one bounded, deduplicated action.
- Display the whole supported queue (up to 300), with no hidden extra tracks.
- Request a current-song download on the PC and show its reported status.
- Toggle related-song autoplay and copy the current YouTube song link.
- Retry failed searches; clearing/switching sessions discards late results.
- Command acknowledgements, duplicate suppression and useful rejection messages.
- No automatic replay of unconfirmed commands after reconnecting.
- Idempotent lock-screen Play/Pause commands and offline command guards.
- Cancel pending PC approval cleanly; discard stale desktop pairing callbacks.
- Separate Amber Studio phone preferences/search history from Classic.

Use the update:

1. Rebuild/install each desktop app from its own 01_Amber_Desktop_App folder.
   These ZIPs contain source/build files; an old EXE is not updated by replacing
   its Python source. The new remote capabilities require the rebuilt desktop.
2. Replace/deploy 02_Website_Control/index.html on your control website host.
   No website was published by this ZIP update. Existing hosted pages stay old
   until you redeploy them. For separate hosts, use the matching Classic or
   Studio controller; either accepts a valid PC code and shows the PC identity.
3. Close the old phone page and reopen/reload the deployed page. Enter the PC's
   current code. Press Allow on the PC when asked. Reconnect-on-reopen is optional.

The paired phone controls the PC; downloads save on the PC, not on the phone.
VB-Cable, microphone permission and OS hold-key selection remain PC setup steps.
The existing app UIs and distinct installer/data identities are preserved.
Voice clean-up still defaults OFF and retains explicit later choices.
No screenshots are included. Control and showcase sites remain separate:
the showcase uses its existing offline sample demo, not live pairing.

Validation: remote-test-results.json contains this update's host/client tests.
They run production client and desktop JavaScript in separate browser pages,
with a deterministic PeerJS transport and sample API responses. Desktop playback
and UI regression suites were also rerun. Real mobile browsers, Windows builds,
WebRTC/TURN across physical networks and live downloads still need PC/phone
testing. Earlier verification reports remain historical records of prior fixes.
