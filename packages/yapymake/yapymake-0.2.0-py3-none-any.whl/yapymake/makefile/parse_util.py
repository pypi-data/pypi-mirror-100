from typing import Callable, List, Optional, Tuple, TypeVar

__all__ = [
    'ParseResult',
    'Parser',
    'alt',
    'tag',
    'take_till1',
    'take_while1',
    'any_char',
    'all_consuming',
    'map_parser',
    'opt',
    'verify',
    'many1',
    'delimited',
    'pair',
    'preceded',
    'separated_pair',
]

# I had a really nice (well, not really, but it worked) implementation of this with Rust's `nom`,
# but then I surrendered to the borrow checker, so now I have to redo that work in a more Pythonic
# way. So I'm reimplementing the nom pieces I used in Python, because fuck it.

T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')

ParseResult = Optional[Tuple[T, str]]
Parser = Callable[[str], ParseResult[T]]

def alt(*parsers: Parser[T]) -> Parser[T]:
    def parse(text: str) -> ParseResult[T]:
        for parser in parsers[:-1]:
            result = parser(text)
            if result is not None:
                return result
        return parsers[-1](text)
    return parse

def tag(tag_text: str) -> Parser[None]:
    def parse(text: str) -> ParseResult[None]:
        if text.startswith(tag_text):
            return None, text[len(tag_text):]
        return None
    return parse

def take_while1(predicate: Callable[[str], bool]) -> Parser[str]:
    def parse(text: str) -> ParseResult[str]:
        if len(text) == 0 or not predicate(text[0]):
            return None
        for i in range(1, len(text)):
            if not predicate(text[i]):
                return text[:i], text[i:]
        return text, ""
    return parse

def take_till1(predicate: Callable[[str], bool]) -> Parser[str]:
    return take_while1(lambda x: not predicate(x))

def any_char(text: str) -> ParseResult[str]:
    if len(text) > 0:
        return text[0], text[1:]
    return None

def all_consuming(parser: Parser[T]) -> Parser[T]:
    def parse(text: str) -> ParseResult[T]:
        parsed_result = parser(text)
        if parsed_result is None:
            return None
        result, extra = parsed_result
        if len(extra) > 0:
            return None
        return result, ''
    return parse

def map_parser(parser: Parser[T1], mapper: Callable[[T1], T2]) -> Parser[T2]:
    def parse(text: str) -> ParseResult[T2]:
        parsed_result = parser(text)
        if parsed_result is None:
            return None
        result, extra = parsed_result
        return mapper(result), extra
    return parse

def opt(parser: Parser[T]) -> Parser[Optional[T]]:
    def parse(text: str) -> ParseResult[Optional[T]]:
        result = parser(text)
        if result is None:
            return None, text
        return result
    return parse

def verify(parser: Parser[T], predicate: Callable[[T], bool]) -> Parser[T]:
    def parse(text: str) -> ParseResult[T]:
        parsed_result = parser(text)
        if parsed_result is None:
            return None
        result, extra = parsed_result
        if predicate(result):
            return result, extra
        return None
    return parse

def many1(parser: Parser[T]) -> Parser[List[T]]:
    def parse(text: str) -> ParseResult[List[T]]:
        parser_result = parser(text)
        if parser_result is None:
            return None
        this_result, extra = parser_result
        result = [this_result]

        parser_result = parser(extra)
        while parser_result is not None:
            this_result, extra = parser_result
            result.append(this_result)
            parser_result = parser(extra)
        return result, extra
    return parse

def delimited(before_parser: Parser[T1], parser: Parser[T], after_parser: Parser[T2]) -> Parser[T]:
    def parse(text: str) -> ParseResult[T]:
        before_result = before_parser(text)
        if before_result is None:
            return None
        _, extra = before_result

        parsed_result = parser(extra)
        if parsed_result is None:
            return None
        result, extra = parsed_result

        after_result = after_parser(extra)
        if after_result is None:
            return None
        _, extra = after_result

        return result, extra
    return parse

def pair(first_parser: Parser[T1], second_parser: Parser[T2]) -> Parser[Tuple[T1, T2]]:
    def parse(text: str) -> ParseResult[Tuple[T1, T2]]:
        first_parsed_result = first_parser(text)
        if first_parsed_result is None:
            return None
        first_result, extra = first_parsed_result

        second_parsed_result = second_parser(extra)
        if second_parsed_result is None:
            return None
        second_result, extra = second_parsed_result

        return (first_result, second_result), extra
    return parse

def preceded(before_parser: Parser[T1], parser: Parser[T]) -> Parser[T]:
    def parse(text: str) -> ParseResult[T]:
        before_result = before_parser(text)
        if before_result is None:
            return None
        _, extra = before_result

        parsed_result = parser(extra)
        if parsed_result is None:
            return None
        result, extra = parsed_result

        return result, extra
    return parse

def separated_pair(first_parser: Parser[T1], between_parser: Parser[T], second_parser: Parser[T2]) -> Parser[Tuple[T1, T2]]:
    def parse(text: str) -> ParseResult[Tuple[T1, T2]]:
        first_parsed_result = first_parser(text)
        if first_parsed_result is None:
            return None
        first_result, extra = first_parsed_result

        between_result = between_parser(extra)
        if between_result is None:
            return None
        _, extra = between_result

        second_parsed_result = second_parser(extra)
        if second_parsed_result is None:
            return None
        second_result, extra = second_parsed_result

        return (first_result, second_result), extra
    return parse
