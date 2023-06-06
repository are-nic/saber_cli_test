"""
Usage:
    app.py list builds [--dir=<directory>]
    app.py list tasks [--dir=<directory>]
    app.py get build <build_name> [--dir=<directory>]
    app.py get task <task_name> [--dir=<directory>]
    app.py (-h | --help)
    app.py --version

Options:
    -h --help           Дополнительные параметры:
    --version           Показать версию
    --dir=<directory>   изменить директорию YAML файлов [default: .]

"""
import os
import yaml
from docopt import docopt


class BuildSystem:
    def __init__(self, tasks_file, builds_file):
        """
        :param tasks_file: файл задач
        :param builds_file: файл билдов
        """
        try:
            self.tasks = self.__get_yaml_data(tasks_file)['tasks']
            self.builds = self.__get_yaml_data(builds_file)['builds']
        except TypeError as e:
            print("Ошибка обработки данные в файлах YAML. Проверьте правильность данных")
            print(str(e))
            exit(1)
        except KeyError as e:
            print(f"Ошибка обработки данные в файлах YAML. В файле нет данных по ключу {e}")
            exit(1)

    @staticmethod
    def __get_yaml_data(file):
        """
        получить данные файла yaml
        :param file: путь к файлу
        """
        try:
            with open(file) as f:
                yaml_data = yaml.safe_load(f)
            return yaml_data
        except FileNotFoundError:
            print(f"Файл '{file}' не найден")
            exit(1)
        except yaml.YAMLError as e:
            print(f"Ошибка обработки данные в '{file}': {str(e)}")
            exit(1)

    def list_builds_or_tasks(self, type_data='builds'):
        """
        вывести список имен всех задач или билдов
        :param type_data: тип сущности для вывода - билд или задача ("build" or "task")
        """
        if type_data == 'tasks':
            objects = self.tasks
        else:
            objects = self.builds

        print(f"List of available {type_data}:")
        for obj in objects:
            print(f" * {obj['name']}")

    def get_task(self, task_name, just_dependencies=False):
        """
        получить имя задачи и ее зависимости
        :param task_name: имя запрашиваемой задачи
        :param just_dependencies: флаг для возврата только списка зависимостей и самой задачи
        :return: список зависимостей задачи, который включает и саму задачу в следующем порядке - [зависимость, задача]
        """
        for task in self.tasks:
            try:
                if task_name in task['name']:

                    if just_dependencies:
                        return list(task['dependencies'])

                    print(f"Task info:")
                    print(f" * name: {task_name}")
                    print(f" * dependencies: {', '.join(task['dependencies'])}")
                    return

            except KeyError as e:
                print(f"Ошибка обработки данные в файлах YAML. В файле нет данных по ключу {e} у задачи '{task_name}'")
                exit(1)
        print(f"Задача '{task_name}' не существует")

    def __get_build_tasks_list(self, tasks, build_tasks_list):
        """ получаем список задач и их зависимостей для конкретного билда """

        if len(tasks) == 0:     # базовый случай рекурсии
            return

        for task_name in tasks:
            task_dependencies = self.get_task(task_name, True)

            self.__get_build_tasks_list(task_dependencies, build_tasks_list)

            build_tasks_list.append(task_name)
        return build_tasks_list

    def get_build(self, build_name):
        """ получить билд и его задачи """
        for build in self.builds:
            try:
                if build_name in build['name']:
                    print(f"Build info:")
                    print(f" * name: {build_name}")
                    task_list = self.__get_build_tasks_list(build['tasks'], [])
                    print(f" * tasks: {', '.join(task_list)}")
                    return
            except KeyError as e:
                print(f"Ошибка обработки данные в файлах YAML. В файле нет данных по ключу {e} у билда '{build_name}'")
                exit(1)
        print(f"Билд '{build_name}' не существует")


if __name__ == '__main__':
    arguments = docopt(__doc__, version='CLI utility for build system v1.0')

    directory = arguments['--dir']
    tasks_file = os.path.join(directory, 'tasks.yaml')
    builds_file = os.path.join(directory, 'builds.yaml')

    build_system = BuildSystem(tasks_file, builds_file)

    if arguments['list'] and arguments['builds']:
        build_system.list_builds_or_tasks('builds')

    elif arguments['list'] and arguments['tasks']:
        build_system.list_builds_or_tasks('tasks')

    elif arguments['get'] and arguments['build']:
        build_name = arguments['<build_name>']
        build_system.get_build(build_name)

    elif arguments['get'] and arguments['task']:
        task_name = arguments['<task_name>']
        build_system.get_task(task_name)
