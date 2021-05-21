from app import create_app,db
from flask_migrate import Migrate


app = create_app('default')
Migrate(app,db)


def main():
    app.run()

if __name__=='__main__':
    main()