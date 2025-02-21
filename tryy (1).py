import sys
import time

cnt = 0

while True:
    cnt += 1

    # 커서를 맨 위로 이동 후, 출력
    if cnt > 1:
        sys.stdout.write("\033[F\033[K" * 3)  # 3줄을 지움
    sys.stdout.write(f"Line 1: {cnt}\n")
    sys.stdout.write(f"Line 2: {cnt * 2}\n")
    sys.stdout.write(f"Line 3: {cnt * 3}\n")

    sys.stdout.flush()
    time.sleep(1)
