from setuptools import setup, Extension
from Cython.Build import cythonize


extensions = [
    Extension(
        "engine.order_book",
        ["engine/order_book.pyx"],
    )
]


setup(
    name="chronosmatch-engine",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3"
        },
    ),
)