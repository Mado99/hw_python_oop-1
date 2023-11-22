class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float, distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return f"Тип тренировки: {self.training_type}; Длительность: {self.duration} ч.; " \
               f"Дистанция: {self.distance} км; Ср. скорость: {self.speed} км/ч; " \
               f"Потрачено ккал: {self.calories}."


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Расчет количества затраченных калорий для бега."""
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) \
               * self.weight / self.M_IN_KM * self.duration


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_STEP_MULTIPLIER_1 = 0.035
    CALORIES_STEP_MULTIPLIER_2 = 0.029

    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет количества затраченных калорий для спортивной ходьбы."""
        return ((self.CALORIES_STEP_MULTIPLIER_1 * self.weight +
                 (self.get_mean_speed() ** 2 / self.height) * self.CALORIES_STEP_MULTIPLIER_2 * self.weight)
                * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_POOL = 25
    COUNT_POOL = 40

    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP = 1.38

    def get_spent_calories(self) -> float:
        """Расчет количества затраченных калорий для плавания."""
        return (self.get_mean_speed() + 1.1) * 2 * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        action, duration, weight, length_pool, count_pool = data
        return Swimming(action, duration, weight, length_pool, count_pool)
    elif workout_type == 'RUN':
        action, duration, weight = data
        return Running(action, duration, weight)
    elif workout_type =='WLK':
        action, duration, weight, height = data
        return SportsWalking(action, duration, weight, height)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    
    data = [1000, 60, 70, 25, 40] 
    workout_type = 'SWM'
    workout = read_package(workout_type, data)
    main(workout)

