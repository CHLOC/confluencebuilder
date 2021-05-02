# -*- coding: utf-8 -*-
"""
:copyright: Copyright 2021 Sphinx Confluence Builder Contributors (AUTHORS)
:license: BSD-2-Clause (LICENSE)
"""

from sphinxcontrib.confluencebuilder.singlebuilder import SingleConfluenceBuilder
from tests.lib import build_sphinx
from tests.lib import parse
from tests.lib import prepare_conf
import os
import unittest

class TestConfluenceSinglepageToctree(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.config = prepare_conf()
        self.test_dir = os.path.dirname(os.path.realpath(__file__))

    def test_storage_singlepage_docref_pageref(self):
        dataset = os.path.join(self.test_dir, 'datasets', 'singlepage-docref')

        out_dir = build_sphinx(dataset, config=self.config,
            builder=SingleConfluenceBuilder.name)

        with parse('index', out_dir) as data:
            links = data.find_all('ac:link')
            self.assertEqual(len(links), 1)

            # the anchor value should be pointing to `pageb2`, which maps to the
            # anchor target generated by confluence based on the title/heading
            # being given a value of "pageb2" (opposed to just `pageb` which is
            # a raw map to the docname target)
            link = links[0]
            self.assertIsNotNone(link)
            self.assertTrue(link.has_attr('ac:anchor'))
            self.assertEqual(link['ac:anchor'], 'pageb2')

    def test_storage_singlepage_docref_index_no_title(self):
        dataset = os.path.join(self.test_dir, 'datasets', 'singlepage-docref')

        out_dir = build_sphinx(dataset, config=self.config,
            builder=SingleConfluenceBuilder.name)

        with parse('index', out_dir) as data:
            links = data.find_all('a')
            self.assertEqual(len(links), 1)

            # link from pagea to the index should have been replaced with a #top
            link = links[0]
            self.assertIsNotNone(link)
            self.assertTrue(link.has_attr('href'))
            self.assertEqual(link['href'], '#top')

    def test_storage_singlepage_docref_index_with_title(self):
        config = dict(self.config)
        config['confluence_remove_title'] = False

        dataset = os.path.join(self.test_dir, 'datasets', 'singlepage-docref')

        out_dir = build_sphinx(dataset, config=config,
            builder=SingleConfluenceBuilder.name)

        with parse('index', out_dir) as data:
            links = data.find_all('ac:link')
            self.assertEqual(len(links), 2)

            # the anchor value should be pointing to `index2`, which maps to the
            # anchor target generated by confluence based on the title/heading
            # being given a value of "index2" (opposed to just `index` which is
            # a raw map to the docname target)
            link = links[1] # (second link)
            self.assertIsNotNone(link)
            self.assertTrue(link.has_attr('ac:anchor'))
            self.assertEqual(link['ac:anchor'], 'index2')