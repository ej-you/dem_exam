from app.app import Application


def main():
    app = Application()
    app.show_auth_window()
    app.start()


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print("FATAL:", str(err))
