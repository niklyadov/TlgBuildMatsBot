import matplotlib.pyplot as plt
import numpy as np
import os
import random
import string

class Graphics:

    # генерация названия изображения
    @staticmethod
    def generate_random_string(length=10):
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string

    # график количества зарегистрированных пользователей по дням
    @staticmethod
    def graphic_user_history(stat):
        x = []
        y = []
        for day in stat:
            x.append(day.date[:-9])
            y.append(day.count)
        plt.bar(x,y,color='orange')
        plt.title('Статистика количества зарегистрированных пользователей по дням',color='darkmagenta')
        plt.xlabel('Дата',color='grey')
        plt.ylabel('Количество',color='grey')
        plt.grid(True)
        plt.yticks((np.arange(0, max(y)+1)))

        fig_name = Graphics.generate_random_string()
        save_path = os.getcwd()[:-len('\Logic')] + '\Graphics' + '\\' + fig_name
        plt.savefig(save_path)
        return save_path+'.png'

    # график количества запросов пользователей по дням
    @staticmethod
    def graphic_requests_history(stat):
        x = []
        y = []
        for day in stat:
            x.append(day.date[:-9])
            y.append(day.count)
        plt.bar(x, y, color='orange')
        plt.title('Статистика количества запросов пользователей по дням', color='darkmagenta')
        plt.xlabel('Дата', color='grey')
        plt.ylabel('Количество', color='grey')
        plt.grid(True)
        plt.yticks((np.arange(0, max(y) + 1)))

        fig_name = Graphics.generate_random_string()
        save_path = os.getcwd()[:-len('\Logic')] + '\Graphics' + '\\' + fig_name
        plt.savefig(save_path)
        plt.show()
        return save_path + '.png'