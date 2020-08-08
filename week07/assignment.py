"""
定义“动物”、“猫”、“动物园”三个类，动物类不允许被实例化。

动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，
是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。

猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，猫类继承自动物类。

动物园类要求有“名字”属性和“添加动物”的方法，
“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。
"""


class Animal(object):
    def __init__(self, diet_type, size, temper):
        self.diet_type = diet_type
        self.size = size
        self.temper = temper

    @property
    def is_aggressive(self):
        if (self.size == '大' or self.size == '中')\
                and self.diet_type == '食肉' and self.temper == '凶猛':
            return True
        else:
            return False


class Cat(Animal):
    shout = '喵'

    def __init__(self, name, diet_type, size, temper):
        super().__init__(diet_type, size, temper)
        self.name = name
        self.suitable_as_pet = True


class Zoo(object):
    def __init__(self, name):
        self.name = name

    def add_animal(self, animal_object):
        if hasattr(self, type(animal_object).__name__) is False:
            setattr(self, type(animal_object).__name__, [])
        value_list = getattr(self, type(animal_object).__name__)
        if animal_object not in value_list:
            value_list.append(animal_object)


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = getattr(z, 'Cat')

    cat2 = Cat('英国短毛猫', '食肉', '中', '凶猛')
    z.add_animal(cat2)
    have_cat = getattr(z, 'Cat')
