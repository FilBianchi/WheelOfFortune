import functools
import datetime
import logging

from PySide6.QtCore import QXmlStreamWriter, QFile, QDir, QIODevice, Signal


class XmlHandler(logging.Handler):

    def __init__(self):
        super().__init__()

        old_logs = QDir().entryList(["log_*.log"], QDir.Filter.Files)

        if len(old_logs) >= 20:
            QDir().remove(old_logs[0])

        filename = datetime.datetime.now().strftime('log_%Y_%m_%d_%H_%M_%S.log')
        self.__file = QFile(filename)
        self.__file.open(QIODevice.OpenModeFlag.WriteOnly)
        self.__xml_write = QXmlStreamWriter()
        self.__xml_write.setDevice(self.__file)
        self.__xml_write.writeStartDocument()

    def close(self) -> None:
        self.__xml_write.writeEndDocument()
        logging.Handler.close(self)

    def emit(self, record: logging.LogRecord) -> None:

        if hasattr(record, "type"):
            t = record.type
        else:
            t = "MESSAGE"
        self.__xml_write.writeStartElement(t)
        self.__xml_write.writeAttribute("time", record.asctime)
        self.__xml_write.writeAttribute("thread", record.threadName)
        self.__xml_write.writeAttribute("thread_id", str(record.thread))
        self.__xml_write.writeAttribute("name", record.name)
        if hasattr(record, "obj_id"):
            self.__xml_write.writeAttribute("obj_id", str(record.obj_id))
        if hasattr(record, "nesting_level"):
            self.__xml_write.writeAttribute("nesting_level", str(record.nesting_level))
        self.__xml_write.writeAttribute("level", record.levelname)
        self.__xml_write.writeCharacters(record.message)
        self.__xml_write.writeEndElement()


def init_logging(level=logging.DEBUG):

    str_formatter_str = "%(asctime)s\t%(threadName)s(%(thread)s)\t%(name)s(%(obj_id)s)\t%(nesting_level)s\t%(" \
                        "levelname)s:\t%(type)s\t%(message)s"
    str_formatter = logging.Formatter(str_formatter_str, defaults={"obj_id": "None",
                                                                   "type": "MSG",
                                                                   "nesting_level": ""})

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(str_formatter)

    file_handler = XmlHandler()

    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(level)

    # sys.excepthook = ObjectLogger.log_exception


class ObjectLogger:
    exception_logger = logging.getLogger("Exception")
    log_stack = []
    nested_call = 0

    class CustomAdapter(logging.LoggerAdapter):

        def process(self, msg, kwargs):
            if "extra" in kwargs:
                kwargs["extra"].update(self.extra)
            else:
                kwargs["extra"] = dict(self.extra)
            if "nesting_level" not in kwargs["extra"]:
                kwargs["extra"]["nesting_level"] = ObjectLogger.nested_call
            return msg, kwargs

    def __init__(self):
        super().__init__()

        logger_hinstance = logging.getLogger("{}.{}".format(self.__class__.__module__,
                                                            self.__class__.__name__))

        self._logger = ObjectLogger.CustomAdapter(logger_hinstance, {"obj_id": hex(id(self))})
        self._logger.debug("Instance created")

    def __del__(self):
        self._logger.debug("Instance deleted")

    @staticmethod
    def log_exception(exc_type: type, value, tb):
        ObjectLogger.exception_logger.warning("\tN.A.\t{}: {} -> {}".format(exc_type.__name__, value, str(tb.tb_frame)))

    @staticmethod
    def log(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if hasattr(self, "_logger"):
                s = "{}(".format(func.__name__)
                for i in range(0, len(args)):
                    s += "{}: {}".format(func.__code__.co_varnames[i + 1], args[i])
                    if i < len(args) - 1:
                        s += "; "
                s += ")"
                self._logger.debug(s, extra={"type": "CALL", "nesting_level": ObjectLogger.nested_call})
                ObjectLogger.nested_call += 1
                ret = "Exception"
                try:
                    ret = func(self, *args, **kwargs)
                except Exception as e:
                    raise
                finally:
                    ObjectLogger.nested_call -= 1
                    s += " -> " + str(ret)
                    self._logger.debug(s, extra={"type": "RETURN", "nesting_level": ObjectLogger.nested_call})
            else:
                ret = func(self, *args, **kwargs)
            return ret

        return wrapper

    def f(self):
        pass

    def __init_subclass__(cls, **kwargs):
        for attr, value in cls.__dict__.items():
            if callable(value):
                if type(value) == type(cls.f):
                    if not (attr.startswith("__") and attr.endswith("__")):
                        if hasattr(cls, "log_discard"):
                            if attr not in getattr(cls, "log_discard"):
                                add_attribute = True
                        else:
                            add_attribute = True
