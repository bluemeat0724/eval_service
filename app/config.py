import os

class Config:
  JSON_AS_ASCII = False
  JSON_SORT_KEYS = False
  UPLOAD_FOLDER = 'uploads/'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  REPORTS_FOLDER = 'reportsfolder/'

  @staticmethod
  def init_app(app):
    pass


class DevelopmentConfig(Config):
      DEBUG = True
      SQLALCHEMY_DATABASE_URI = os.getenv('DATA_BASE')


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/report'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://ryan:Rjy1958113@rm-uf68r3ut1z0eao1ezko.mysql.rds.aliyuncs.com:3306/questionnaire'


config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig
          }
