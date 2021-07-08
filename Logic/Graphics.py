import matplotlib.pyplot as plt
import numpy as np
import os
import random
import string

class Graphics:

    # генерация названия изображения
    @staticmethod
    def _generate_random_string(length=10):
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string

    # создание полного пути
    @staticmethod
    def _get_save_path():
        fig_name = Graphics._generate_random_string()
        save_path = os.getcwd() + '\\' + fig_name + '.png'
        return save_path

    # возвращает полный путь к png, на которой изображена гистограмма
    @staticmethod
    def get_history_histogram(stat, str):
        return Graphics._get_history(stat, str, False)

    # возвращает полный путь к png, на которой изображена гистограмма
    @staticmethod
    def get_history_plot(stat, str):
        return Graphics._get_history(stat, str, True)

    @staticmethod
    def _get_history(stat, str, is_plot):
        x = []
        y = []
        for day, count in stat.items():
            x.append(day[5:])
            y.append(count)
        if is_plot:
            plt.plot(x, y, color='orange')
        else:
            plt.bar(x, y, color='orange')
        plt.title(str, color='darkmagenta')
        plt.xlabel('Дата', color='grey')
        plt.ylabel('Количество', color='grey')
        if not is_plot:
            plt.yticks((np.arange(0, max(y)+1)))
        plt.grid(True)

        save_path = Graphics._get_save_path()
        plt.savefig(save_path)
        plt.close()
        return save_path