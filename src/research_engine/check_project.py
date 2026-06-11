"""Lightweight delivery checklist for LO17 project state."""

import os


def _exists(path):
    return os.path.exists(path)


def main():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    checks = {
        "requirements.txt exists": _exists(os.path.join(base, "requirements.txt")),
        "requirements.txt non-empty": os.path.getsize(os.path.join(base, "requirements.txt")) > 0 if _exists(os.path.join(base, "requirements.txt")) else False,
        "README.md exists": _exists(os.path.join(base, "README.md")),
        "TD1 xml exists": _exists(os.path.join(base, "data", "output", "TD1", "xml.xml")),
        "inverse_title exists": _exists(os.path.join(base, "data", "output", "TD3", "inverse_title.txt")),
        "inverse_text exists": _exists(os.path.join(base, "data", "output", "TD3", "inverse_text.txt")),
        "ground_truth.json exists": _exists(os.path.join(base, "data", "output", "evaluation", "ground_truth.json")),
        "evaluation_results.csv exists": _exists(os.path.join(base, "data", "output", "evaluation", "evaluation_results.csv")),
        "evaluation_results.json exists": _exists(os.path.join(base, "data", "output", "evaluation", "evaluation_results.json")),
    }

    print("LO17 project check")
    print("------------------")
    for label, ok in checks.items():
        print(f"- {label}: {'OK' if ok else 'MISSING'}")

    try:
        from moteur import SearchEngine
        from traitement_requete import process_request
        from evaluation import QUERIES
        from tokenizer import Tokenizer
        from spell_checker import SpellChecker

        td1_xml = os.path.join(base, "data", "output", "TD1", "xml.xml")
        td2_dir = os.path.join(base, "data", "output", "TD2")
        td3_dir = os.path.join(base, "data", "output", "TD3")
        anti_dic = os.path.join(td2_dir, "anti_dic.txt")
        stem = os.path.join(td3_dir, "stem_nltk.txt")

        engine = SearchEngine(index_dir=td3_dir, xml_path=td1_xml)
        tokenizer = Tokenizer(xml_filepath=td1_xml, output_dir=td2_dir)
        stop_words = tokenizer.load_dictionary(anti_dic)
        spell_checker = SpellChecker(lexicon_file=stem)
        structured = process_request(QUERIES[0][1], stemmer=None, spell_checker=spell_checker, stop_words=stop_words)
        results = engine.search(structured)
        print(f"- backend import/search smoke test: OK ({len(results)} result(s))")
    except Exception as exc:
        print(f"- backend import/search smoke test: FAILED ({exc})")


if __name__ == "__main__":
    main()
