import atexit
import flet
from app import main
from functions.files_operations import delete_all_files

if __name__ == '__main__':
    flet.app(target=main)
    atexit.register(lambda: delete_all_files('../tmp'))