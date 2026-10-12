import copy, json, subprocess, sys, tempfile, unittest, os
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = json.load(open(os.path.join(HERE, 'events.json')))

def run(data):
    f = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False); json.dump(data, f); f.close()
    return subprocess.run([sys.executable, os.path.join(HERE, 'validate.py'), f.name], capture_output=True, text=True)

class ValidatorTests(unittest.TestCase):
    def test_current_feed_is_valid(self):
        self.assertEqual(run(BASE).returncode, 0)
    def mutate(self, **changes):
        d = copy.deepcopy(BASE); d['events'][0].update(changes); return run(d)
    def test_rejects_bad_status(self): self.assertEqual(self.mutate(st='maybe').returncode, 1)
    def test_rejects_bad_date(self): self.assertEqual(self.mutate(d=['13-40']).returncode, 1)
    def test_rejects_http_link(self): self.assertEqual(self.mutate(ap='http://x.com').returncode, 1)
    def test_rejects_non_numeric_miles(self): self.assertEqual(self.mutate(mi='close').returncode, 1)
    def test_rejects_duplicate_ids(self):
        d = copy.deepcopy(BASE); d['events'].append(copy.deepcopy(d['events'][0])); self.assertEqual(run(d).returncode, 1)
    def test_rejects_feed_that_lost_most_events(self):
        d = copy.deepcopy(BASE); d['events'] = d['events'][:5]; self.assertEqual(run(d).returncode, 1)
if __name__ == '__main__': unittest.main()
