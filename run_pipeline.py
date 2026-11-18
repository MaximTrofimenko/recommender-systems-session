"""Запуск всего проекта на CSV-файлах того же формата."""

import argparse
import os
from pathlib import Path

import nbformat
from nbclient import NotebookClient


project_dir = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--data', type=Path, default=project_dir / 'data')
parser.add_argument('--output', type=Path, default=project_dir / 'sz_result.ipynb')
args = parser.parse_args()

data_dir = args.data.resolve()
for name in ('ratings.csv', 'books.csv', 'tags.csv', 'book_tags.csv'):
    if not (data_dir / name).is_file():
        parser.error(f'Не найден файл: {data_dir / name}')

os.environ['BOOK_DATA_DIR'] = str(data_dir)
notebook = nbformat.read(project_dir / 'sz.ipynb', as_version=4)
client = NotebookClient(
    notebook, timeout=1200, kernel_name='python3',
    resources={'metadata': {'path': str(project_dir)}},
)
client.execute()
nbformat.write(notebook, args.output)
print(f'Готово: {args.output.resolve()}')
