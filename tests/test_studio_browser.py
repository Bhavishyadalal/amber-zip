"""Production desktop HTML in Chromium; deterministic API and artwork fixtures.

Run: python -m unittest discover -s tests -p 'test_studio_browser.py' -v
Requires Playwright and its Chromium browser. No YouTube/audio/device claims.
"""
import ast
import io
import json
import re
from pathlib import Path
import unittest
import wave
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'Amber_Studio/01_Amber_Desktop_App'
tree = ast.parse((APP / 'amber_studio.py').read_text())
HTML = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == 'FRONTEND_HTML' for t in n.targets))
TRACKS = [{'id': f'track{i:06d}', 'title': name, 'sub': artist, 'dur': '3:24',
           'thumb': f'https://i.ytimg.com/vi/track{i:06d}/hq720.jpg'}
          for i, (name, artist) in enumerate([
              ('Midnight City', 'M83'), ('Electric Feel', 'MGMT'), ('Tame the Night', 'Studio sessions'),
              ('After Hours', 'The Weeknd'), ('Space Song', 'Beach House'), ('Feel It All', 'Independent sounds'),
              ('New Frequencies', 'Late night radio'), ('Soft Landing', 'Slow sessions')])]
SHELVES = [{'id': key, 'title': title, 'subtitle': 'Related listening, selected for a new direction.',
            'items': [dict(t) for t in TRACKS]}
           for key, title in [('picks', 'Your next rabbit hole'), ('trending', 'On repeat'),
                              ('lofi', 'Take the slow lane'), ('ambient', 'A little headspace')]]


