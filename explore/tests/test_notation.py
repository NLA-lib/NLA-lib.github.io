import unittest
from notation import math_spans,diagnostics,normalize
from content_pages import markdown

class NotationTests(unittest.TestCase):
    def test_math_delimiters_code_and_escaped_currency(self):
        text=r'\(x+1\) and \[A\] and $y$ and \$5. `\(code\) $z$`'+'\n~~~\n$x$\n~~~\n'
        spans,issues=math_spans(text)
        self.assertEqual([span[2] for span in spans],['x+1','A','y'])
        self.assertFalse(issues)
        rendered=markdown(text)
        self.assertEqual(rendered.count('class="math'),3)
        self.assertIn('$5',rendered)
        self.assertIn('<code>\\(code\\) $z$</code>',rendered)

    def test_unfinished_math_is_diagnostic_and_source_is_preserved(self):
        self.assertEqual(diagnostics('$x')[0]['code'],'math-delimiter')
        self.assertEqual(diagnostics('$x^{2$')[0]['code'],'math-braces')
        self.assertIn('x',markdown('$x'))

    def test_declared_roles_do_not_guess_from_capitalization(self):
        roles={'matrices':['A'],'vectors':['x']}
        self.assertEqual([x['code'] for x in diagnostics('$Ax=b$',roles)],['symbol-weight','symbol-weight'])
        self.assertFalse(diagnostics(r'$\mathbf{A}\mathbf{x}=b$',roles))
        self.assertFalse(diagnostics(r'$\operatorname{Ax}(b)+\mathbb{A}$',roles))
        self.assertFalse(diagnostics('$Ax=b$'))

    def test_explicit_migration_preserves_scalars_code_and_fonts(self):
        source=r'$A x=b,\quad k=1,\quad \mathbb P,\quad \mathbf x^{\mathsf H}$. `$Ax=b$`'
        fixed=normalize(source,{'matrices':['A'],'vectors':['x','b']})
        self.assertIn(r'\mathbf{A} \mathbf{x}=\mathbf{b}',fixed)
        self.assertIn('k=1',fixed)
        self.assertIn(r'\mathbb P',fixed)
        self.assertIn(r'\mathbf{x}^{\mathsf{H}}',fixed)
        self.assertTrue(fixed.endswith('`$Ax=b$`'))
        self.assertEqual(normalize(fixed,{'matrices':['A'],'vectors':['x','b']}),fixed)

    def test_transpose_suggestions_do_not_rewrite_powers_or_conjugates(self):
        source=r'$A^T+A^{H}+z^*+x^k$'
        issues=diagnostics(source)
        self.assertEqual(len(issues),2)
        self.assertTrue(all(issue['severity']=='warning' for issue in issues))
        self.assertEqual(normalize(source),source)
        self.assertFalse(diagnostics(r'$\mathbf{A}^{\mathsf{T}}+\mathbf{A}^{\mathsf{H}}+z^*$'))
