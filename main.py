from Core_layer.Test_package.PythonTests import TestRun as PyTest
import subprocess

if __name__ == "__main__":
    test = PyTest.TestRun()
    test.run_all_tests()
    subprocess.Popen(['python', 'discord_main.py'])
    subprocess.Popen(['python', 'telegram_main.py'])
