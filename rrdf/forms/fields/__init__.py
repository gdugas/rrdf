from django import forms
from rrdf import Archive, Datasource


class DsField(forms.Field):
    
    def clean(self, value):
        if not isinstance(value, Datasource):
            try:
                ds = Datasource.load_from_string(value)
            except:
                raise forms.ValidationError("Invalid string format")
        else:
            ds = value
        return ds.to_string()
    
    
    def to_python(self, value):
        if isinstance(value, Datasource):
            return Datasource
        try:
            ds = Datasource.load_from_string(value)
            return ds
        except:
            raise forms.ValidationError("Datasource expected")


class RraField(forms.Field):
    
    def clean(self, value):
        if not isinstance(value, Archive):
            try:
                ds = Archive.load_from_string(value)
            except:
                raise forms.ValidationError("Invalid string format")
        else:
            ds = value
        return ds.to_string()
    
    
    def to_python(self, value):
        if isinstance(value, Datasource):
            return Archive
        try:
            ds = Archive.load_from_string(value)
            return ds
        except:
            raise forms.ValidationError("Archive expected")
