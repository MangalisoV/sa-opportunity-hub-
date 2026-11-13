import json
import unittest
from pathlib import Path
from unittest.mock import patch
import update

class WebsiteDataTests(unittest.TestCase):
    def test_directory_json(self):
        data=json.loads((Path(__file__).parent/'data/opportunities.json').read_text())
        self.assertIsInstance(data['items'], list)
        for item in data['items']:
            self.assertTrue(item['url'].startswith('https://'))
            self.assertIn(item['category'],update.CATEGORIES)
            self.assertIn(item.get('type'),('directory','information'))
            self.assertTrue(item['title'])
    def test_dpsa_parser(self):
        sample='<a href="/newsroom/psvc/circular-41-of-2026/">Circular 41</a>'
        with patch.object(update,'load',return_value=sample):
            records={}
            update.dpsa(records)
            self.assertEqual(len(records),1)
            self.assertEqual(next(iter(records.values()))['type'],'directory')
    def test_invalid_feeds_ignored(self):
        with patch.dict('os.environ',{'OFFICIAL_FEEDS_JSON':'[{"url":"http://not-secure.example/feed","category":"Jobs"}]'}):
            records={}
            update.feeds(records)
            self.assertEqual(records,{})
if __name__=='__main__':
    unittest.main()
