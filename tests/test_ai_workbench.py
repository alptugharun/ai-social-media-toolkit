from __future__ import annotations
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ai_workbench', ROOT / 'tools' / 'ai_workbench.py')
wb = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(wb)


class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.cards = wb.load_catalog()
        self.card = self.cards[0]

    def test_all_cards_have_bilingual_contracts(self):
        self.assertEqual(8, len(self.cards))
        for card in self.cards:
            for field in ('instructions', 'sample_input', 'expected_output', 'acceptance'):
                for lang in ('en', 'tr'):
                    self.assertGreater(len(card[field][lang]), 30)

    def test_invalid_catalog_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'catalog.json'
            path.write_text('{"schema_version":2,"cards":[]}', encoding='utf-8')
            with self.assertRaises(ValueError):
                wb.load_catalog(path)

    def test_duplicate_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'catalog.json'
            path.write_text(json.dumps({'schema_version':1, 'cards':[self.card, self.card]}), encoding='utf-8')
            with self.assertRaises(ValueError):
                wb.load_catalog(path)

    def test_unknown_card_is_rejected(self):
        with self.assertRaises(ValueError):
            wb.find_card(self.cards, '../secret')

    def test_all_export_targets_and_languages(self):
        for target in wb.TARGETS:
            for lang in ('en', 'tr'):
                with self.subTest(target=target, lang=lang):
                    text = wb.export_card(self.card, target, lang)
                    self.assertIn(self.card['instructions'][lang], text)
                    self.assertIn('Acceptance check', text)
                    self.assertIn('not a measured model result', text)

    def test_skill_has_frontmatter_and_license(self):
        text = wb.export_card(self.card, 'skill', 'en')
        self.assertTrue(text.startswith('---\nname: evidence-desk\n'))
        self.assertIn('license: CC-BY-NC-4.0', text)

    def test_gpt_export_is_not_a_published_gpt_claim(self):
        self.assertIn('not an installed or published GPT', wb.export_card(self.card, 'gpt', 'en'))

    def test_invalid_export_target(self):
        with self.assertRaises(ValueError):
            wb.export_card(self.card, 'unknown', 'tr')

    def test_openai_payload_has_no_automatic_tools(self):
        p = wb.build_payload('openai', 'test-model', 'rules', 'data', 1024)
        self.assertEqual('rules', p['instructions'])
        self.assertFalse(p['store'])
        self.assertNotIn('tools', p)

    def test_xai_payload_keeps_roles(self):
        p = wb.build_payload('xai', 'test-model', 'rules', 'data', 1024)
        self.assertEqual(['system','user'], [x['role'] for x in p['input']])
        self.assertFalse(p['store'])

    def test_anthropic_payload(self):
        p = wb.build_payload('anthropic', 'test-model', 'rules', 'data', 1024)
        self.assertEqual('rules', p['system'])
        self.assertEqual(1024, p['max_tokens'])
        self.assertEqual('user', p['messages'][0]['role'])

    def test_invalid_request_parameters(self):
        for provider, model, text, limit in [('other','m','x',64),('openai','','x',64),('openai','m','',64),('openai','m','x',0),('openai','m','x',99999),('openai','m','a'*100001,64)]:
            with self.subTest(provider=provider, limit=limit), self.assertRaises(ValueError):
                wb.build_payload(provider, model, 'rules', text, limit)

    def test_responses_text_extraction(self):
        result = {'status':'completed','output':[{'type':'reasoning','summary':[]},{'type':'message','content':[{'type':'output_text','text':'hello'}]}]}
        self.assertEqual('hello', wb.extract_text('openai', result))
        self.assertEqual('hello', wb.extract_text('xai', result))

    def test_anthropic_text_extraction(self):
        self.assertEqual('hello', wb.extract_text('anthropic', {'stop_reason':'end_turn','content':[{'type':'text','text':'hello'}]}))

    def test_incomplete_response_is_not_success(self):
        with self.assertRaises(ValueError):
            wb.extract_text('openai', {'status':'incomplete','output':[]})

    def test_refusal_or_empty_response_is_not_success(self):
        with self.assertRaises(ValueError):
            wb.extract_text('xai', {'status':'completed','output':[]})

    def test_truncated_claude_response_is_not_success(self):
        with self.assertRaises(ValueError):
            wb.extract_text('anthropic', {'stop_reason':'max_tokens','content':[{'type':'text','text':'partial'}]})

    def test_api_error_is_not_success(self):
        with self.assertRaises(ValueError):
            wb.extract_text('openai', {'error':{'message':'do not expose details'}})

    def test_redirect_is_refused(self):
        with self.assertRaises(ValueError):
            wb.NoRedirect().redirect_request(None,None,302,'',{},'https://example.com')

    def test_missing_key_blocks_network(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(wb.urllib.request,'build_opener') as mock:
            with self.assertRaises(ValueError):
                wb.call_provider('openai', {}, 30)
            mock.assert_not_called()

    def test_timeout_bounds(self):
        with self.assertRaises(ValueError):
            wb.call_provider('openai', {}, 301)

    def test_live_request_is_fixed_endpoint_and_one_call(self):
        reply = json.dumps({'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':'ok'}]}]}).encode()
        opener=MagicMock()
        opener.open.return_value.__enter__.return_value.read.return_value=reply
        with patch.dict(os.environ, {'OPENAI_API_KEY':'local-test-secret'}), patch.object(wb.urllib.request,'build_opener',return_value=opener):
            result=wb.call_provider('openai', {'model':'test'}, 30)
        self.assertEqual('ok',result)
        self.assertEqual(1,opener.open.call_count)
        self.assertEqual('https://api.openai.com/v1/responses',opener.open.call_args.args[0].full_url)

    def test_http_error_is_redacted_without_retry(self):
        opener=MagicMock()
        opener.open.side_effect=urllib.error.HTTPError('https://api.openai.com/v1/responses',429,'sensitive data',{},None)
        with patch.dict(os.environ, {'OPENAI_API_KEY':'local-test-secret'}), patch.object(wb.urllib.request,'build_opener',return_value=opener):
            with self.assertRaises(ValueError) as caught:
                wb.call_provider('openai', {}, 30)
        self.assertNotIn('local-test-secret',str(caught.exception))
        self.assertNotIn('sensitive data',str(caught.exception))
        self.assertEqual(1,opener.open.call_count)

    def test_preview_never_calls_network_or_prints_key(self):
        out=io.StringIO()
        with patch.dict(os.environ, {'XAI_API_KEY':'local-test-secret'}), patch.object(wb,'call_provider') as mock, contextlib.redirect_stdout(out):
            result=wb.main(['request','evidence-desk','--provider','xai','--model','test-model','--input',str(ROOT/'ai-workbench'/'sample-input.txt')])
        self.assertEqual(0,result)
        mock.assert_not_called()
        self.assertNotIn('local-test-secret',out.getvalue())
        self.assertFalse(json.loads(out.getvalue())['network_called'])

    def test_list_cli(self):
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(0,wb.main(['list']))
        self.assertIn('knowledge-map',out.getvalue())

    def test_missing_input_file_returns_error(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(2,wb.main(['request','evidence-desk','--provider','openai','--model','test','--input','does-not-exist.txt']))


class BrowserBuildTests(unittest.TestCase):
    def test_browser_embeds_reviewed_catalog(self):
        spec = importlib.util.spec_from_file_location('builder', ROOT / 'tools' / 'build_workbench_browser.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        html = builder.build()
        embedded = html.split('<script type="application/json" id="data">', 1)[1].split('</script>', 1)[0]
        self.assertEqual(json.loads(embedded)['cards'], wb.load_catalog())

    def test_browser_has_no_remote_assets(self):
        spec = importlib.util.spec_from_file_location('builder', ROOT / 'tools' / 'build_workbench_browser.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        text = builder.build()
        self.assertNotIn('__WORKBENCH_DATA__', text)
        self.assertNotIn('<script src=', text)
        self.assertNotIn('<link', text)
        self.assertIn('textContent', text)


if __name__ == '__main__':
    unittest.main()
