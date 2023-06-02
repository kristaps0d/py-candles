from widgets.database.schemas.products import Products
from widgets.database.cursor import DbCursor

class DeliveredEvent(object):
    def __new__(self, state):
        # debug
        if state == 'passed':
            pass
        
        if state == 'defective':
            print('Action!: IO action, logging!')

class LegacyDeliveredEvent(object):
    def __new__(self, obj, obj_quality, dbCon):
        # add new database entry
        with DbCursor(dbCon) as cur:
            ProductsTable = Products(cur)
            ProductsTable.Insert(obj_quality)
    