class StudioBrowser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 1000})
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror', lambda err: self.errors.append(str(err)))
        self.home_calls = 0
        self.home_mode = 'normal'
        self.saved = []
        self.has_library = True
        self.synthetic_audio = False
        self.context.route('**/*', self.route)

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [], 'Uncaught production JavaScript errors')

    def route(self, route):
        request = route.request
        url = urlsplit(request.url)
        p = url.path
        if p == '/':
            return route.fulfill(body=HTML, content_type='text/html')
        if p.startswith('/vendor/'):
            return route.fulfill(body=(APP / p.lstrip('/')).read_bytes(), content_type='text/javascript')
        if 'ytimg.com' in url.netloc or p == '/api/art':
            color = ['#8d6eb8', '#b46a53', '#6c9f86', '#626cc0'][sum(map(ord, request.url)) % 4]
            svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600"><rect width="600" height="600" fill="{color}"/><circle cx="300" cy="300" r="190" fill="#172122"/><circle cx="300" cy="300" r="65" fill="#d7fa58"/><path d="M0 520 600 100" stroke="#ffffff30" stroke-width="90"/></svg>'
            return route.fulfill(body=svg, content_type='image/svg+xml')
        data = {'ok': True}
        if p == '/api/data':
            if request.method == 'POST':
                self.saved.append(request.post_data_json)
            else:
                data = {'queue': TRACKS[:2] if self.has_library else [], 'recent': TRACKS[:6] if self.has_library else [],
                        'liked': TRACKS[:3] if self.has_library else [], 'revision': 1, 'session': {'tab': 'home'}}
        elif p == '/api/home':
            self.home_calls += 1
            if self.home_mode == 'failure':
                return route.fulfill(status=503, json={'error': 'unavailable'})
            data = {'shelves': SHELVES if self.home_mode == 'normal' else [dict(s, items=[]) for s in SHELVES]}
        elif p == '/api/config':
            data = {'locked': False, 'alive': 1, 'total': 1, 'has_manual': True}
        elif p == '/api/health':
            data = {'ok': True, 'ffmpeg': True, 'ytdlp': 'fixture', 'version': 'fixture'}
        elif p == '/api/downloads' or p == '/api/vd/files':
            data = {'files': [], 'downloads': []}
        elif p == '/api/vd/jobs':
            data = {'jobs': []}
        elif p == '/api/sb/state':
            data = {'sounds': [], 'settings': {}, 'hotkeys': {}, 'defaults': {}, 'hk': {'seq': 0, 'status': {}, 'supported': False}}
        elif p == '/api/cache':
            data = {'enabled': True, 'count': 0, 'bytes': 0, 'limit_mb': 512}
        elif p == '/api/related/track000000':
            data = {'results': []}
        elif p.startswith('/api/stream/'):
            if self.synthetic_audio:
                buffer = io.BytesIO()
                with wave.open(buffer, 'wb') as wav:
                    wav.setnchannels(1)
                    wav.setsampwidth(2)
                    wav.setframerate(8000)
                    wav.writeframes(b'\x00\x00' * 8000 * 30)
                body = buffer.getvalue()
                requested = request.headers.get('range', '')
                if requested:
                    match = re.fullmatch(r'bytes=(\d+)-(\d*)', requested)
                    start = int(match[1])
                    end = min(int(match[2]) if match[2] else len(body)-1, len(body)-1)
                    return route.fulfill(status=206, body=body[start:end+1], content_type='audio/wav',
                                         headers={'Accept-Ranges': 'bytes', 'Content-Range': f'bytes {start}-{end}/{len(body)}'})
                return route.fulfill(body=body, content_type='audio/wav', headers={'Accept-Ranges': 'bytes'})
            return route.fulfill(status=404, body='No real audio in fixture')
        elif '/status' in p:
            data = {'status': 'idle'}
        return route.fulfill(json=data)

    def load(self):
        self.page.goto('http://127.0.0.1:8878/')
        self.page.wait_for_function("document.querySelector('#home-content').getAttribute('aria-busy') === 'false' && window.S")

    def go(self, tab):
        self.page.locator(f'#nav [data-tab="{tab}"]').click()
        self.page.wait_for_function('(tab) => document.body.dataset.tab === tab', arg=tab)

    def test_home_personalization_filters_and_queue(self):
        self.load()
        self.assertEqual(self.page.locator('.studio-hero').count(), 1)
        self.assertEqual(self.page.locator('.studio-resume').count(), 6)
        self.assertIn('3 liked tracks', self.page.locator('#home-liked-count').inner_text())
        self.assertEqual(self.page.locator('.shelf-section').count(), 4)
        self.page.locator('[data-home-filter="lofi"]').click()
        self.assertEqual(self.page.locator('.shelf-section').count(), 1)
        self.assertIn('slow lane', self.page.locator('.shelf-section h3').inner_text())
        self.page.locator('.shelf-card').nth(3).get_by_role('button', name='Add After Hours to queue').click()
        self.assertEqual(self.page.evaluate('window.S.queue.length'), 3)
        self.assertEqual(self.page.evaluate('window.S.queue[2].title'), 'After Hours')
        self.page.wait_for_timeout(450)
        self.assertTrue(any(len(s['queue']) == 3 for s in self.saved))

    def test_empty_recommendations_and_new_user(self):
        self.home_mode = 'empty'
        self.has_library = False
        self.load()
        self.assertIn('A little quiet', self.page.locator('#home-content').inner_text())
        self.assertIn('Your soundtrack starts', self.page.locator('#home-personal').inner_text())
        self.page.locator('#home-resume').click()
        self.assertEqual(self.page.evaluate('document.body.dataset.tab'), 'browse')
        self.assertTrue(self.page.locator('#q').evaluate('(el)=>el===document.activeElement'))

    def test_failure_retry_and_keep_previous_results(self):
        self.home_mode = 'failure'
        self.load()
        self.assertIn('taking a break', self.page.locator('#home-content').inner_text())
        self.home_mode = 'normal'
        self.page.locator('[data-home-retry]').click()
        self.page.wait_for_selector('.shelf-card')
        self.home_mode = 'failure'
        self.page.locator('#home-refresh').click()
        self.page.wait_for_function("document.querySelector('#home-request-status').textContent.includes('Keeping')")
        self.assertEqual(self.page.locator('.shelf-section').count(), 4)

    def test_navigation_shortcuts_and_keyboard(self):
        self.load()
        for tab in ['library', 'mic', 'download', 'setup', 'player', 'browse', 'home']:
            self.go(tab)
            self.assertEqual(self.page.locator('#nav [aria-current="page"]').count(), 1)
        self.page.locator('.studio-shortcut[data-workspace-go="mic"]').click()
        self.assertEqual(self.page.evaluate('document.body.dataset.tab'), 'mic')
        self.page.keyboard.press('Control+k')
        self.assertEqual(self.page.evaluate('document.body.dataset.tab'), 'browse')
        self.assertTrue(self.page.locator('#q').evaluate('(el)=>el===document.activeElement'))

    def test_late_recommendations_cannot_replace_newer_results(self):
        self.context.add_init_script('''
          const originalFetch=window.fetch;window.delayedHome=[];
          window.fetch=(url,options)=>String(url).startsWith('/api/home')
            ? new Promise(resolve=>window.delayedHome.push(data=>resolve(new Response(JSON.stringify(data),{status:200}))))
            : originalFetch(url,options);
        ''')
        self.page.goto('http://127.0.0.1:8878/')
        self.page.wait_for_function('window.delayedHome.length===1')
        self.page.locator('#home-refresh').click()
        self.page.wait_for_function('window.delayedHome.length===2')
        fresh = [dict(SHELVES[0], title='The fresh result')]
        self.page.evaluate('(s)=>window.delayedHome[1]({shelves:s})', fresh)
        self.page.wait_for_selector('.shelf-card')
        old = [dict(SHELVES[0], title='The obsolete result')]
        self.page.evaluate('(s)=>window.delayedHome[0]({shelves:s})', old)
        self.assertEqual(self.page.locator('.shelf-section h3').inner_text(), 'The fresh result')
        self.assertEqual(self.page.locator('#home-content').get_attribute('aria-busy'), 'false')

    def test_home_timeout_cancels_caller_signal_request(self):
        self.context.add_init_script('''
          const originalTimeout=window.setTimeout;
          window.setTimeout=(fn,delay,...args)=>originalTimeout(fn,delay===45000?100:delay,...args);
          const originalFetch=window.fetch;
          window.fetch=(url,options)=>String(url).startsWith('/api/home')
            ? new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>{
                window.homeWasAborted=true;reject(new DOMException('Aborted','AbortError'));
              },{once:true}))
            : originalFetch(url,options);
        ''')
        self.load()
        self.assertTrue(self.page.evaluate('window.homeWasAborted'))
        self.assertIn('taking a break', self.page.locator('#home-content').inner_text())

    def test_autoplay_disabled_does_not_fetch_related_on_play(self):
        self.context.add_init_script("localStorage.setItem('amberstudio.auto','0')")
        calls = []
        self.page.on('request', lambda req: calls.append(req.url) if '/api/related/' in req.url else None)
        self.load()
        self.page.evaluate('window.AmberPlayer.playNow(window.S.recent[0],true)')
        self.page.wait_for_timeout(100)
        self.assertEqual(calls, [])

    def test_recommendation_text_is_escaped(self):
        self.load()
        hostile = dict(TRACKS[0], id='safe0000000', title='<img src=x onerror="window.injected=true">')
        self.page.route('**/api/home*', lambda route: route.fulfill(json={'shelves': [dict(SHELVES[0], items=[hostile])]}))
        self.page.locator('#home-refresh').click()
        self.page.wait_for_function("document.querySelector('.shelf-card .c-title')?.textContent.includes('<img')")
        self.assertFalse(self.page.evaluate('!!window.injected'))
        self.assertEqual(self.page.locator('.shelf-card .c-title img').count(), 0)

    def test_home_resume_preserves_playback_position_and_queue(self):
        self.synthetic_audio = True
        self.context.add_init_script("localStorage.setItem('amberstudio.auto','0')")
        self.load()
        self.page.locator('#home-resume').click()
        self.page.wait_for_function('window.S.playing')
        self.page.evaluate('window.AmberPlayer.seekBy(12)')
        self.page.wait_for_function('window.AmberPlayer.pos() >= 12')
        self.page.locator('#btn-play').click()
        self.page.wait_for_function('!window.S.playing')
        before = self.page.evaluate('window.AmberPlayer.pos()')
        self.assertGreater(before, 11)
        self.go('home')
        self.page.locator('#home-resume').click()
        self.page.wait_for_function('window.S.playing')
        self.assertGreaterEqual(self.page.evaluate('window.AmberPlayer.pos()'), before - .5)
        self.assertEqual(self.page.evaluate('window.S.queue.length'), 2)

    def test_responsive_layout_and_previews(self):
        self.load()
        for width in [360, 390, 700, 768, 980, 981, 1180, 1440, 1920]:
            self.page.set_viewport_size({'width': width, 'height': 900})
            for tab in ['home', 'player', 'mic', 'setup', 'library', 'download', 'browse']:
                self.go(tab)
                self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (width, tab))
                view = self.page.locator('#view')
                self.assertTrue(view.evaluate('(el) => el.scrollWidth <= el.clientWidth + 1'), (width, tab, 'view overflow'))
            self.go('home')
        self.page.set_viewport_size({'width': 1440, 'height': 1000})
        self.page.screenshot(path=str(ROOT / 'docs/previews/studio-desktop.png'), animations='disabled')
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.screenshot(path=str(ROOT / 'docs/previews/studio-mobile.png'), full_page=True, animations='disabled')

    def test_reduced_motion_and_home_focus(self):
        self.context.close()
        self.context = self.browser.new_context(reduced_motion='reduce')
        self.context.route('**/*', self.route)
        self.page = self.context.new_page()
        self.page.on('pageerror', lambda err: self.errors.append(str(err)))
        self.load()
        self.assertTrue(self.page.evaluate("document.documentElement.classList.contains('quiet-motion')"))
        self.assertEqual(self.page.locator('.studio-art svg').evaluate('(el)=>getComputedStyle(el).animationName'), 'none')
        self.page.locator('[data-home-filter="lofi"]').focus()
        self.page.keyboard.press('Enter')
        self.assertEqual(self.page.locator('[data-home-filter="lofi"]').get_attribute('aria-pressed'), 'true')
        self.assertEqual(self.page.locator('.shelf-card [role="button"]').count(), 0)


if __name__ == '__main__':
    unittest.main()
