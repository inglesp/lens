# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.organization'
        db.add_column(u'contacts_person', 'organization',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Person.organization'
        db.delete_column(u'contacts_person', 'organization')


    models = {
        u'contacts.address': {
            'City': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'Address'},
            'State': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ZIP': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'latlng_error': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lng': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contacts.Person']"})
        },
        u'contacts.person': {
            'Meta': {'object_name': 'Person'},
            'address_book_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }

    complete_apps = ['contacts']