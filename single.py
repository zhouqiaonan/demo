# # class Singleton(object):
# #     def foo(self):
# #         pass
# #
# # singleton = Singleton()
#
#
# def Singleton(cls):
#     _instance = {}
#
#     def _singleton(*args, **kwargs):
#         if cls not in _instance:
#             _instance[cls] = cls(*args, **kwargs)
#         return _instance[cls]
#
#     return _singleton
#
#
# @Singleton
# class A(object):
#     a = 1
#
#     def __init__(self, x=0):
#         self.x = x
#
#
# a1 = A(1)
# a2 = A(2)
# print(a1.x)
# print(a2.x)
import ctypes
# class Singleton(object):
#
#     def __init__(self):
#         import time
#         time.sleep(1)
#
#     @classmethod
#     def instance(cls, *args, **kwargs):
#         if not hasattr(cls, '_instance'):
#             Singleton._instance = Singleton(*args, **kwargs)
#         return Singleton._instance
#
#
# import threading
#
# def task(arg):
#     obj = Singleton.instance()
#     print(obj)
#
#
# for i in range(10):
#     t = threading.Thread(target=task, args=(i,))
#     t.start()


# import time
# import threading
# class Singleton(object):
#     _instance_lock = threading.Lock()
#
#     def __init__(self):
#         time.sleep(1)
#
#     @classmethod
#     def instance(cls, *args, **kwargs):
#         if not hasattr(Singleton, "_instance"):
#             with cls._instance_lock:
#                 if not hasattr(cls, '_instance'):
#                     Singleton._instance = Singleton(*args, **kwargs)
#         return Singleton._instance
#
#
# def task(arg):
#     obj = Singleton.instance()
#     print(obj)
#
#
# for i in range(10):
#     t = threading.Thread(target=task, args=(i,))
#     t.start()
#
# time.sleep(12)
# obj = Singleton.instance()
# print(obj)


# import threading
#
#
# class Singleton(object):
#     _instance_lock = threading.Lock()
#
#     def __init__(self):
#         pass
#
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(Singleton, '_instance'):
#             with Singleton._instance_lock:
#                 if not hasattr(Singleton, '_instance'):
#                     Singleton._instance = object.__new__(cls)
#         return Singleton._instance
#
#
# obj1 = Singleton()
# obj2 = Singleton()
# print(obj1)
# print(obj2)
#
# def task(arg):
#     obj = Singleton()
#     print(obj)
#
#
# for i in range(10):
#     t = threading.Thread(target=task, args=[i,])
#     t.start()


# class Foo:
#     def __init__(self):
#         pass
#
#     def __call__(self, *args, **kwargs):
#         pass
#
#
# obj  = Foo()
# obj()


# class SingletonType(type):
#     def __init__(self, *args, **kwargs):
#         super(SingletonType, self).__init__(*args, **kwargs)
#
#     def __call__(cls, *args, **kwargs):
#         print(f"cls: {cls}")
#         obj = cls.__new__(cls, *args, **kwargs)
#         cls.__init__(obj, *args, **kwargs)
#         return obj
#
#
# class Foo(metaclass=SingletonType):
#     def __init__(self, name):
#         self.name = name
#
#     def __new__(cls, *args, **kwargs):
#         return object.__new__(cls)
#
#
# obj = Foo("foo")
# print(type(obj))
# print(obj.name)


# double_func = lambda s: s*2
# res = map(double_func, [1,2,3,4,5,6])
# print(list(res))


# mode2 = lambda x: x % 2
# res = filter(mode2, range(10))
# print(list(res))
#
# lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# res1 = all(lst)
# print(res1)
# res2 = any(lst)
# print(res2)


# import multiprocessing
#
# def func(num):
#     num[2] = 9999
#
#
# if __name__ == '__main__':
#     num = multiprocessing.Array("i", [1, 2, 3, 4, 5])
#     print(num)
#
#     p = multiprocessing.Process(target=func, args=(num,))
#     p.start()
#     p.join()
#     print(num[:])


# from multiprocessing import Pool, Manager
#
#
# def func(my_list, my_dict):
#     my_list.append(10)
#     my_list.append(11)
#     my_dict["a"] = 1
#     my_dict["b"] = 2
#
#
# if __name__ == '__main__':
#     manager = Manager()
#     my_list = manager.list()
#     my_dict = manager.dict()
#
#     pool = Pool(processes=2)
#     for i in range(2):
#         pool.apply_async(func=func, args=(my_list, my_dict))
#     pool.close()
#     pool.join()
#
#     print(my_list)
#     print(my_dict)


# class Stack(object):
#
#     def __init__(self):
#         self.__items = []
#
#     def push(self, item):
#         self.__items.append(item)
#
#     def pop(self):
#         return self.__items.pop()
#
#     def peek(self):
#         return self.__items[len(self.__items)-1]
#
#     def size(self):
#         return len(self.__items)
#
#     def is_empty(self):
#         return len(self.__items) == 0
#
#
# if __name__ == '__main__':
#     stack = Stack()
#     stack.push(1)
#     stack.push(2)
#     stack.push(3)
#     stack.push(4)
#     stack.push(5)
#     tmp = stack.pop()
#     print(tmp)
#     print(stack)
#     print(stack.peek())
#     print(stack.size())
#     print(stack.is_empty())


# class Queue(object):
#     def __init__(self):
#         self.queue = []
#
#     def push(self, item):
#         self.queue.append(item)
#
#     def pop(self):
#         return self.queue.pop(0)
#
#     def is_empty(self):
#         return len(self.queue) == 0
#
#     def size(self):
#         return len(self.queue)
#
# if __name__ == '__main__':
#     q = Queue()
#     q.push(1)
#     q.push(2)
#     q.push(3)
#     q.push(4)
#     q.push(5)
#     print(q.pop())
#     print(q.pop())
#     print(q.pop())
#     print(q.size())
#     print(q.is_empty())


class Deque(object):
    def __init__(self):
        self.items = []

    def add_front(self, item):
        self.items.insert(0, item)

    def add_rear(self, item):
        self.items.append(item)

    def remove_front(self):
        return self.items.pop(0)

    def remove_rear(self):
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def print_items(self):
        print(self.items)


if __name__ == '__main__':
    deq = Deque()
    deq.print_items()
    deq.add_front(1)
    deq.add_front(2)
    deq.add_front(3)
    deq.add_rear(8)
    deq.add_rear(9)
    deq.add_rear(10)

    deq.print_items()
    print("================")
    print(deq.remove_front())
    print(deq.remove_rear())
    print("================")
    print(deq.is_empty())
    print(deq.size())
    print("================")
    deq.print_items()


