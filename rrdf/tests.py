from django.utils import unittest


class RrdfTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_datasource_type(self):
        """Datasource type test"""
        from rrdf import Datasource
        
        ds_string = 'DS:test:GAUGE:20:1:1'
        ds1 = Datasource.load_from_string(ds_string)
        ds2 = Datasource("test", "GAUGE", 20, 1, 1)
        self.assertEqual(isinstance(ds1, Datasource), True)
        self.assertEqual(ds1.to_string(), ds_string)
        self.assertEqual(ds2.to_string(), ds_string)
    
    def test_archive_type(self):
        """Archive type test"""
        from rrdf import Archive
        
        rra_string = 'RRA:AVERAGE:0.5:1:24'
        rra1 = Archive.load_from_string(rra_string)
        rra2 = Archive("AVERAGE", 0.5, 1, 24)
        self.assertEqual(isinstance(rra1, Archive), True)
        self.assertEqual(rra1.to_string(), rra_string)
        self.assertEqual(rra2.to_string(), rra_string)

