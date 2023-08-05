from typing import Iterator, Optional, TypeVar

__all__ = [
    'PeekableIterator',
]

T = TypeVar('T')

class PeekableIterator(Iterator[T]):
    _inner: Iterator[T]
    _peeked: Optional[T]

    def __init__(self, inner: Iterator[T]):
        self._inner = inner
        self._peeked = None

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        if self._peeked is not None:
            result = self._peeked
            self._peeked = None
            return result
        return next(self._inner)

    def peek(self) -> Optional[T]:
        if self._peeked is None:
            try:
                self._peeked = next(self._inner)
            except StopIteration:
                self._peeked = None
        return self._peeked
