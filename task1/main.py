import math
from typing import Union, List


class Rational:
    def __init__(self, numerator=0, denominator=1):
        if isinstance(numerator, str):
            if '/' in numerator:
                n, d = map(int, numerator.split('/'))
            else:
                n, d = int(numerator), 1
        else:
            n, d = numerator, denominator

        if d == 0:
            raise ZeroDivisionError("Знаменник не може бути нулем")

        common_divisor = math.gcd(abs(n), abs(d))
        self.n = n // common_divisor
        self.d = d // common_divisor

        if self.d < 0:
            self.n *= -1
            self.d *= -1

    def __add__(self, other):
        if isinstance(other, int):
            other = Rational(other)
        new_n = self.n * other.d + other.n * self.d
        new_d = self.d * other.d
        return Rational(new_n, new_d)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        return f"{self.n}/{self.d}" if self.d != 1 else f"{self.n}"

    def __repr__(self):
        return f"Rational({self.n}, {self.d})"


class RationalList:
    def __init__(self, data: List[Union[Rational, int]] = None):
        self.data = []
        if data:
            for item in data:
                self.append(item)

    def append(self, item: Union[Rational, int]):
        if isinstance(item, int):
            self.data.append(Rational(item))
        elif isinstance(item, Rational):
            self.data.append(item)
        else:
            raise TypeError("Елемент має бути Rational або int")

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        sorted_data = sorted(
            self.data,
            key=lambda x: (-x.d, -x.n)
        )
        return iter(sorted_data)

    def sum(self):
        total = Rational(0)
        for num in self.data:
            total += num
        return total


def read_numbers_from_file(filename):
    numbers = RationalList()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split()
                for part in parts:
                    try:
                        if '/' in part:
                            numbers.append(Rational(part))
                        else:
                            numbers.append(int(part))
                    except ValueError:
                        print(f"Пропускаємо невірний формат числа: {part}")
    return numbers


def process_files():
    for i in range(1, 4):
        input_file = f"input{i:02d}.txt"
        output_file = f"output{i:02d}.txt"

        try:
            numbers = read_numbers_from_file(input_file)
            total = numbers.sum()

            with open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write(f"Файл {input_file}:\n")
                f_out.write(f"Сума = {total}\n\n")
                f_out.write("Числа у порядку спадання знаменників (і при рівних - чисельників):\n")
                for num in numbers:
                    f_out.write(f"{str(num)}\n")

            print(f"Результати для {input_file} збережено у {output_file}")

        except FileNotFoundError:
            print(f"Файл {input_file} не знайдено, пропускаємо...")


if __name__ == "__main__":
    process_files()
