import random
import json
from datetime import datetime, timedelta


def generate_logs(num_lines=200):
    start_time = datetime(2024, 5, 1, 10, 0, 0)
    lines = []

    # Định nghĩa các kịch bản log giống hệt mẫu bạn cung cấp
    scenarios = [
        # (LEVEL, SERVICE, MESSAGE, METADATA_GENERATOR)
        (
            "INFO",
            "[auth-service]",
            "User login successful",
            lambda: {
                "user_id": random.randint(100, 199),
                "ip": f"192.168.1.{random.randint(2, 254)}",
            },
        ),
        (
            "DEBUG",
            "[payment-service]",
            "Processing transaction",
            lambda: {"amount": random.choice([500, 1200, 2340, 3000, 450])},
        ),
        (
            "ERROR",
            "[payment-service]",
            "Connection timeout",
            lambda: {
                "user_id": random.randint(100, 199),
                "retry": random.randint(1, 3),
            },
        ),
        (
            "INFO",
            "[auth-service]",
            "Token refreshed",
            lambda: {"user_id": random.randint(100, 199)},
        ),
        (
            "WARN",
            "[risk-engine]",
            "High latency detected",
            lambda: {"latency_ms": random.randint(1000, 5000)},
        ),
        (
            "ERROR",
            "[payment-service]",
            "Insufficient Funds",
            lambda: {
                "user_id": random.randint(100, 199),
                "balance": round(random.uniform(0.5, 50.0), 2),
            },
        ),
    ]

    req_counter = 1
    current_time = start_time

    for _ in range(num_lines):
        # 5% cơ hội sinh ra dòng log rác (Broken line) để test tool
        if random.random() < 0.05:
            garbage_id = random.randint(10000, 99999)
            lines.append(f"BROKEN_LINE_GARBAGE_DATA_{garbage_id}")
            continue

        # Tăng thời gian ngẫu nhiên 1-3 giây mỗi dòng
        current_time += timedelta(seconds=random.randint(1, 3))
        timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # Chọn ngẫu nhiên 1 kịch bản
        level, service, msg, meta_func = random.choice(scenarios)
        meta_json = json.dumps(meta_func())

        # Format: [TIMESTAMP] | LEVEL | [SERVICE] | REQ_ID | MSG | JSON
        line = f"[{timestamp_str}] | {level} | {service} | req-{req_counter:03d} | {msg} | {meta_json}"
        lines.append(line)

        req_counter += 1

    return lines


if __name__ == "__main__":
    logs = generate_logs(200)

    # Ghi ra file server.log
    with open("server2.log", "w", encoding="utf-8") as f:
        f.write("\n".join(logs))

    print(f"Đã tạo thành công {len(logs)} dòng log vào file 'server.log'.")
