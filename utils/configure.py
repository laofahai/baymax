# coding: utf-8
import configparser


class Configure:

    config = None

    debug = None

    @staticmethod
    def init():
        if Configure.config is None:
            Configure.config = configparser.ConfigParser()
            Configure.config.read("data/config.conf")

    @staticmethod
    def get(group, key):
        Configure.init()

        return Configure.config.get(group, key)


Configure.debug = Configure.get("core", "debug")
