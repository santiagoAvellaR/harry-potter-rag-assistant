"""Hand-calculated cases, independent of PDFs, embeddings and system output."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from metrics import score_question, summarize, page_pair


def ref(p):
    return {'source': 'book.pdf', 'page': p}


def need(*routes):
    return {'any_of': [{'all_of': [ref(p) for p in route]} for route in routes]}


class MetricsTest(unittest.TestCase):
    def test_duplicate_pages_keep_rank(self):
        m = score_question([ref(9), ref(1), ref(1), ref(2)], [ref(1), ref(2)],
                           {'needs': [need([1]), need([2])]}, ks=[1, 3, 5, 12])
        self.assertEqual(m['mrr'], 1/2)
        self.assertEqual(m['hit@1'], 0)
        self.assertEqual(m['hit@3'], 1)
        self.assertEqual(m['recall@3'], 1/2)
        self.assertEqual(m['recall@5'], 1)
        self.assertEqual(m['need_coverage@3'], 1/2)
        self.assertEqual(m['all_needs@3'], 0)
        self.assertEqual(m['all_needs@12'], 1)

    def test_alternative_and_complementary_bundle(self):
        a = {'needs': [need([1, 2], [3]), need([4])]}
        m = score_question([ref(1), ref(4), ref(3)], [ref(1), ref(2), ref(4)], a, [1, 2, 3])
        self.assertEqual(m['recall@3'], 2/3)
        self.assertEqual(m['need_coverage@1'], 0)  # incomplete two-page route
        self.assertEqual(m['need_coverage@2'], 1/2)
        self.assertEqual(m['need_coverage@3'], 1)
        self.assertEqual(m['all_needs@3'], 1)

    def test_alternative_outside_flat_gold(self):
        m = score_question([ref(2)], [ref(1)], {'needs': [need([1], [2])]}, [1])
        self.assertEqual(m['hit@1'], 0)
        self.assertEqual(m['mrr'], 0)
        self.assertEqual(m['need_coverage@1'], 1)

    def test_context_and_shared_support(self):
        m = score_question([ref(1)], [ref(1), ref(2)],
                           {'needs': [need([1]), need([1])], 'context_only': [ref(2)]}, [1])
        self.assertEqual(m['recall@1'], 1/2)
        self.assertEqual(m['all_needs@1'], 1)

    def test_missing_ranked_reference_is_miss_not_rank_removal(self):
        m = score_question([{}, ref(1)], [ref(1)], {'needs': [need([1])]}, [1, 3])
        self.assertEqual(m['mrr'], 1/2)
        self.assertEqual(m['hit@1'], 0)
        self.assertEqual(m['hit@3'], 1)

    def test_empty_retrieval(self):
        m = score_question([], [ref(1)], {'needs': [need([1])]}, [1, 12])
        self.assertTrue(all(v == 0 for v in m.values()))

    def test_invalid_labels_fail(self):
        for gold, a in [([], {'needs': [need([1])]}), ([{}], {'needs': [need([1])]}),
                        ([ref(1)], {'needs': []}), ([ref(1)], {'needs': [need([])]}),
                        ([ref(1)], {'needs': [{'any_of': [{'all_of': [{}]}]}]})]:
            with self.assertRaises(ValueError):
                score_question([], gold, a)

    def test_source_normalization_and_page_types(self):
        self.assertEqual(page_pair({'source': '/a/book.pdf', 'page': 1}), ('book.pdf', 1))
        for p in [-1, True, '1', None]:
            self.assertIsNone(page_pair({'source': 'book.pdf', 'page': p}))

    def test_macro_mean_and_bootstrap(self):
        # Two equally weighted questions: bootstrap means 0, 0.5 and 1.
        r = summarize([{'mrr': 0}, {'mrr': 1}], samples=10000, seed=42)
        self.assertEqual(r['n'], 2)
        self.assertEqual(r['metrics']['mrr'], {'mean': .5, 'ci95': [0., 1.]})
        self.assertEqual(r, summarize([{'mrr': 0}, {'mrr': 1}], seed=42))
        self.assertEqual(summarize([{'mrr': .25}])['metrics']['mrr']['ci95'], [.25, .25])
        self.assertEqual(summarize([]), {'n': 0, 'metrics': {}})


if __name__ == '__main__':
    unittest.main()
