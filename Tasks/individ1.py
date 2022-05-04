#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
import sys
import logging
from typing import List
import xml.etree.ElementTree as ET


"""
Выполнить индивидуальное задание 2 лабораторной работы 2.19, добавив аннтотации типов.
Выполнить проверку программы с помощью утилиты mypy.
"""

# Класс пользовательского исключения в случае, если введенная
# команда является недопустимой.
class UnknownCommandError(Exception):

    def __init__(self, command, message="Unknown command"):
        self.command = command
        self.message = message
        super(UnknownCommandError, self).__init__(message)

    def __str__(self):
        return f"{self.command} -> {self.message}"


@dataclass(frozen=True)
class Human:
    name: str
    zodiac: str
    year: str


@dataclass
class Staff:
    people: List[Human] = field(default_factory=lambda: [])
    def add(self, name: str, zodiac: str, year: str) -> None:
        self.people.append(
            Human(
                name=name,
                zodiac=zodiac,
                year=year,
            )
        )
        self.people.sort(key=lambda human: human.name)

    def __str__(self) -> str:
        # Заголовок таблицы.
        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        table.append(line)
        table.append(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "No",
                "Ф.И.О.",
                "Знак зодиака",
                "Дата рождения"
            )
        )
        table.append(line)
        # Вывести данные о всех сотрудниках.
        for idx, human in enumerate(self.people, 1):
            table.append(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    human.name,
                    human.zodiac,
                    human.year
                )
            )
        table.append(line)
        return '\n'.join(table)

    def select(self, nom: str) -> List[Human]:
        count = 0
        result: List[Human] = []
        # Проверить сведения людей из списка.
        for i, num in enumerate(self.people, 1):
            if nom == num.name:
                count += 1
                result.append(human)
        return result


    def load(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as fin:
            xml = fin.read()
        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.fromstring(xml, parser=parser)

        self.people = []
        for human_element in tree:
            name, zodiac, year = None, None, None

            for element in human_element:
                if element.tag == 'name':
                    name = element.text
                elif element.tag == 'zodiac':
                    zodiac = element.text
                elif element.tag == 'year':
                    year = element.text

                if name is not None and zodiac is not None \
                        and year is not None:
                    self.people.append(
                        Human(
                            name=name,
                            zodiac=zodiac,
                            year=year
                        )
                    )

    def save(self, filename: str) -> None:
        root = ET.Element('people')
        for human in self.people:
            human_element = ET.Element('human')
            name_element = ET.SubElement(human_element, 'name')
            name_element.text = human.name
            post_element = ET.SubElement(human_element, 'zodiac')
            post_element.text = str(human.zodiac)
            year_element = ET.SubElement(human_element, 'year')
            year_element.text = human.year
            root.append(human_element)
        tree = ET.ElementTree(root)
        with open(filename, "w", encoding="utf-8") as fout:
            tree.write(fout, encoding="utf-8", xml_declaration=True)


if __name__ == '__main__':
    logging.basicConfig(
        filename='people.log',
        level=logging.INFO
    )

    staff = Staff()

    while True:
        try:
            # Запросить команду из терминала.
            command = input(">>> ").lower()
            # Выполнить действие в соответствие с командой.
            if command == 'exit':
                break
            elif command == 'add':
                    # Запросить данные о человеке.
                    name = input("ФИО: ")
                    zodiac = input("Знак зодиака: ")
                    year = input("Дата рождения ")
                    # Добавить человека.
                    staff.add(name, zodiac, year)
                    logging.info(
                    f"Добавлен человек: {name}, {zodiac}, "
                    f"с датой рождения {year}")
            elif command == 'list':
                    # Вывести список.
                    print(staff)
                    logging.info("Список людей.")
            elif command.startswith('select '):
                    parts = command.split(maxsplit=1)
                    # Запросить людей.
                    selected = staff.select()
                    # Вывести результаты запроса.
                    if selected:
                        for idx, human in enumerate(selected, 1):
                            print(
                            '{:>4}: {}'.format(idx, human.name)
                            )
                            logging.info(
                            f"Найдено {len(selected)} людей с "
                            f"данным именем: {parts[1]}."
                            )
                    else:
                        print("Человек с данным именем не найден.")
                        logging.warning(
                        f"Человек с данным именем: {parts[1]}  не найден."
                        )
            elif command.startswith('load '):
                    # Разбить команду на части для имени файла.
                    parts = command.split(maxsplit=1)
                    # Загрузить данные из файла.
                    staff.load(parts[1])
                    logging.info(f"Загружены данные из файла {parts[1]}.")
            elif command.startswith('save '):
                    # Разбить команду на части для имени файла.
                    parts = command.split(maxsplit=1)
                    # Сохранить данные в файл.
                    staff.save(parts[1])
                    logging.info(f"Сохранены данные в файл {parts[1]}.")
            elif command == 'help':
                    # Вывести справку о работе с программой.
                    print("Список команд:\n")
                    print("add - добавить человека;")
                    print("list - вывести список людей;")
                    print("select <1> - запросить человека с заданным именем;")
                    print("load <имя_файла> - загрузить данные из файла;")
                    print("save <имя_файла> - сохранить данные в файл;")
                    print("help - отобразить справку;")
                    print("exit - завершить работу с программой.")
            else:
                    raise UnknownCommandError(command)
        except Exception as exc:
            logging.error(f"Ошибка: {exc}")
            print(exc, file=sys.stderr)