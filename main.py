from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def add(self, name, count):
        pass

    @abstractmethod
    def remove(self, name, count):
        pass

    @abstractmethod
    def get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class BaseStorage(Storage):
    def __init__(self, items, capacity):
        self._items = items
        self._capacity = capacity

    def add(self, name, count):
        if self.get_free_space() < count:
            raise Exception("Нет места")
        self._items[name] = self._items.get(name, 0) + count

    def remove(self, name, count):
        if name not in self._items:
            raise Exception("Нет такого объекта")
        if self._items[name] < count:
            raise Exception("Нет места")
        self._items[name] -= count
        if self._items[name] == 0:
            self._items.pop(name)

    def get_free_space(self):
        return self._capacity - sum(self._items.values())

    def get_items(self):
        return self._items

    def get_unique_items_count(self):
        return len(self._items)


class Store(BaseStorage):
    def __init__(self, items, capacity=100):
        super().__init__(items, capacity)


class Shop(BaseStorage):
    def __init__(self, items, capacity=20):
        super().__init__(items, capacity)

    def add(self, name, count):
        if self.get_unique_items_count() >= 5:
            raise Exception("Много разных товаров")

        super().add(name, count)


class Request:
    def __init__(self, request_str, storages):
        request_list = request_str.lower().split(' ')
        if len(request_list) != 7:
            raise Exception("Не верный запрос")
        self.count = int(request_list[1])
        self.product = request_list[2]
        self.from_send = request_list[4]
        self.to_send = request_list[6]

        if self.to_send not in storages or self.from_send not in storages:
            raise Exception("Ошибка отпраки")


class Courier:
    def __init__(self, request: Request, storages):
        self.__request = request
        self.__from = storages[self.__request.from_send]
        self.__to = storages[self.__request.to_send]

    def move(self):
        self.__from.remove(name=self.__request.product, count=self.__request.count)
        print(f'Курьер забрал {self.__request.count} {self.__request.product} из {self.__request.from_send}')
        print(f'Курьер везёт {self.__request.count} {self.__request.product}')
        self.__to.add(name=self.__request.product, count=self.__request.count)
        print(f'Курьер доставил {self.__request.count} {self.__request.product} в {self.__request.to_send}')


store = Store({
    'печенька': 3,
    'ноутбук': 2
})

shop = Shop({
    'печенька': 10,
    'ноутбук': 5
})

storages = {
    'магазин': shop,
    'склад': store
}


def main():
    while True:
        for name, items in storages.items():
            print(f'В {name} храниться:\n')
            its = items.get_items()
            for item in its:
                print(f'{its[item]} {item}')
            print("\n")
        req = input('Введите сообщение типа "Доставить [сколько] [чего] из [откуда] в [куда]"\n'
                    'Пример: "Доставить 3 печенька из склад в магазин"\n'
                    'Напишите stop/стоп - для выхода\n')
        if req.lower() in ['stop', 'стоп']:
            break
        request = Request(req, storages)
        courier = Courier(request, storages)
        courier.move()


if __name__ == "__main__":
    main()
