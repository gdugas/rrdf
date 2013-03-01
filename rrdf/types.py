
class Datasource(object):
    TYPES = ['ABSOLUTE', 'COMPUTE', 'COUNTER', 'DERIVE', 'GAUGE']
    
    class DsTypeException(Exception):
        def __init__(self):
            msg = "Datasource type must be one of these types: "
            msg = msg + ' - '.join(Datasource.TYPES)
            super(Datasource.DsTypeException, self).__init__(msg)
    
    def __init__(self, ds_name, ds_type, *ds_args):
        self.name = ds_name
        self.type = ds_type
        self.args = ds_args
        self.validate()
    
    def validate(self):
        if self.type not in Datasource.TYPES:
            raise Datasource.DsTypeException()
    
    @staticmethod
    def load_from_string(string):
        args = string.split(':')[1:]
        return Datasource(*args)
    
    def to_string(self):
        self.validate()
        args = [str(x) for x in self.args]
        row = ':'.join([str(self.name), self.type] + args) 
        return 'DS:'+row
    
    def __unicode__(self):
        return self.to_string()
    


class Archive(object):
    CFs = ['AVERAGE', 'MIN', 'MAX', 'LAST']
    
    class RraTypeException(Exception):
        def __init__(self):
            msg = "Archive consolidation function must be one of: "
            msg = msg + ' - '.join(Archive.CFs)
            super(Archive.RRaTypeException, self).__init__(msg)
    
    def __init__(self, cf, *cf_args):
        self.cf = cf
        self.args = cf_args
        self.validate()
    
    def validate(self):
        if self.cf not in Archive.CFs:
            raise Archive.RraTypeException()
    
    @staticmethod
    def load_from_string(string):
        args = string.split(':')[1:]
        return Archive(*args)
    
    def to_string(self):
        self.validate()
        args = [str(x) for x in self.args]
        row = ':'.join([self.cf] + args)
        return 'RRA:'+row
    
    def __unicode__(self):
        return self.to_string()

"""
def datasource(ds_name, ds_type, *ds_args):
    return Datasource(ds_name, ds_type, *ds_args)

def absolute(ds_name, heartbeat, vmin, vmax):
    return datasource(ds_name, 'ABSOLUTE', heartbeat, vmin, vmax)
def compute(ds_name, rpn):
    return datasource(ds_name, 'COMPUTE', rpn)
def counter(ds_name, heartbeat, vmin, vmax):
    return datasource(ds_name, 'COUNTER', heartbeat, vmin, vmax)
def derive(ds_name, heartbeat, vmin, vmax):
    return datasource(ds_name, 'DERIVE', heartbeat, vmin, vmax)
def gauge(ds_name, heartbeat, vmin, vmax):
    return datasource(ds_name, 'GAUGE', heartbeat, vmin, vmax)

"""