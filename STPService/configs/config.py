# config.py

# 数据库配置
class Config:
    MYSQL_HOST= 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'TPMStore'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'XXXX'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST,
                                                                             MYSQL_PORT, MYSQL_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20

    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = "XXXX"
    MAIL_PASSWORD = "XXXX"
    MAIL_DEFAULT_SENDER = "XXXXX"


class ProductmentConfig():
    ENV = 'PROD'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'TPMStore'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'XXXX'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST,
                                                                             MYSQL_PORT, MYSQL_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = "3226204545@qq.com"
    MAIL_PASSWORD = "XXXX"
    MAIL_DEFAULT_SENDER = "3226204545@qq.com"
    DEBUG = True
    LOG_PATH = '../prod_main.log'


class DevelopmentConfig():
    ENV = "DEV"
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'TPMStore'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '!QAZ1qaz199510'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST,
                                                                             MYSQL_PORT, MYSQL_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = "3226204545@qq.com"
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = "3226204545@qq.com"
    DEBUG = True
    LOG_PATH = '../dev_main.log'


map_config={
    'product':'ProductmentConfig',
    'develop':'DevelopmentConfig'
}