import os
import traceback
from time import time

import click

from site_speaker.speech.CrtAdapter import CrtAdapter
from site_speaker.utils.export import export
from site_speaker.utils.files import get_all_files_with_extension, get_base_filename
from site_speaker.utils.parsing import get_posts
from site_speaker.utils.queries import query
from site_speaker.utils.string import stringify_number


@click.group()
def main():
    pass


@main.command()
@click.argument('url', type=str)
@click.option('--output-path', '-o', type=str)
def read(url: str, output_path: str):
    page = query(url, as_html=True)
    posts = get_posts(html=page, class_name='post__text')
    export(output_path=output_path, posts=posts)


@main.command()
@click.argument('url_pattern', type=str)
@click.option('--n_pages', '-n', default=None, type=int)
@click.option('--output-path', '-o', type=str)
def read_many(url_pattern: str, n_pages: int, output_path: str):
    posts = []
    i = 0
    n_new_posts = None
    try:
        while (n_new_posts is None or n_new_posts > 0) and (n_pages is None or i < n_pages):
            start = time()
            page = query(url_pattern.format(i=i), as_html=True)
            new_posts = get_posts(html=page, class_name='post__text')
            n_new_posts = len(new_posts)
            print(f'Handled {stringify_number(i + 1)} page in {time() - start:.3f} seconds (fetched {n_new_posts} new posts)')
            if n_new_posts == 0:
                break
            posts.extend(new_posts)
            i += 1
    except Exception:
        print(f'Oops, an exception occurred:')
        print(traceback.format_exc())

    export(output_path=output_path, posts=posts)


@main.command()
@click.option('--input-path', '-i', type=str)
@click.option('--output-path', '-o', type=str)
def tts(input_path: str, output_path: str):
    adapter = CrtAdapter()
    adapter.generate_audio(input_file_path=input_path, output_file_path=output_path)


@main.command()
@click.option('--input-path', '-i', type=str)
@click.option('--src-extension', '-s', default='txt', type=str)
@click.option('--output-path', '-o', type=str)
@click.option('--dst-extension', '-d', default='mp3', type=str)
def tts_many(input_path: str, output_path: str, src_extension: str, dst_extension: str):
    os.makedirs(output_path, exist_ok=True)
    adapter = CrtAdapter()
    files = get_all_files_with_extension(input_path, src_extension)
    n_files = len(files)
    for i, input_file_path in enumerate(sorted(files)):
        base_input_filename = get_base_filename(input_file_path)
        output_file_path = os.path.join(output_path, f'{base_input_filename}.{dst_extension}')
        adapter.generate_audio(input_file_path=input_file_path, output_file_path=output_file_path)
        print(f'Handled {i + 1} / {n_files} files')


if __name__ == '__main__':
    main()
