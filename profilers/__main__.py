from vprof import runner
import time
from src.main import up
# def hard():
#     time.sleep(2)
#     return 'ok'

# def lesshard():
#     time.sleep(1)

# def main(a, b):
#     print(hard())
#     lesshard()

runner.run(up, 'cmhp', host='localhost', port=8000)