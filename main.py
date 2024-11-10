from functools import wraps
def cache_decorator (cache_depth = 10):
    def decorator(func):
        cache = {}           #словарь для хранения кэш значений
        cache_order = []     #список для отслеживания порядка добавления элементов

        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) == 1 and not kwargs:
                key = args[0]
            else:
                key = (*args, *kwargs.items())

            if key in cache:
                print(f"(Возвращаем значение {cache[key]} из кэша по ключу: {key})")
                return cache[key]

            result = func(*args, **kwargs)

            # удаляем самый старый элемент, если кэш превышает допустимую глубину
            if len(cache_order) >= cache_depth:
                old_key = cache_order.pop(0)
                del cache[old_key]
                print(f"(Превышена глубина кэша. Удаляем из кэша самый старый элемент с ключом: {old_key})")

            cache[key] = result
            cache_order.append(key)

            return result

        return wrapper

    return decorator


if __name__ == '__main__':
    #пример 1: проверка возврата значений из кэша и удаления старых значений при превышении глубины кэша
    @cache_decorator(2)
    def example_1 (a, b):
        return a + b

    print("--------------------------------- тест 1 -------------------------------------")
    print(example_1(2,5))        #вычислили и добавили в кэш
    print(example_1(2,5))        #взяли из кэша
    print(example_1(1, 3))       #вычислили и добавили в кэш
    print(example_1(10, 12))     #кэш переполнен -> удалили (2,5) и добавили в кэш
    print(example_1(2,5))        #кэш переполнен -> удалили (1,3) и добавили в кэш

    #пример 2: проверка работы декоратора для нескольких функций одновременно
    @cache_decorator(3)
    def example_2(a):
        return a * 2

    @cache_decorator(2)
    def example_2_1(a):
        return a ** 2

    print("--------------------------------- тест 2 -------------------------------------")
    print(example_2(4))
    print(example_2_1(4))
    print(example_2(4))
    print(example_2_1(4))
    # кэши функций независимы

    #пример 3: проверка с ключевыми аргументами
    @cache_decorator(3)
    def example_3(a, b, c=1):
        return (a + b) * c

    print("--------------------------------- тест 3 -------------------------------------")
    print(example_3(3,5, 2))
    print(example_3(3, 5))
    print(example_3(6, 3, 3))
    print(example_3(3, 5, 2))
    print(example_3(1,4))