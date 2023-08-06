"""
Implementa um meta singleton.
"""

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Sempre que chamado.
        """

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]
