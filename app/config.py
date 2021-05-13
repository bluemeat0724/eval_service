

class Config:
  JSON_AS_ASCII = False
  JSON_SORT_KEYS = False
  UPLOAD_FOLDER = 'uploads/'
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  @staticmethod
  def init_app(app):
    pass


class DevelopmentConfig(Config):
  DEBUG = True


class TestingConfig(Config):
  TESTING = True
  # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/report'


class ProductionConfig(Config):
    DEBUG = False
  # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:NetC@123@localhost:3306/report'


config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig
          }
