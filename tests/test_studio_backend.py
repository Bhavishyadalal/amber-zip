"""Real Flask endpoints with isolated storage and stubbed upstream recommendations."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
storage = tempfile.TemporaryDirectory(prefix='amber-studio-test-')
os.environ['AMBER_STUDIO_FILES_DIR'] = storage.name
spec = importlib.util.spec_from_file_location('amber_studio_test', ROOT / 'Amber_Studio/01_Amber_Desktop_App/amber_studio.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class StudioBackend(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_home_empty_upstream_is_valid(self):
        with patch.object(app, '_get_shelf_radio', return_value=[]):
            response = self.client.get('/api/home?seed=invalid')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['shelves']), 4)
        self.assertTrue(all(s['items'] == [] for s in response.json['shelves']))

    def test_home_uses_seed_and_does_not_claim_chart_rankings(self):
        with patch.object(app, '_get_shelf_radio', return_value=[{'id': '12345678901', 'title': 'Example'}]) as get:
            response = self.client.get('/api/home?seed=abcdefghijk')
        self.assertEqual(get.call_count, 4)
        get.assert_any_call('abcdefghijk', 8)
        self.assertNotIn('charts', json.dumps(response.json).lower())

    def test_null_origin_and_cross_site_requests_blocked(self):
        for headers in [{'Origin': 'null'}, {'Sec-Fetch-Site': 'cross-site'}, {'Origin': 'https://example.com'}]:
            self.assertEqual(self.client.post('/api/data', json={'queue': []}, headers=headers).status_code, 403)
        self.assertEqual(self.client.post('/api/data', json={'queue': []}, headers={'Origin': 'http://localhost'}).status_code, 200)

    def test_library_revision_and_backup_recovery(self):
        track = {'id': 'abcdefghijk', 'title': 'Preserve this track'}
        self.assertEqual(self.client.post('/api/data', json={'queue': [track], 'revision': 100}).status_code, 200)
        self.assertTrue(self.client.post('/api/data', json={'queue': [], 'revision': 99}).json['stale'])
        self.assertEqual(self.client.get('/api/data').json['queue'][0]['id'], track['id'])
        self.client.post('/api/data', json={'queue': [track], 'revision': 101})
        app.DATA_FILE.write_text('{broken')
        self.assertEqual(self.client.get('/api/data').json['queue'][0]['id'], track['id'])

    def test_optional_rtc_configuration_safely_embedded(self):
        with patch.dict(os.environ, {'AMBER_STUDIO_RTC_CONFIG': '{"iceServers":[],"note":"</script><script>bad()</script>"}'}):
            text = self.client.get('/').text
        self.assertIn('window.AMBER_RTC_CONFIG=', text)
        self.assertNotIn('</script><script>bad()', text)
        with patch.dict(os.environ, {'AMBER_STUDIO_RTC_CONFIG': 'not json'}):
            self.assertEqual(self.client.get('/').status_code, 200)

    def test_studio_identity_and_packaged_vendor(self):
        self.assertEqual(self.client.get('/api/identity').json['app_id'], 'Amber.Studio.AudioPlayer')
        self.assertEqual(self.client.get('/vendor/qrcode.js').status_code, 200)


if __name__ == '__main__':
    unittest.main()
