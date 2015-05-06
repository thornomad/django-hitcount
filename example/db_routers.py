class HitCountRouter(object):
    """A router to control all database operations on models in
    the hitcount application"""

    def db_for_read(self, model, **hints):
        "Point all operations on hitcount models to 'mongodb'"
        if model._meta.app_label == 'hitcount':
            return 'mongodb'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on hitcount models to 'mongodb'"
        if model._meta.app_label == 'hitcount':
            return 'mongodb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in hitcount is involved"
        if obj1._meta.app_label == 'hitcount' or obj2._meta.app_label == 'hitcount':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the hitcount app only appears on the 'mongodb' db"
        if db == 'mongodb':
            return model._meta.app_label == 'hitcount'
        elif model._meta.app_label == 'hitcount':
            return False
        return None