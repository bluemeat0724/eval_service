from app import create_app,db
from flask_migrate import Migrate


app = create_app('production')
Migrate(app,db)


def main():
    app.run(debug=False)

if __name__=='__main__':
    main()