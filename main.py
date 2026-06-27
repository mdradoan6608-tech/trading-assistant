import os
import time

APP_NAME = "Trading Assistant"

def main():
    print("=" * 40)
    print(f"{APP_NAME} is starting...")
    print("Running on Railway Cloud")
    print("=" * 40)

    while True:
        print("Trading Assistant is alive...")
        time.sleep(60)

if __name__ == "__main__":
    main()
