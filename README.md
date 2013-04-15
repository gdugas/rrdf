rrdf is a django application which provide models and form abstraction layers.

# Types

from rrdf.types

## Archive (cf, *cf_args):  
- cf (consolidation function): AVERAGE | MIN | MAX | LAST
- cf_args: depend of cf - visit the [rrdtool website](http://oss.oetiker.ch/rrdtool/) for more info

## Datasource (ds_name, ds_type, *ds_args):  
- ds_name: datasource name
- ds_type: ABSOLUTE | COMPUTE | COUNTER | DERIVE | GAUGE
- ds_args: depend of type - visit the [rrdtool website](http://oss.oetiker.ch/rrdtool/) for more info

# Model

## Properties rrdf.models.RrdModel
- **start**: DateTimeField (default=now-10, null=True, blank=True)  
  Rrd start date

- **step**: IntegerField (default=300, null=True, blank=True)  
  Rrd step

- **autocreate**: BooleanField  
  Auto create rrd if not exist

- **overwrite**: BooleanField  
  Overwrite rrd if exist when calling create method

## Methods
- **save**: if autocreate set and rrd does not exist, the save method will autocreate the rrd in path defined by get_rrd_path
- **get_ds_list**: get list of ds fields
- **get_rra_list**: get list of rra fields
- **get_rrd_name**: return the rrd file name
- **get_rrd_path**: return the rrd file path including name
- **rrd_create**: create the rrd in path returned by get_rrd_path. If rrd already exist and overwrite property is defined, the rrd will be overwrited
- **rrd_drop**: delete the rrd
- **rrd_first**
- **rrd_info**
- **rrd_last**
- **rrd_update**
- **rrd_bulk_update**

## Fields 

### rrdf.models.DsField ()  
Represent a rrd datasource: must be set with the Datasource object

### rrdf.models.RraField  
Represent a rrd archive: must be set with the Archive object
