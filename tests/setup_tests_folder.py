import os


def setup_tests_folder():
    """
    Создаёт папку 'tests', если её нет в текущей рабочей директории.
    """
    tests_folder = os.path.join(os.getcwd(), "tests")
    if not os.path.exists(tests_folder):
        os.makedirs(tests_folder)
        print(f"Папка 'tests' была успешно создана в {os.getcwd()}.")
    else:
        print(f"Папка 'tests' уже существует в {os.getcwd()}.")


# Вызываем функцию для создания папки
setup_tests_folder()
