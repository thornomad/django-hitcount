VERSION = (0, 2, 0, 'beta', 1)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    else:
        if VERSION[3] != 'final':
            version = '%s %s' % (version, VERSION[3])
    return version

__version__ = get_version()
