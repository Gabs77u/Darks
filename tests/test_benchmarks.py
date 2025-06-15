import time


def test_sleep_benchmark(benchmark):
    def sleeper():
        time.sleep(0.01)

    benchmark(sleeper)
