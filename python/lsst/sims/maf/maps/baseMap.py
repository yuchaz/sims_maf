import inspect

__all__ = ['MapsRegistry', 'BaseMap']

class MapsRegistry(type):
    """
    Meta class for Maps, to build a registry of maps classes.
    """
    def __init__(cls, name, bases, dict):
        super(MapsRegistry, cls).__init__(name, bases, dict)
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        modname = inspect.getmodule(cls).__name__
        if modname.startswith('lsst.sims.maf.maps'):
            modname = ''
        else:
            if len(modname.split('.')) > 1:
                modname = '.'.join(modname.split('.')[:-1]) + '.'
            else:
                modname = modname + '.'
        mapsname = modname + name
        if mapsname in cls.registry:
            raise Exception('Redefining maps %s! (there are >1 maps with the same name)' %(mapsname))
        if mapsname != 'BaseMaps':
            cls.registry[mapsname] = cls

    def getClass(cls, mapsname):
        return cls.registry[mapsname]

    def list(cls, doc=False):
        for mapsname in sorted(cls.registry):
            if not doc:
                print mapsname
            if doc:
                print '---- ', mapsname, ' ----'
                print cls.registry[mapsname].__doc__
                maps = cls.registry[mapsname]()
                print ' added to SlicePoint: ', ','.join(maps.keynames)

class BaseMap(object):
    """ """
    __metaclass__ = MapsRegistry

    def __init__(self,**kwargs):
        self.keyname = 'newkey'

    def run(self,slicePoints):
        """
        Given slicePoints (dict containing metadata about each slicePoint, including ra/dec),
         adds additional metadata at each slicepoint and returns updated dict.
        """
        raise NotImplementedError('This must be defined in subclass')
