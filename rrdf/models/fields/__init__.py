from django.db import models
from django.core.exceptions import ValidationError
from rrdf import Archive, Datasource
from rrdf import forms

class DsField(models.Field):
    
    description = 'Rrd Datasource field (DS:ds-name:DST:dst args)'
    
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        if 'default' in kwargs and isinstance(kwargs['default'],
                                              (list, tuple)):
            default = kwargs['default']
            kwargs['default'] = lambda: Datasource(*default)
        
        super(DsField, self).__init__(*args, **kwargs)
    
    
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.DsField}
        defaults.update(kwargs)
        return super(DsField, self).formfield(**defaults)
    
    
    def to_python(self, value):
        # null value
        if not value:
            return value
        
        # datasource object
        elif isinstance(value, Datasource):
            value.name = self.name
            return value
        
        # else: loading datasource from string or raise exception
        else:
            try:
                ds = Datasource.load_from_string(value)
                ds.name = self.name
            except:
                raise ValidationError
            return ds

    def get_internal_type(self):
        return 'CharField'

    def get_prep_value(self, ds):
        if not isinstance(ds, Datasource):
            raise ValueError('Datasource object excepted')
        ds.name = self.name
        return ds.to_string()
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)



class RraField(models.Field):
    
    description = 'RRA:CF:cf arguments'
    
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        if 'default' in kwargs and isinstance(kwargs['default'],
                                              (list, tuple)):
            default = kwargs['default']
            kwargs['default'] = lambda: Archive(*default)
        
        super(RraField, self).__init__(*args, **kwargs)
    
    
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.RraField}
        defaults.update(kwargs)
        return super(RraField, self).formfield(**defaults)
    
    
    def to_python(self, value):
        # null value
        if not value:
            return value
        
        # datasource object
        elif isinstance(value, Archive):
            return value
        
        # else: loading archive from string or raise exception
        else:
            try:
                ds = Archive.load_from_string(value)
            except:
                raise ValidationError
            return ds

    def get_internal_type(self):
        return 'CharField'

    def get_prep_value(self, ds):
        if not isinstance(ds, Archive):
            raise ValueError('Archive object excepted')
        return ds.to_string()
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
