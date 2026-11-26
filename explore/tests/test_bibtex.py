"""Frontend bibliography fidelity, citation styling and immutable citation identities."""
import json
from pathlib import Path
import tempfile
import unittest
from bibtex import parse_bib_text, one_reference, citation_parts
from bibliography import frontend_references
import test_content_pages as fixtures
from content_pages import Explorer

BOOK='@book{Key2020,\n author = {Doe, Jane and Smith, John},\n title = {A {Protected} Title},\n publisher = {Publisher},\n year = {2020},\n doi = {10.1000/test},\n note = {Keep this extra field}\n}\n'

class BibtexTests(unittest.TestCase):
    def test_raw_entry_and_extra_fields_survive_parsing(self):
        key,record=one_reference(BOOK,'Key2020')
        self.assertEqual(record['bibtex'],BOOK);self.assertEqual(record['authors'],['Jane Doe','John Smith'])
        self.assertEqual(record['title'],'A Protected Title');self.assertEqual(record['publisher'],'Publisher')
        self.assertIn('Keep this extra field',record['bibtex'])
    def test_citation_styles_do_not_wrap_authors_or_publisher_in_a_link(self):
        record=one_reference(BOOK)[1];markup=citation_parts(record)
        self.assertIn('<span class="reference-authors">Jane Doe and John Smith.</span>',markup)
        self.assertIn('<cite class="reference-title"><a ',markup)
        self.assertIn('<span class="reference-publisher">Publisher</span>',markup)
        self.assertNotIn('>Jane Doe',markup.split('<a ',1)[1].split('</a>',1)[0])
    def test_quoted_fields_nested_braces_and_math_titles(self):
        record=one_reference('@article{Test, title = "The {$Ax=b$} problem", author = {D\\\'erezinski, Micha{\\\"e}l}, journal={A Journal}, volume=12, year=2024}\n')[1]
        markup=citation_parts(record)
        self.assertIn('class="math">Ax=b',markup);self.assertIn('<cite class="reference-journal">A Journal</cite>',markup)
        self.assertIn('<strong class="reference-volume">12</strong>',markup)
    def test_key_changes_multiple_entries_unsafe_urls_and_missing_title_are_rejected(self):
        with self.assertRaises(ValueError):one_reference(BOOK,'OtherKey')
        with self.assertRaises(ValueError):one_reference(BOOK+BOOK.replace('Key2020','Other'))
        with self.assertRaises(ValueError):one_reference('@misc{Bad,title={Bad},url={javascript:alert(1)}}')
        with self.assertRaises(ValueError):one_reference('@misc{Bad,author={A}}')
    def test_title_and_author_html_are_escaped(self):
        record=one_reference('@misc{Safe,title={<script>bad</script>},author={<b>Author</b>}}')[1]
        markup=citation_parts(record);self.assertNotIn('<script>',markup);self.assertNotIn('<b>',markup)
    def test_reference_directory_and_individual_downloads_use_frontend_bibtex(self):
        fixture=fixtures.MarkdownExplorerTests();fixture.setUp();self.addCleanup(fixture.doCleanups)
        folder=fixture.content/'references';folder.mkdir();(folder/'Key2020.bib').write_text(BOOK)
        explorer=Explorer(fixture.site,fixture.content);explorer.build()
        self.assertEqual((fixture.site/'references/Key2020.bib').read_text(),BOOK)
        self.assertEqual((fixture.site/'references.bib').read_text().strip(),BOOK.strip())
        page=(fixture.site/'references/index.html').read_text()
        self.assertIn('Download the complete bibliography',page);self.assertIn('reference-authors',page)
        self.assertIn('<cite class="reference-title">',page)
