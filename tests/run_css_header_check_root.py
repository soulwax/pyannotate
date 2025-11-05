from pathlib import Path
import sys

# Ensure src is on sys.path so package imports work when running tests directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# Import after adjusting sys.path; pylint: disable=wrong-import-position
from pyannotate.annotate_headers import process_file  # pylint: disable=wrong-import-position

repo_root = Path('.').resolve()
css_file = Path('tests/sample_files/globals.css')
print('Initial content:')
print(css_file.read_text(encoding='utf-8'))
process_file(css_file, repo_root)
print('\nAfter processing with project_root=repo root:')
print(css_file.read_text(encoding='utf-8'))
