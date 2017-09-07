class XpathUtil:

    def __init__(self):
        pass

    #==fc== xpath for class???
    @staticmethod
    def xpath_for_class(classname):
        return "*[contains(concat(' ', @class, ' '), ' " + classname + " ')]"
