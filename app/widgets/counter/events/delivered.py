from widgets.database.schemas.products import Products
from widgets.database.cursor import DbCursor

class DeliveredEvent(object):
    def __new__(self, key):
        # debug
        print(f'{key} delivered')

class LegacyDeliveredEvent(object):
    def __new__(self, obj, obj_quality, dbCon):
        # add new database entry
        with DbCursor(dbCon) as cur:
            ProductsTable = Products(cur)
            ProductsTable.Insert(obj_quality)
    