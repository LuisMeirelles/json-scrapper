import importlib
import inspect
import os

from AutomationInstance import AutomationInstance


def get_automation_instances(directory) -> dict[str, type[AutomationInstance]]:
    classes = {}

    for file in os.listdir(directory):
        if file.endswith(".py") and file != f'{__name__}.py':
            module_name = file[:-3]

            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, AutomationInstance) and obj is not AutomationInstance:
                    classes[name] = obj

    return classes


if __name__ == '__main__':
    automation_instances = get_automation_instances('.')

    for instance in automation_instances.values():
        instance.run()
