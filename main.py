from collections import Counter

filename = "server.log"
log_counts = Counter()


def analyzeLog():
    log_counts = Counter()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split("|")
                #
                if len(parts) >= 2:
                    level = parts[1].strip()
                    log_counts[level] += 1

        print("Analysis result:")
        for level, count in log_counts.items():
            print(f"{level}: {count}")

    except FileNotFoundError:
        print("There's no LOG file")


def main():
    print("Hello from test-project!")
    analyzeLog()


if __name__ == "__main__":
    main()
