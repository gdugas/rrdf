from rrdf.models.fields import DsField, RraField
from django.db import models
import rrdtool


def default_start():
    from datetime import timedelta
    from django.utils import timezone
    delta = timedelta(0, 10)
    start = timezone.now() - delta
    return start


class Rrd(models.Model):
    
    start = models.DateTimeField(default=default_start,
                                 null=True, blank=True)
    step = models.IntegerField(null=True, blank=True, default=300)
    autocreate = models.BooleanField()
    overwrite = models.BooleanField()

    class Meta:
        abstract = True
    
    
    def __init__(self, *args, **kwargs):
        super(Rrd, self).__init__(*args, **kwargs)
        ds = []
        rra = []
        for name in self._meta.get_all_field_names():
            field = self._meta.get_field(name)
            if isinstance(field, DsField):
                ds.append(name)
            elif isinstance(field, RraField):
                rra.append(name)
        self._meta.rrd_ds = ds
        self._meta.rrd_rra = rra
    
    def get_ds_list(self):
        return self._meta.rrd_ds
    
    def get_rra_list(self):
        return self._meta.rrd_rra
    
    def get_rrd_name(self):
        return self._meta.db_table+'_'+str(self.id)+'.rrd'
    
    def get_rrd_path(self):
        from django.conf import settings
        import os
        return os.path.join(settings.RRD_PATH, self.get_rrd_name())
    
    
    def save(self, *args, **kwargs):
        import os
        save = super(Rrd, self).save(*args, **kwargs)
        
        path = self.get_rrd_path()
        pathexists = os.path.exists(path)
        if not pathexists and self.autocreate:
            self.rrdcreate()
        return save
    
    def rrdcreate(self):
        if not self.id:
            return None
        
        cmd = []
        path = self.get_rrd_path()
        cmd.append(str(path))
        
        # options
        cmd.append('--start')
        cmd.append(str(self.start.strftime("%s")))
        cmd.append('--step')
        cmd.append(str(self.step))
        
        if not self.overwrite:
            cmd.append('--no-overwrite')
        
        ds = []
        for name in self.get_ds_list():
            row = getattr(self, name, None)
            if row:
                ds.append(str(row.to_string()))
        cmd.append(ds)
        
        for name in self.get_rra_list():
            row = getattr(self, name, None)
            if row:
                cmd.append(str(row.to_string()))
        
        rrdtool.create(*cmd)

"""
    def drop(self):
    def first(self):
    def create(self):
    def update(self):
    def graph(self):
    def dump(self):
    def restore(self):
    def fetch(self):
    def tune(self):
    def last(self):
    def info(self):
    def xport(self):
    '''

"""
