import os
from math import ceil, log10

from site_speaker.utils.files import get_extension, write_as_binary, write_as_text
from site_speaker.utils.string import normalize_spaces


def export(output_path: str, posts):
    print(f'Exporting {len(posts)} posts...')
    output_file_extension = get_extension(output_path)
    if output_file_extension == 'pkl':
        write_as_binary(output_path, posts)
    elif output_file_extension == 'txt':
        write_as_text(output_path, '\n'.join(normalize_spaces(post) for post in posts))
    elif output_file_extension is None:
        os.makedirs(output_path, exist_ok=True)
        n_decimal_places_for_post_index = ceil(log10(len(posts)))
        filename_pattern = os.path.join(output_path, f'{{i:0{n_decimal_places_for_post_index}}}.txt')
        for i, post in enumerate(posts):
            file_path = eval(f"f'{filename_pattern}'")
            write_as_text(file_path, post)
