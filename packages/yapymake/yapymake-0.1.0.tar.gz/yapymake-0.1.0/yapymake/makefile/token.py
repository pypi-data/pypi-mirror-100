from dataclasses import dataclass
from typing import Iterable, Iterator, List, MutableSequence, Optional, Tuple

from .parse_util import *

__all__ = [
    'TokenString',
    'Token',
    'MacroToken',
    'TextToken',
    'tokenize',
]

class TokenString(Iterable['Token']):
    _tokens: MutableSequence['Token']

    def __init__(self, my_tokens: Optional[MutableSequence['Token']] = None):
        if my_tokens is None:
            self._tokens = []
        else:
            self._tokens = my_tokens

    @staticmethod
    def text(body: str) -> 'TokenString':
        return TokenString([TextToken(body)])

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TokenString) and self._tokens == other._tokens

    def __iter__(self) -> Iterator['Token']:
        return iter(self._tokens)

    def __repr__(self) -> str:
        return f'TokenString({repr(self._tokens)})'

    def __str__(self) -> str:
        return ''.join(str(x) for x in self._tokens)

    def split_once(self, delimiter: str) -> Optional[Tuple['TokenString', 'TokenString']]:
        result0: List[Token] = []
        self_iter = iter(self._tokens)
        for t in self_iter:
            if isinstance(t, TextToken) and delimiter in t.text:
                before, after = t.text.split(delimiter, 1)
                result0.append(TextToken(before))
                result1 = [TextToken(after), *self_iter]
                return TokenString(result0), TokenString(result1)
            result0.append(t)
        return None

    def lstrip(self) -> None:
        first_token = self._tokens[0]
        if isinstance(first_token, TextToken):
            first_token.text = first_token.text.lstrip()
        self._tokens[0] = first_token

    def rstrip(self, chars: Optional[str] = None) -> None:
        last_token = self._tokens[-1]
        if isinstance(last_token, TextToken):
            last_token.text = last_token.text.rstrip(chars)
        self._tokens[-1] = last_token

    def endswith(self, pattern: str) -> bool:
        last_token = self._tokens[-1]
        return isinstance(last_token, TextToken) and last_token.text.endswith(pattern)

    def concat(self, other: 'TokenString') -> 'TokenString':
        return TokenString([*self._tokens, *other._tokens])


@dataclass()
class Token:
    pass

@dataclass()
class TextToken(Token):
    text: str

    def __str__(self) -> str:
        return self.text

@dataclass()
class MacroToken(Token):
    name: str
    replacement: Optional[Tuple[TokenString, TokenString]]

    def __str__(self) -> str:
        if self.replacement is None:
            return f'$({self.name})'
        else:
            r1, r2 = self.replacement
            return f'$({self.name}:{r1}={r2})'

macro_name = take_while1(lambda c: c.isalnum() or c in ['.', '_'])

def macro_expansion_body(end: str) -> Parser[MacroToken]:
    subst = preceded(tag(":"), separated_pair(tokens('='), tag('='), tokens(end)))

    def make_token(data: Tuple[str, Optional[Tuple[TokenString, TokenString]]]) -> MacroToken:
        name, replacement = data
        return MacroToken(name, replacement)

    return map_parser(pair(macro_name, opt(subst)), make_token)

def parens_macro_expansion(text: str) -> ParseResult[MacroToken]:
    return delimited(tag('$('), macro_expansion_body(')'), tag(')'))(text)

def braces_macro_expansion(text: str) -> ParseResult[MacroToken]:
    return delimited(tag('${'), macro_expansion_body('}'), tag('}'))(text)

def build_tiny_expansion(name_probably: str) -> Token:
    if name_probably == '$':
        return TextToken('$')
    else:
        return MacroToken(name_probably, None)

def tiny_macro_expansion(text: str) -> ParseResult[Token]:
    return map_parser(preceded(tag('$'), verify(any_char, lambda c: c not in ['(', '{'])), build_tiny_expansion)(text)

def macro_expansion(text: str) -> ParseResult[Token]:
    return alt(tiny_macro_expansion, parens_macro_expansion, braces_macro_expansion)(text)

just_text = map_parser(take_till1(lambda c: c == '$'), TextToken)

def text_until(end: str) -> Parser[TextToken]:
    return map_parser(take_till1(lambda c: c in ['$', end]), TextToken)

def single_token(until: Optional[str] = None) -> Parser[Token]:
    if until is None:
        text = just_text
    else:
        text = text_until(until)
    return alt(text, macro_expansion)

empty_tokens = map_parser(tag(''), lambda _: TokenString.text(''))

def tokens(until: Optional[str] = None) -> Parser[TokenString]:
    return alt(map_parser(many1(single_token(until)), TokenString), empty_tokens)

def full_text_tokens(text: str) -> ParseResult[TokenString]:
    return all_consuming(tokens())(text)

def tokenize(text: str) -> TokenString:
    parsed_result = full_text_tokens(text)
    assert parsed_result is not None
    result, _ = parsed_result
    return result

# TODO handle errors
# TODO test any of this
