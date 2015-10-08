import muffin


app = application = muffin.Application('example', CONFIG='example.config.debug')


muffin.import_submodules(__name__)
