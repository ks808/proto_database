#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~ Author: Krylov Sergey


class DataBase(object):
    """ Класс прототип базы данных поддерживающий транзакции (в том числе вложенные)
     и хранящий значения в оперативной памяти

    Внешнее взаимодействие осуществляется через передачу строки с параметрами в аргумент метода <input_params>
    экземпляра класса
    """

    def __init__(self):
        """Инициализация переменных экземпляра класса

        """
        self.environment = {}
        self.conditions = []

    def get_last_state(self):
        """Возвращает состояние преведущей транзакции

        :return: dict
        """
        state = {}
        if not len(self.conditions):
            return self.environment

        for i in self.conditions:
            for k, v in i.items():
                if v is None:
                    del state[k]
                else:
                    state[k] = v
        return state

    def fixed_state(self, state):
        """Фиксирует все различия текущего состояния с последним состоянием транзакции

        :param state: dict
        :return:
        """
        _fix = {}
        last_state = self.get_last_state()
        unset = set(last_state) - set(state)
        add = set(state) - set(last_state)
        print('add: {}'.format(add))
        for k, v in last_state.items():
            if k in state:
                if v != state[k]:
                    _fix[k] = state[k]
            elif k in unset:
                _fix[k] = None
            else:
                _fix[k] = v
        if add:
            for i in add:
                _fix[i] = state[i]
        self.conditions.append(_fix)

    def transaction_begin(self):
        """Формирует транзакцию

        :return:
        """
        _begin = {k: v for k, v in self.environment.items()}
        _len = len(self.conditions)

        if not _len:
            self.conditions.append(_begin)
            return 'TRANSACTION BEGIN 1'

        self.fixed_state(_begin)

        return 'TRANSACTION BEGIN'

    def transaction_rollback(self):
        """Откат изменений

        :return:
        """
        if not len(self.conditions):
            return 'NO ACTIVE TRANSACTION'
        self.environment = self.get_last_state()
        self.conditions.pop()

        return 'TRANSACTION ROLLBACK'

    def transaction_commit(self):
        """Комитит изменения

        :return:str
        """
        self.conditions.clear()
        return 'TRANSACTION COMMIT'

    def commands_1_params(self, params):
        """Задает состояние окружения

        :param params: array
        :return: string
        """
        if params[0] == 'BEGIN':
            return self.transaction_begin()
        elif params[0] == 'COMMIT':
            return self.transaction_commit()
        elif params[0] == 'ROLLBACK':
            return self.transaction_rollback()
        return ''

    def commands_2_params(self, params):
        """Определяет обработчик возвращающий значение

        :param params: array
        :return: string
        """
        com, var = params
        if not var:
            return ''
        if com == 'COUNTS':
            return len([r for r in self.environment.values() if r == var])
        elif com == 'GET':
            return self.environment.get(var, 'NULL')
        elif com == 'UNSET':
            message = 'DELETED {}'.format(var)
            del self.environment[var]
            return message

    def commands_3_params(self, params):
        """Устанавливает значение переменной окружения

        :param params:
        :return:
        """
        com, var, arg = params
        if arg == '':
            return ''
        self.environment[var] = arg
        return arg

    def input_params(self, value):
        """Разбивает сроку с входными параметрами и в зависемости от количества параметров вызывает нужный обработчик

        :param value: string
        :return: string
        """
        params = value.split(' ')
        len_args = len(params)

        if len_args == 1:
            return self.commands_1_params(params)
        elif len_args == 2:
            return self.commands_2_params(params)
        elif len_args == 3 and params[0] == 'SET':
            return self.commands_3_params(params)
        else:
            return ''
