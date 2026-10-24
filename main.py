def solve():
    while True:
        try:
            user_input = input("Введите число больше 8.0 и меньше 9.0 (не включительно): ");
            number = float(user_input.replace(",", "."));
            if 8.0 < number < 9.0: break;
            else: print("Число должно быть больше 8.0 и меньше 9.0, попробуйте снова");
        except ValueError:
            print("Некорректный ввод, введите число");
    
    decimal_str = str(number).split(".")[1];
    digit_sum = sum(int(d) for d in decimal_str);
    print(f"Сумма цифр после запятой: {digit_sum}");
    
    sequence = [digit_sum];
    current = digit_sum;
    while current != 1:
        if current % 2 != 0: current = 3 * current + 1;
        else: current = current // 2;
        sequence.append(current);
    
    print(f"Последовательность Коллатца: {' -> '.join(str(x) for x in sequence)}");
    
    steps = len(sequence) - 1;
    print(f"Количество шагов для достижения единицы: {steps}");
    
    max_value = max(sequence);
    print(f"Самое большое число в последовательности: {max_value}");

def main() -> None:
    solve();

if __name__ == "__main__":
    main();
