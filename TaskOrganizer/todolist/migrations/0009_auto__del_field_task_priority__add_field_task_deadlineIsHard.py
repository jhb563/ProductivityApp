# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Task.priority'
        db.delete_column(u'todolist_task', 'priority')

        # Adding field 'Task.deadlineIsHard'
        db.add_column(u'todolist_task', 'deadlineIsHard',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Task.priority'
        db.add_column(u'todolist_task', 'priority',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'Task.deadlineIsHard'
        db.delete_column(u'todolist_task', 'deadlineIsHard')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'todolist.project': {
            'Meta': {'object_name': 'Project'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'#0000FF'", 'max_length': '7'}),
            'date_finished': ('django.db.models.fields.DateTimeField', [], {}),
            'date_started': ('django.db.models.fields.DateTimeField', [], {}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {}),
            'finished': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parentid': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'todolist.task': {
            'Meta': {'object_name': 'Task'},
            'assigned': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_finished': ('django.db.models.fields.DateTimeField', [], {}),
            'date_started': ('django.db.models.fields.DateTimeField', [], {}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {}),
            'deadlineIsHard': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'finished': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent_project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['todolist.Project']", 'null': 'True'}),
            'requiredTasks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['todolist.Task']", 'null': 'True', 'symmetrical': 'False'}),
            'timeAllocation': ('django.db.models.fields.IntegerField', [], {'default': '60'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'todolist.useroptions': {
            'Meta': {'object_name': 'UserOptions'},
            'fridayTime': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mondayTime': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'saturdayTime': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'sundayTime': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'thursdayTime': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'tuesdayTime': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'wednesdayTime': ('django.db.models.fields.IntegerField', [], {'default': '300'})
        }
    }

    complete_apps = ['todolist']