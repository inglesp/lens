# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'contacts_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_book_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'contacts', ['Person'])

        # Adding model 'Address'
        db.create_table(u'contacts_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contacts.Person'])),
            ('Street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('City', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('State', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ZIP', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Country', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lat', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lng', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('latlng_error', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'contacts', ['Address'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'contacts_person')

        # Deleting model 'Address'
        db.delete_table(u'contacts_address')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['contacts']