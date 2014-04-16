
from glob import glob
from doit.tools import run_once

def task_getTheZip():
    datazip = 'data.zip'
    return {
        'targets': [datazip],
        'uptodate': [run_once],
        'actions': ['cp ../data.zip %s' % datazip] # would be a 'wget' in a different context
        }


def task_unzip():
    # using glob, because in a real context, multiple zips would be downloaded
    for z in glob('*.zip'):
        folder = z.replace('.zip', '')
        yield {
            'name': folder,
            'targets': [folder],
            'uptodate': [run_once],
            'actions': [' rm -f %s/* ; mkdir -p %s ; (cd %s && unzip ../%s)' % (folder,folder,folder,z) ]
            }
        for f in glob(folder+'/*.txt'):
            future = f + '.future'
            yield {
                'name': future,
                'targets': [future],
                'file_dep': [f],
                'uptodate': [run_once],
                'actions': [""" cat %s | sed 's@this is@this gonna be... wait for it... @g' > %s """ % (f, future) ]
                }

