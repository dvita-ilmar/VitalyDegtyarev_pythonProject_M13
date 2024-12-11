"""
coding: utf-8
Дегтярев Виталий (группа 22/08)
Домашнее задание №13.1
Домашнее задание по теме "Асинхронность на практике"
"""


import time, asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования')
    for ball in range(1, 5):
        await asyncio.sleep(10/power)
        print(f'Силач {name} поднял {ball}-й шар')
    print(f'Силач {name} закончил соревнования')


async def start_tournament():
    print('Старт соревнований')
    task1 = asyncio.create_task(start_strongman('Добрыня Никитич', 7))
    task2 = asyncio.create_task(start_strongman('Алеша Попович', 5))
    task3 = asyncio.create_task(start_strongman('Илья Муромец', 9))
    await task1
    await task2
    await task3
    print('Финиш соревнований')


# Запуск
asyncio.run(start_tournament())
