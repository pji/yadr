"""
common
~~~~~~

Common classes for testing.
"""
import unittest as ut

from yadr import lex
from yadr import maps
from yadr import model as m


# Base test case.
class BaseTests:
    class LexTestCase(ut.TestCase):
        def setUp(self):
            self.lexer = lex.Lexer()

        def tearDown(self):
            self.lexer = None

        def lex_test(self, exp, data):
            """Run a basic test on yadr.lex.lex."""
            act = self.lexer.lex(data)
            self.assertTupleEqual(exp, act)

    class LexTokenTestCase(ut.TestCase):
        token = m.Token.START
        allowed = []
        tokens = [
            m.Token.AS_OPERATOR,
            m.Token.BOOLEAN,
            m.Token.CHOICE_OPERATOR,
            m.Token.CHOICE_OPTIONS,
            m.Token.COMPARISON_OPERATOR,
            m.Token.DICE_OPERATOR,
            m.Token.EX_OPERATOR,
            m.Token.GROUP_OPEN,
            m.Token.GROUP_CLOSE,
            m.Token.MAP,
            m.Token.MAP_END,
            m.Token.MAPPING_OPERATOR,
            m.Token.MD_OPERATOR,
            m.Token.MEMBER,
            m.Token.MEMBER_DELIMITER,
            m.Token.NEGATIVE_SIGN,
            m.Token.NUMBER,
            m.Token.OPERATOR,
            m.Token.OPTIONS_OPERATOR,
            m.Token.POOL,
            m.Token.POOL_CLOSE,
            m.Token.POOL_DEGEN_OPERATOR,
            m.Token.POOL_END,
            m.Token.POOL_GEN_OPERATOR,
            m.Token.POOL_OPEN,
            m.Token.POOL_OPERATOR,
            m.Token.QUALIFIER,
            m.Token.QUALIFIER_END,
            m.Token.QUALIFIER_DELIMITER,
            m.Token.ROLL_DELIMITER,
            m.Token.U_POOL_DEGEN_OPERATOR,
        ]
        symbols_raw = m.yadn_symbols_raw

        # To test for what is allowed, the YADN sent must be legal. Some
        # of the tokens that need to be tested cannot be the end of a roll.
        # Some cannot be at the start. This provides a standard suffix that
        # can be added after the token to make the test valid YADN. Tokens
        # that have empty tuples don't need to have anything following them.
        # Those that contain just a string and an empty tuple of tokens are
        # are symbols that are part of a complex syntax that results in a
        # single token, like pools.
        example_after = {
            m.Token.AS_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.BOOLEAN: ('', ()),
            m.Token.CHOICE_OPERATOR: (
                '"spam":"eggs"',
                (
                    (m.Token.QUALIFIER, 'spam'),
                    (m.Token.OPTIONS_OPERATOR, ':'),
                    (m.Token.QUALIFIER, 'eggs'),
                ),
            ),
            m.Token.COMPARISON_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.DICE_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.EX_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.GROUP_OPEN: (
                '3+3)',
                (
                    (m.Token.NUMBER, 3),
                    (m.Token.AS_OPERATOR, '+'),
                    (m.Token.NUMBER, 3),
                    (m.Token.GROUP_CLOSE, ')'),
                ),
            ),
            m.Token.GROUP_CLOSE: ('', ()),
            m.Token.MAP: ('', ()),
            m.Token.MAP_CLOSE: ('', ()),
            m.Token.MAP_END: ('', ()),
            m.Token.MAP_OPEN: ('}', ((m.Token.MAP, ('', {})),)),
            m.Token.MAPPING_OPERATOR: (
                '"spam"',
                ((m.Token.QUALIFIER, 'spam'), )
            ),
            m.Token.MD_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.MEMBER_DELIMITER: ('3]', ()),
            m.Token.NEGATIVE_SIGN: ('3', ((m.Token.NUMBER, -3), )),
            m.Token.NUMBER: ('', ()),
            m.Token.OPTIONS_OPERATOR: (
                '"eggs"',
                ((m.Token.QUALIFIER, 'eggs'), )
            ),
            m.Token.POOL_CLOSE: ('', ()),
            m.Token.POOL: ('', ()),
            m.Token.POOL_END: ('', ()),
            m.Token.POOL_OPEN: ('3,3]', ((m.Token.POOL, (3, 3)), )),
            m.Token.POOL_DEGEN_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.POOL_GEN_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.POOL_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.QUALIFIER: ('', ()),
            m.Token.QUALIFIER_DELIMITER: ('spam"', ()),
            m.Token.QUALIFIER_END: ('', ()),
            m.Token.ROLL_DELIMITER: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.U_POOL_DEGEN_OPERATOR: (
                '[3,3]',
                ((m.Token.POOL, (3, 3)), )
            ),
        }
        example_before = {
            m.Token.AS_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.BOOLEAN: ('', ()),
            m.Token.CHOICE_OPERATOR: ('T', ((m.Token.BOOLEAN, True), )),
            m.Token.COMPARISON_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.DICE_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.EX_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.GROUP_OPEN: ('', ()),
            m.Token.GROUP_CLOSE: (
                '(3+3',
                (
                    (m.Token.GROUP_OPEN, '('),
                    (m.Token.NUMBER, 3),
                    (m.Token.AS_OPERATOR, '+'),
                    (m.Token.NUMBER, 3),
                ),
            ),
            m.Token.MAP: ('', ()),
            m.Token.MAP_CLOSE: ('{', ((m.Token.MAP, ('', {})), )),
            m.Token.MAP_END: ('{}', ((m.Token.MAP, ('', {})), )),
            m.Token.MAP_OPEN: ('', ()),
            m.Token.MAPPING_OPERATOR: (
                '3',
                ((m.Token.NUMBER, 3), )
            ),
            m.Token.MD_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.MEMBER_DELIMITER: ('[3', ()),
            m.Token.NEGATIVE_SIGN: ('', ()),
            m.Token.NUMBER: ('', ()),
            m.Token.OPTIONS_OPERATOR: (
                '"spam"',
                ((m.Token.QUALIFIER, 'spam'), )
            ),
            m.Token.POOL_CLOSE: ('[3,3', ()),
            m.Token.POOL: ('', ()),
            m.Token.POOL_END: ('[3,3]', ((m.Token.POOL, (3, 3)), )),
            m.Token.POOL_OPEN: ('', ()),
            m.Token.POOL_DEGEN_OPERATOR: ('[3,3]', ((m.Token.POOL, (3, 3)), )),
            m.Token.POOL_GEN_OPERATOR: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.POOL_OPERATOR: ('[3,3]', ((m.Token.POOL, (3, 3)), )),
            m.Token.QUALIFIER: ('', ()),
            m.Token.QUALIFIER_DELIMITER: ('', ()),
            m.Token.QUALIFIER_END: ('"spam"', ((m.Token.QUALIFIER, 'spam'), )),
            m.Token.ROLL_DELIMITER: ('3', ((m.Token.NUMBER, 3), )),
            m.Token.U_POOL_DEGEN_OPERATOR: ('', ()),
        }

        def setUp(self):
            self.lexer = lex.Lexer()

        def tearDown(self):
            self.lexer = None

        def lex_test(self, exp, data):
            """Run a basic test on yadr.lex.lex."""
            act = self.lexer.lex(data)
            self.assertTupleEqual(exp, act)

        def get_symbol_for_token(self, token):
            symbols = self.symbols_raw[token]
            symbol = ''
            if symbols:
                symbol = symbols[0]
                if token.name == "NUMBER":
                    symbol = int(symbol)
            else:
                if token.name == 'MAP':
                    symbol = (
                        'name',
                        {
                            1: 'none',
                            2: 'success',
                            3: 'success',
                            4: 'success success',
                        }
                    )
                if token.name == "POOL":
                    symbol = (3, 3)
                if token.name == "QUALIFIER":
                    symbol = 'spam'
                if token.name == "CHOICE_OPTIONS":
                    symbol = ('spam', 'eggs')
            return symbol

        def get_token_for_name(self, name):
            for token in self.tokens:
                if token.name == name:
                    return token

        def get_example(self, token, before=True):
            # Pick which dictionary you are getting the test code and
            # expected values from.
            example_dict = self.example_before
            if not before:
                example_dict = self.example_after

            # Look up the token being tested in the relevant dictionary.
            # Get the test code and expected results for that token.
            # Then get the symbol for the token being tested and build
            # a token for it to add into the expected results.
            test, exp = example_dict[token]
            symbol = self.get_symbol_for_token(token)
            token_info = (token, symbol)

            # Handle complicated tokens where the needed test information
            # couldn't fit into the dictionary well.
            if token.name == "BOOLEAN":
                token_info = (token, True)
            elif token.name == "QUALIFIER_DELIMITER":
                new_token = self.get_token_for_name('QUALIFIER')
                token_info = (new_token, 'spam')
            if token.name == "QUALIFIER":
                symbol = f'"{symbol}"'
            elif token.name == "MAP":
                symbol = (
                    '{"name"=1:"none",2:"success",3:"success"'
                    ',4:"success success"}'
                )
            elif token.name == "POOL":
                symbol = str(symbol)
                symbol = f'[{symbol[1:-1]}]'

            # Add the symbol and token being tested into the code and
            # the expected results. The order they are placed in depends
            # on whether we are looking at the code that comes before
            # the token or after.
            if before and token.name == 'NEGATIVE_SIGN':
                test = f'{test}{symbol}'
            elif before:
                exp = (*exp, token_info)
                test = f'{test}{symbol}'
            elif not before and token.name in ["NEGATIVE_SIGN",
                                               "POOL_OPEN",
                                               "MAP_OPEN",]:
                test = f'{symbol}{test}'
            else:
                exp = (token_info, *exp)
                test = f'{symbol}{test}'
            return exp, test

        def allowed_test(self, state_token, test_token):
            # Expected data and setup.
            b_exp, b_test = self.get_example(state_token)
            a_exp, a_test = self.get_example(test_token, False)

            # Expected value.
            exp = (*b_exp, *a_exp)

            # Test data and state.
            yadn = f'{b_test}{a_test}'
            yadn_ws = f'{b_test} {a_test}'

            # Run test and determine result.
            try:
                self.lex_test(exp, yadn)
            except Exception as ex:
                msg = f'{yadn} failed.'
                raise ex.__class__(msg) from ex
            try:
                if "WHITESPACE" in [t.name for t in self.allowed]:
                    self.lex_test(exp, yadn_ws)
            except Exception as ex:
                msg = f'{yadn} failed.'
                raise ex.__class__(msg) from ex

        def unallowed_test(self, state_token, test_token):
            # Expected data and setup.
            name = self.token.name
            article = 'a'
            if name[0] in 'AEIOU':
                article = 'an'

            _, b_test = self.get_example(state_token)
            _, a_test = self.get_example(test_token, False)

            escaped = a_test[0]
            if isinstance(escaped, str):
                escaped = escaped[0]
                if escaped in '+[](){}?^*':
                    escaped = f'\\{escaped}'

            # Expected values.
            exp_ex = ValueError
            exp_msg = f'{escaped} cannot follow {article} {name}.'

            # Test data and state.
            yadn = f'{b_test}{a_test}'
            yadn_ws = f'{b_test} {a_test}'

            # Run test and determine the result.
            try:
                with self.assertRaisesRegex(exp_ex, exp_msg):
                    _ = self.lexer.lex(yadn)
            except AssertionError as ex:
                msg = f'{test_token} failed on {yadn}.'
                raise AssertionError(msg) from ex
            finally:
                self.lexer.state = m.Token.START
                self.lexer.process = self.lexer._start

            try:
                if m.Token.WHITESPACE in self.allowed:
                    self.lexer.state = m.Token.START
                    self.lexer.process = self.lexer._start
                    with self.assertRaisesRegex(exp_ex, exp_msg):
                        _ = self.lexer.lex(yadn_ws)
            except AssertionError as ex:
                msg = f'{test_token} failed on {yadn_ws}.'
                raise AssertionError(msg) from ex
            finally:
                self.lexer.state = m.Token.START
                self.lexer.process = self.lexer._start

        # Allowed next operator.
        def test_alloweds(self):
            """Test tokens allowed to follow."""
            allowed = [t for t in self.allowed if t.name != "WHITESPACE"]
            for token in allowed:
                try:
                    self.allowed_test(self.token, token)
                except Exception as ex:
                    msg = f'{token} failed.'
                    raise ex.__class__(msg) from ex

        def test_unalloweds(self):
            """Test tokens not allowed to follow."""
            unallowed = [t for t in self.tokens if t not in self.allowed]
            unallowed = [t for t in unallowed if t in m.symbols]
            ignore = [
                m.Token.WHITESPACE,
                m.Token.START,
                m.Token.MAP_END,
                m.Token.POOL_END,
                m.Token.QUALIFIER_END,
                m.Token.CHOICE_OPTIONS,
            ]
            if m.Token.AS_OPERATOR in self.allowed:
                ignore.append(m.Token.NEGATIVE_SIGN)
            if self.token == m.Token.NUMBER:
                ignore.append(m.Token.NUMBER)
            unallowed = [t for t in unallowed if t not in ignore]
            for token in unallowed:
                try:
                    self.unallowed_test(self.token, token)
                except Exception as ex:
                    msg = f'{token} failed.'
                    raise ex.__class__(msg) from ex

    class MapLexTestCase(ut.TestCase):
        def setUp(self):
            self.lexer = maps.Lexer()

        def tearDown(self):
            self.lexer = None

        def lex_test(self, exp, yadn):
            act = self.lexer.lex(yadn)
            self.assertTupleEqual(exp, act)

    class MapLexTokenTestCase(LexTokenTestCase):
        token = m.Token.START
        allowed = []
        tokens = (
            m.Token.KV_DELIMITER,
            m.Token.MAP_CLOSE,
            m.Token.MAP_OPEN,
            m.Token.NAME_DELIMITER,
            m.Token.NEGATIVE_SIGN,
            m.Token.NUMBER,
            m.Token.PAIR_DELIMITER,
            m.Token.QUALIFIER,
            m.Token.QUALIFIER_DELIMITER,
        )
        symbols_raw = m.yadn_symbols_raw

        # Details for the allowed and unallowed tests. See
        # LexTokenTestCase above for more explanation.
        example_after = {
            m.Token.KV_DELIMITER: (
                '"spam"}',
                (
                    (m.Token.QUALIFIER, 'spam'),
                    (m.Token.MAP_CLOSE, '}'),
                )
            ),
            m.Token.MAP_CLOSE: ('', ()),
            m.Token.MAP_OPEN: ('}', ((m.Token.MAP_CLOSE, '}'),)),
            m.Token.NEGATIVE_SIGN: (
                '1:"spam"}',
                (
                    (m.Token.NUMBER, -1),
                    (m.Token.KV_DELIMITER, ':'),
                    (m.Token.QUALIFIER, 'spam'),
                    (m.Token.MAP_CLOSE, '}'),
                )
            ),
            m.Token.NAME_DELIMITER: (
                '1:"spam"}',
                (
                    (m.Token.NUMBER, 1),
                    (m.Token.KV_DELIMITER, ':'),
                    (m.Token.QUALIFIER, 'spam'),
                    (m.Token.MAP_CLOSE, '}'),
                )
            ),
            m.Token.NUMBER: (
                ':"eggs"}',
                (
                    (m.Token.KV_DELIMITER, ':'),
                    (m.Token.QUALIFIER, 'eggs'),
                    (m.Token.MAP_CLOSE, '}'),
                )
            ),
            m.Token.PAIR_DELIMITER: (
                '2:"spam"}',
                (
                    (m.Token.NUMBER, 2),
                    (m.Token.KV_DELIMITER, ':'),
                    (m.Token.QUALIFIER, 'spam'),
                    (m.Token.MAP_CLOSE, '}'),
                )
            ),
            m.Token.QUALIFIER_DELIMITER: (
                'spam"}',
                (
                    (m.Token.MAP_CLOSE, '}'),
                )
            ),
            m.Token.QUALIFIER: (
                '}',
                (
                    (m.Token.MAP_CLOSE, '}'),
                )
            ),
        }
        example_before = {
            m.Token.KV_DELIMITER: (
                '{"spam"=1',
                (
                    (m.Token.MAP_OPEN, '{'),
                    (m.Token.QUALIFIER, 'spam'),
                    (m.Token.NAME_DELIMITER, '='),
                    (m.Token.NUMBER, 1),
                )
            ),
            m.Token.MAP_CLOSE: (
                '{"spam"=1:"eggs"',
                (
                    (m.Token.MAP_OPEN, '{'),
                    (m.Token.QUALIFIER, 'spam'),
                    (m.Token.NAME_DELIMITER, '='),
                    (m.Token.NUMBER, 1),
                    (m.Token.KV_DELIMITER, ':'),
                    (m.Token.QUALIFIER, 'eggs'),
                )
            ),
            m.Token.MAP_OPEN: ('', ()),
            m.Token.NAME_DELIMITER: (
                '{"spam"',
                (
                    (m.Token.MAP_OPEN, '{'),
                    (m.Token.QUALIFIER, 'spam'),
                )
            ),
            m.Token.NEGATIVE_SIGN: (
                '{"spam"=',
                (
                    (m.Token.MAP_OPEN, '{'),
                    (m.Token.QUALIFIER, 'spam'),
                    (m.Token.NAME_DELIMITER, '='),
                )
            ),
            m.Token.NUMBER: (
                '{"spam"=',
                (
                    (m.Token.MAP_OPEN, '{'),
                    (m.Token.QUALIFIER, 'spam'),
                    (m.Token.NAME_DELIMITER, '='),
                )
            ),
            m.Token.PAIR_DELIMITER: (
                '{"spam"=1:"eggs"',
                (
                    (m.Token.MAP_OPEN, '{'),
                    (m.Token.QUALIFIER, 'spam'),
                    (m.Token.NAME_DELIMITER, '='),
                    (m.Token.NUMBER, 1),
                    (m.Token.KV_DELIMITER, ':'),
                    (m.Token.QUALIFIER, 'eggs'),
                )
            ),
            m.Token.QUALIFIER: ('{', ((m.Token.MAP_OPEN, '{'),))
        }

        def setUp(self):
            self.lexer = maps.Lexer()

        def tearDown(self):
            self.lexer = None

        def lex_test(self, exp, yadn):
            act = self.lexer.lex(yadn)
            self.assertTupleEqual(exp, act)
