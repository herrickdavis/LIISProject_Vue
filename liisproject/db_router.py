class LiisRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'liis':
            return 'liis_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'liis':
            return 'liis_db'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # La aplicación 'liis' no se migra en ninguna base de datos
        # porque sus tablas ya existen.
        if app_label == 'liis':
            return False
        
        # Las aplicaciones internas de Django se migran solo en la base de datos 'default'
        return db == 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Permite relaciones entre modelos de la misma base de datos
        if obj1._meta.app_label == 'liis' and obj2._meta.app_label == 'liis':
            return True
        elif obj1._meta.app_label != 'liis' and obj2._meta.app_label != 'liis':
            return True
        return None