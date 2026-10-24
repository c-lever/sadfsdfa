def solve_1():
    import csv;
    import json;
    import os;

    folder = "input_data";
    extensions = {};
    fractional = [];
    nonnegative_integers = [];
    negative_integers = [];

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename);
        if os.path.isfile(path):
            extension = os.path.splitext(filename)[1].lower();
            extensions[extension] = extensions.get(extension, 0) + 1;

    print("Расширения файлов и их количество:");
    for extension, count in sorted(extensions.items()): print(f"{extension or '[без расширения]'}: {count}");

    def add_number(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)): return;
        if value != value: return;
        if value % 1 != 0: fractional.append(value);
        elif value >= 0: nonnegative_integers.append(int(value));
        else: negative_integers.append(int(value));

    def process_json_value(value):
        if isinstance(value, dict):
            for item in value.values(): process_json_value(item);
        elif isinstance(value, list):
            for item in value: process_json_value(item);
        else: add_number(value);

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename);
        extension = os.path.splitext(filename)[1].lower();
        if not os.path.isfile(path) or filename == "numbers.json": continue;

        if extension == ".txt":
            with open(path, "r", encoding="utf-8") as file:
                for token in file.read().replace(",", " ").replace(";", " ").split():
                    try:
                        add_number(float(token));
                    except ValueError:
                        continue;

        elif extension == ".csv":
            with open(path, "r", encoding="utf-8-sig", newline="") as file:
                for row in csv.reader(file, delimiter="?"):
                    for token in row:
                        token = token.strip();
                        if token:
                            try:
                                add_number(float(token));
                            except ValueError:
                                continue;

        elif extension == ".json":
            with open(path, "r", encoding="utf-8") as file:
                process_json_value(json.load(file));

    groups = [
        ("дробные", fractional),
        ("целые неотрицательные", nonnegative_integers),
        ("целые отрицательные", negative_integers),
    ];

    result = [];
    for number_type, numbers in groups:
        item = {
            "type": number_type,
            "sum": sum(numbers),
            "max": max(numbers) if numbers else None,
            "min": min(numbers) if numbers else None,
            "count": len(numbers),
        };
        result.append(item);

    output = json.dumps(result, ensure_ascii=False, indent=2);
    print(output);

    with open("numbers.json", "w", encoding="utf-8") as file:
        file.write(output);

def solve_2():
    import pandas;
    import requests;

    response = requests.get("https://jsonplaceholder.typicode.com/posts");
    response.raise_for_status();
    df = pandas.DataFrame(response.json());

    print("Количество постов у каждого пользователя:");
    for user_id, count in df.groupby("userId").size().items(): print(f"{user_id} - {count}");

    df["post_length"] = df["body"].str.len();
    print(f"\nСредняя длина поста: {df['post_length'].mean()}");

    stats = df.groupby("userId")["post_length"].agg(["mean", "max", "min"]);
    stats = stats.rename(columns={"mean": "средняя", "max": "максимальная", "min": "минимальная"});
    print("\nДлина постов для каждого пользователя:");
    print(stats);

    matching_posts = df[df["body"].str.contains("aspernatur", case=False, na=False)];
    print("\nПосты со словом 'aspernatur':");
    print(matching_posts[["userId", "id", "title", "body"]]);

def main() -> None:
    solve_1();
    solve_2();

if __name__ == "__main__":
    main();
