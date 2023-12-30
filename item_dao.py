from pydantic import BaseModel, validator

class Item(BaseModel):
    id: int
    nome: str
    price: float

class ItemDAO():
    def __init__(self):
        self.items = {}
    
    def add(self, item: Item):
        self.items[item.id] = item
    
    def find_all(self):
        return [value for key, value in self.items.items()]
    
    def find_one(self, id: int):
        try:
            return self.items[id]
        except KeyError:
            return None
    
    def edit(self, id: int, new_item: Item):
        if self.items.get(id) is None:
            return None
        self.items[id] = new_item
        return self.items[id]

    def remove(self, id: int):
        try:
            self.items.pop(id)
        except KeyError:
            return None


if __name__ == '__main__':
    item1 = Item(id=1, nome='Computer', price=4000.0)
    item2 = Item(id=2, nome='Smartwatch', price=250.0)
    dao = ItemDAO()
    dao.add(item1)
    dao.add(item2)
    print(dao.find_all())
    print(dao.find_one(1))
    print(dao.find_one(2))
    print(dao.find_one(3))
    new_item = Item(id=1, nome='Lenovo', price=4200.0)
    dao.edit(1, new_item)
    print(dao.find_all())
    dao.remove(2)
    print(dao.find_all())
    print(dao.edit(3, new_item))
    print(dao.remove(3))