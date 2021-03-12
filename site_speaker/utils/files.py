import os
import pickle


def get_extension(path: str):
    path_components = path.split('.')
    if len(path_components) > 1:
        return path_components[-1]
    else:
        return None


def replace_extension(path: str, extension: str):
    path_components = path.split('.')
    if len(path_components) > 1:
        return '.'.join((*path_components[:-1], extension))
    else:
        raise ValueError('No extension!')


def write_as_binary(path: str, contents):
    with open(path, 'wb') as file:
        pickle.dump(contents, file)


def write_as_text(path: str, contents):
    with open(path, 'w') as file:
        file.write(contents)


def read_as_text(path: str):
    with open(path, 'r') as file:
        return file.read()


def get_all_files_with_extension(folder: str, extension: str):
    return tuple(
        map(
            # Get full path to the files
            lambda filename: os.path.join(folder, filename),
            filter(
                # Skip not-docx files
                lambda filename: os.path.splitext(filename)[-1] == f'.{extension}',
                os.listdir(folder)
            )
        )
    )


def get_base_filename(filename):
    return ".".join(str(filename).split("/")[-1].split(".")[:-1])
