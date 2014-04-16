
from glob import glob
from doit.tools import run_once

def task_getTheZip():
    d = 'data.zip'
    return {
        'targets': [d],
        'uptodate': [run_once],
        'actions': ['cp ../data.zip %s' % d]
        }


def task_unzip():
    for z in glob('*.zip'):
        d = z.replace('.zip', '')
        yield {
            'name': d,
            'targets': [d],
            'uptodate': [run_once],
            'actions': [' mkdir -p %s ; (cd %s && unzip ../%s)' % (d,d,z) ]
            }
        for f in glob(d+'/*.txt'):
            rep = f + '.future'
            yield {
                'name': rep,
                'targets': [rep],
                'file_dep': [f],
                'uptodate': [run_once],
                'actions': [""" cat %s | sed 's@This is@This gonna be@g' > %s """ % (f, rep) ]
                
                }

