from shutil import make_archive

def zip_folder(fname, archive_from, archive_to):
    print(f'Zipping folder - {archive_from}')
    response = make_archive(
        base_name=fname,
        format='zip',
        base_dir=archive_from,
        root_dir=archive_to
    )
    print(f'Done making archive.')
    return response