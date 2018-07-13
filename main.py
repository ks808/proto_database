#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~ Author: Krylov Sergey

from core import DataBase


def main_loop():
    """Главный цикл событий

    :return:
    """
    EOF = 0
    db = DataBase()
    while True:
        n = input('>>')
        if n == 'ENV':
            # Вывод содержимого словоря текущего окружения
            print(db.environment)
            continue
        if n == 'STATE':
            # Вывод соржимого словоря хранящего состояния окружений при транзакциях
            print(db.conditions)
            continue
        if n == '':
            if EOF != 2:
                EOF += 1
                continue
        else:
            EOF = 0

        if n == 'END' or EOF == 2:
            break
        # Передача строки параметров к базе и сохранение возвращаемого значения
        result = db.input_params(n)
        if not result:
            print('WARNING: INCORRECT INPUT')
            continue
        print(result)


if __name__ == '__main__':
    main_loop()
