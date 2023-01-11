import abc
import base64
import funPIL as df
import io
import base64
from PIL import Image, ImageDraw

class File(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, name, mode):
        pass
    @abc.abstractmethod
    def read(self):
        pass
    @abc.abstractmethod
    def write(self):
        pass

class Record(File):
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
        self.file = open(self.name, self.mode)
    def read(self):
        return self.file.read()
    def write(self, content):
        self.file.write(content)

class Img(File):
    def __init__(self, name, mode = 'r'):
        self.name = name
        self.mode = mode
        self.file = open(self.name, mode=mode)
        self.image = Image.open(io.BytesIO(base64.b64decode(self.data.read()))).convert('RGBA')
    def read(self, name, mode='r'):
        self.file = open(name,mode=mode)
        self.image = Image.open(io.BytesIO(base64.b64decode(self.file.read()))).convert('RGBA')
    def write(self, content, mode='w'):
        self.file = open(self.name, mode=mode)
        self.file.write(base64.b64encode(content))
    def resize(self, size):
        self.image, _ = df.resize(self.image, *size)
        return self.image