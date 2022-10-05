from django.apps import apps
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.fields import Field
from the_system.locks import lock_object, release_object_lock





"""
If you do something with the database in AppConfig.ready(), 
then during test runs it runs against the production db as it happens before django knows it's testing.
I don't think there's any way to change this, but it should be documented.



https://docs.djangoproject.com/en/1.11/topics/testing/tools/#provided-test-case-classes
"""
 
from django.test.utils import override_settings    
@override_settings(   )
class TestModelMeta(TestCase):
        multi_db = True
        databases = {'default', 'pci'}
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------   
        @classmethod
        def setUpTestData(cls):
            pass      


    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------        
        def setUp(self):
            self.app_name= self.__module__.split('.')[0]

        
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def tearDown(self):
            # Clean up run after every test method.
            pass
 
   
    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_lock_basic(self):
            sample_object = "test_lock_basic"
            self.assertTrue(lock_object(sample_object, lock_duration=10))
 
            self.assertFalse(lock_object(sample_object, lock_duration=10))

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_lock_basic_002(self):
            sample_object = "test_lock_basic_002"
            self.assertTrue(lock_object(sample_object, lock_duration=10))
            self.assertFalse(lock_object(sample_object, lock_duration=10))
            release_object_lock(sample_object)
            self.assertTrue(lock_object(sample_object, lock_duration=10))

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
        def test_lock_basic_003(self):
            sample_object = "test_lock_basic_003"
            self.assertTrue(lock_object(sample_object,extra_id="SOMTHING", lock_duration=60))
            self.assertFalse(lock_object(sample_object,extra_id="SOMTHING", lock_duration=60))
            
            # release lock without extra id
            release_object_lock(sample_object)

            # lock should still be there
            self.assertFalse(lock_object(sample_object,extra_id="SOMTHING", lock_duration=60))

            # release the final lock
            release_object_lock(sample_object,extra_id="SOMTHING")
            self.assertTrue(lock_object(sample_object,extra_id="SOMTHING", lock_duration=10))