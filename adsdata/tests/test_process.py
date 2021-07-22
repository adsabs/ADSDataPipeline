
import unittest
from mock import patch, mock_open
from datetime import datetime

from adsmsg import NonBibRecord
from adsdata import reader
from adsdata.process import Processor
from adsdata.file_defs import data_files
from adsdata.memory_cache import Cache


class TestMemoryCache(unittest.TestCase):
    """test higher level operations for reading in a set of data for a bibcode"""

    def setup_method(self, method):
        Cache._initted = False

    def test_open(self):
        """can we open data files in the test directory"""
        with Processor(compute_metrics=False) as processor, patch('adsputils.load_config', return_value={'INPUT_DATA_ROOT': './test/data1/config/'}):
            self.assertEqual(len(data_files), len(processor.readers))
            self.assertTrue(isinstance(processor.readers['citation'], reader.NonbibFileReader))
                            
        self.assertEqual(0, len(processor.readers))

    def test_read(self):
        """can we read in all the data for a bibcode"""
        with Processor(compute_metrics=False) as processor, patch('adsputils.load_config', return_value={'INPUT_DATA_ROOT': './test/data1/config/'}):
            d = processor._read_next_bibcode('1057wjlf.book.....C')
            self.assertEqual(d['canonical'], '1057wjlf.book.....C')
            self.assertEqual(len(d['author']), 1)
            self.assertEqual(d['author'], ['Chao, C'])
            self.assertFalse(d['citation'])
            self.assertEqual(d['download'], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
            self.assertFalse(d['grants'])
            self.assertFalse(d['ned_objects'])
            self.assertTrue(d['nonarticle'])
            self.assertEqual(d['ocrabstract'], {'ocrabstract': False})
            self.assertEqual(d['private'], {'private': False})
            self.assertEqual(d['pub_openaccess'], {'pub_openaccess': False})
            self.assertEqual(d['readers'], ['4fc45951aa', '557ebfd055', '57fcb9018a'])
            self.assertEqual(d['reads'], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 6])
            self.assertEqual(d['refereed'], {'refereed': False})
            self.assertEqual(d['relevance'], {'norm_cites': 0, 'read_count': 25, 'boost': 0.32, 'citation_count': 0})

    def test_protobuf(self):
        """make sure protobuf are created without an exception"""
        with Processor(compute_metrics=False) as processor, patch('adsputils.load_config', return_value={'INPUT_DATA_ROOT': './test/data1/config/'}):
            d = processor._read_next_bibcode('1057wjlf.book.....C')
            c = processor._convert(d)
            nonbib = NonBibRecord(**c)
            print('nonbib = {}'.format(nonbib))

    def test_nonbib_record(self):
        self.maxDiff = None
        with Processor(compute_metrics=False) as processor, patch('adsputils.load_config', return_value={'INPUT_DATA_ROOT': './test/data1/config/'}):
            d = processor._read_next_bibcode('2003ASPC..295..361M')
            n = processor._convert(d)
            a = {"read_count": 4, "bibcode": "2003ASPC..295..361M",
                 'bibgroup': ['Chandra Technical'], 'bibgroup_facet': ['Chandra Technical'],
                 "data_links_rows": [{"url": ["http://articles.adsabs.harvard.edu/pdf/2003ASPC..295..361M"], "link_type": "ESOURCE", "link_sub_type": "ADS_PDF", 'item_count': 0, 'title': ['']},
                                     {"url": ["http://articles.adsabs.harvard.edu/full/2003ASPC..295..361M"], "link_type": "ESOURCE", "link_sub_type": "ADS_SCAN", 'item_count': 0, 'title': ['']},
                                     {"url": [""], "link_type": "TOC", "link_sub_type": "NA", 'item_count': 0, 'title': ['']}],
                 "esource": ["ADS_PDF", "ADS_SCAN"],
                 "identifier": ["2003ASPC..295..361M"],
                 "property": ["ADS_OPENACCESS", "ARTICLE", "ESOURCE", "NOT REFEREED", "OPENACCESS", "TOC"], "boost": 0.15, 'citation_count': 0, 'norm_cites': 0,
                 'citation_count_norm': 0.0, 'data': [], 'total_link_counts': 0}
            self.assertEqual(a, n)

            d = processor._read_next_bibcode('2004MNRAS.354L..31M')
            v = processor._convert(d)
            a = {"bibcode": "2004MNRAS.354L..31M",
                 "simbad_objects": ["3253618 G"],
                 "read_count": 20,
                 "data_links_rows": [{"url": ["http://dx.doi.org/10.1111/j.1365-2966.2004.08374.x"], "link_type": "ESOURCE", "link_sub_type": "PUB_HTML", 'item_count': 0, 'title': ['']},
                                     {"url": ["https://arxiv.org/abs/astro-ph/0405472"], "link_type": "ESOURCE", "link_sub_type": "EPRINT_HTML", 'item_count': 0, 'title': ['']},
                                     {"url": ["https://academic.oup.com/mnras/pdf-lookup/doi/10.1111/j.1365-2966.2004.08374.x"], "link_type": "ESOURCE", "link_sub_type": "PUB_PDF", 'item_count': 0, 'title': ['']},
                                     {"url": ["http://articles.adsabs.harvard.edu/pdf/2004MNRAS.354L..31M"], "link_type": "ESOURCE", "link_sub_type": "ADS_PDF", 'item_count': 0, 'title': ['']},
                                     {"url": ["https://arxiv.org/pdf/astro-ph/0405472"], "link_type": "ESOURCE", "link_sub_type": "EPRINT_PDF", 'item_count': 0, 'title': ['']},
                                     {"url": ["http://articles.adsabs.harvard.edu/full/2004MNRAS.354L..31M"], "link_type": "ESOURCE", "link_sub_type": "ADS_SCAN", 'item_count': 0, 'title': ['']},
                                     {"url": ["2004MNRAS.354L..31M", "2005yCat..73549031M"], "title": ["Source Paper", "Catalog Description"], "link_type": "ASSOCIATED", "link_sub_type": "NA", 'item_count': 0},
                                     {"url": ["http://inspirehep.net/search?p=find+j+MNRAA,354,L31"], "link_type": "INSPIRE", "link_sub_type": "NA", 'item_count': 0, 'title': ['']},
                                     {"url": ["http://$VIZIER$/viz-bin/VizieR?-source=J/MNRAS/354/L31"], "item_count": 1, "link_type": "DATA", "link_sub_type": "CDS", 'title': ['']},
                                     {"url": ["https://$NED$/cgi-bin/objsearch?search_type=Search&refcode=2004MNRAS.354L..31M"], "title": ["NED Objects (1953)"], "item_count": 1953, "link_type": "DATA", "link_sub_type": "NED"},
                                     {"url": ["http://$SIMBAD$/simbo.pl?bibcode=2004MNRAS.354L..31M"], "title": ["SIMBAD Objects (1)"], "item_count": 1, "link_type": "DATA", "link_sub_type": "SIMBAD"},
                                     {"url": ["http://$VIZIER$/viz-bin/VizieR?-source=J/MNRAS/354/L31"], "item_count": 1, "link_type": "DATA", "link_sub_type": "Vizier", 'title': ['']}],
                 "identifier": ["2004MNRAS.354L..31M"],
                 "norm_cites": 10000,
                 "data": ["CDS:1", "NED:1953", "SIMBAD:1", "Vizier:1"],
                 "citation_count_norm": 49.5,
                 "citation_count": 99,
                 "property": ["ADS_OPENACCESS", "ARTICLE", "ASSOCIATED", "DATA", "EPRINT_OPENACCESS", "ESOURCE", "INSPIRE", "OPENACCESS", "PUB_OPENACCESS", "REFEREED"],
                 "total_link_counts": 1956,
                 "esource": ["ADS_PDF", "ADS_SCAN", "EPRINT_HTML", "EPRINT_PDF", "PUB_HTML", "PUB_PDF"],
                 "boost": 0.4399999976158142}
            v_boost = v.pop('boost')
            a_boost = a.pop('boost')
            self.assertAlmostEqual(a_boost, v_boost)
            self.assertEqual(a, v)

        # consider video 1997kbls.confE..10C
        # consider library 1810hdla.book.....V
        # consider inspire 1908PASP...20....1.

    def test_add_data_summary(self):
        self.maxDiff = None
        with Processor(compute_metrics=False) as processor, patch('adsputils.load_config', return_value={'INPUT_DATA_ROOT': './test/data1/config/'}):
            data_links_rows = [{"url": ["http://dx.doi.org/10.1111/j.1365-2966.2004.08374.x"], "link_type": "ESOURCE", "link_sub_type": "PUB_HTML"},
                               {"url": ["https://arxiv.org/abs/astro-ph/0405472"], "link_type": "ESOURCE", "link_sub_type": "EPRINT_HTML"},
                               {"url": ["https://academic.oup.com/mnras/pdf-lookup/doi/10.1111/j.1365-2966.2004.08374.x"], "link_type": "ESOURCE", "link_sub_type": "PUB_PDF"},                                                                 {"url": ["http://articles.adsabs.harvard.edu/pdf/2004MNRAS.354L..31M"], "link_type": "ESOURCE", "link_sub_type": "ADS_PDF"},
                               {"url": ["https://arxiv.org/pdf/astro-ph/0405472"], "link_type": "ESOURCE", "link_sub_type": "EPRINT_PDF"},
                               {"url": ["http://articles.adsabs.harvard.edu/full/2004MNRAS.354L..31M"], "link_type": "ESOURCE", "link_sub_type": "ADS_SCAN"},
                               {"url": ["2004MNRAS.354L..31M", "2005yCat..73549031M"], "title": ["Source Paper", "Catalog Description"], "link_type": "ASSOCIATED", "link_sub_type": "NA"},
                               {"url": ["http://inspirehep.net/search?p=find+j+MNRAA,354,L31"], "link_type": "INSPIRE", "link_sub_type": "NA"},
                               {"url": ["http://$VIZIER$/viz-bin/VizieR?-source=J/MNRAS/354/L31"], "item_count": 1, "link_type": "DATA", "link_sub_type": "CDS"},
                               {"url": ["http://$VIZIER$/viz-bin/VizieR?-source=J/MNRAS/354/L32"], "item_count": 1, "link_type": "DATA", "link_sub_type": "CDS"},
                               {"url": ["https://$NED$/cgi-bin/objsearch?search_type=Search&refcode=2004MNRAS.354L..31M"], "title": ["NED Objects (1953)"], "item_count": 1953, "link_type": "DATA", "link_sub_type": "NED"},
                               {"url": ["http://$VIZIER$/viz-bin/VizieR?-source=J/MNRAS/354/L33"], "item_count": 2, "link_type": "DATA", "link_sub_type": "CDS"},
                               {"url": ["http://$SIMBAD$/simbo.pl?bibcode=2004MNRAS.354L..31M"], "title": ["SIMBAD Objects (1)"], "item_count": 1, "link_type": "DATA", "link_sub_type": "SIMBAD"},
                               {"url": ["http://$VIZIER$/viz-bin/VizieR?-source=J/MNRAS/354/L31"], "item_count": 2, "link_type": "DATA", "link_sub_type": "Vizier"}]
            d = {'data_links_rows': data_links_rows}
            processor._add_data_summary(d)
            self.assertEqual(["CDS:4", "NED:1953", "SIMBAD:1", "Vizier:2"], d['data'])

    def test_metrics_trivial_fields(self):
        d = {'canonical': "1998PPGeo..22..553A", 'refereed': {'refereed': False}, 'author': ["Arnfield, A. L."],
             'reads': [1, 2, 3, 4], 'download': [0, 1, 2, 3],
             'citations':  ['1998PPGeo..22..553B'], 'id': 11, 'reference': ["1997BoLMe..85..475M"]}
        m = mock_open(read_data='')
        m.return_value.__iter__ = lambda self: iter(self.readline, '')
        with patch('builtins.open', m), Processor(compute_metrics=False) as processor:
            Cache.get('citation')['1998PPGeo..22..553A'] = ['1998PPGeo..22..553B']
            met = processor._compute_metrics(d)
            self.assertEqual(met['bibcode'], d['canonical'])
            self.assertEqual(met['citations'], d['citations'])
            self.assertEqual(met['reads'], d['reads'])
            self.assertEqual(met['downloads'], d['download'])

    def test_num_fields(self):
        d = {'canonical': "1998PPGeo..22..553A", 'refereed': {'refereed': False}, 'author': ["Arnfield, A. L."],
             'reads': [1, 2, 3, 4], 'download': [0, 1, 2, 3],
             'citations':  ['1998PPGeo..22..553A'], 'id': 11, 'reference': ["1997BoLMe..85..475M"]}
        m = mock_open(read_data='')
        m.return_value.__iter__ = lambda self: iter(self.readline, '')
        with patch('builtins.open', m), Processor(compute_metrics=True) as processor:
            Cache.get('citation')['1998PPGeo..22..553A'].append('1998PPGeo..22..553B')
            Cache.get('reference')['1998PPGeo..22..553A'].append('1998PPGeo..22..553B')
            met = processor._compute_metrics(d)
            self.assertEqual(met['citation_num'], len(d['citations']))
            self.assertEqual(met['reference_num'], len(d['reference']))
            self.assertEqual(met['author_num'], len(d['author']))
            self.assertEqual(met['refereed_citation_num'], 0)

    def test_with_citations(self):
        d = {'canonical': "1997BoLMe..85..475M", 'refereed': {'refereed': True},
             'author': ["Meesters, A. G. C. A.", "Bink, N. J.",  "Henneken, E. A. C.",
                        "Vugts, H. F.", "Cannemeijer, F."],
             'download': [], 'reads': [],
             'citations': ["1998PPGeo..22..553A", "1999P&SS...47..951S", "2000BoLMe..97..385O",
                           "2001MAP....78..115K", "2002BoLMe.103...49H", "2006QJRMS.132..779R",
                           "2006QJRMS.132...61E", "2008Sci...320.1622D", "2016BoLMe.159..469G"],
             'reference': ["1994BoLMe..71..393V", "1994GPC.....9...53M", "1994GPC.....9...53X"]}
        m = mock_open(read_data='')
        m.return_value.__iter__ = lambda self: iter(self.readline, '')
        with patch('builtins.open', m), Processor(compute_metrics=True) as processor:
            for bib in d['citations']:
                Cache.get('citation')['1997BoLMe..85..475M'].append(bib)
            for bib in d['reference']:
                Cache.get('reference')['1997BoLMe..85..475M'].append(bib)
            refereed = ['1997BoLMe..85..475M', "1999P&SS...47..951S", "2000BoLMe..97..385O",
                        "2001MAP....78..115K", "2002BoLMe.103...49H", "2006QJRMS.132..779R",
                        "2006QJRMS.132...61E", "2008Sci...320.1622D", "2016BoLMe.159..469G"]
            for bib in refereed:
                Cache.get('refereed').add(bib)
            # 1999P&SS...47..951S
            PSSreferences = ["1973JAtS...30...66B", "1973JAtS...30..749L", "1976JAtS...33..923B",
                             "1977JGR....82.4121B", "1977JGR....82.4249K", "1977JGR....82.4559H",
                             "1978Icar...33..417W", "1978JAtS...35.2346S", "1978JGR....83.1889D",
                             "1979Icar...39..151H", "1979Icar...39..184H", "1979JGR....84.2889J",
                             "1979JGR....84.2929P", "1979Natur.278..531H", "1981GeoRL...8..899R",
                             "1981suma.book.....C", "1982JAtS...39.2701M", "1982JGR....87.9975M",
                             "1982MWRv..110..994A", "1985AdSpR...5...93H", "1985PhDT.........2P",
                             "1985TellA..37..156A", "1985wagp.book.....G", "1987MWRv..115..936Y",
                             "1987MWRv..115.2214P", "1988aitb.book.....S", "1989BAMS...70..738B",
                             "1990JAtS...47..612Y", "1990JGR....95.1359J", "1991ConAP..64..103S",
                             "1992aitd.book.....H", "1992BoLMe..59..141G", "1992JGR....97.7781Z",
                             "1993JAtS...50...77S", "1993JGR....98.3125B", "1994DPS....26.1806G",
                             "1995Icar..113..277M", "1995JGR...100.5277H", "1995MWRv..123.1146H",
                             "1996Icar..122...36C", "1996JGR...10114957S", "1996Sci...271..184S",
                             "1997AdSpR..19.1241S", "1997AdSpR..19.1289M", "1997BoLMe..85..475M",
                             "1997JGR...102.4463W", "1997Sci...278.1758S", "1998Sci...279.1686S"]
            for bib in PSSreferences:
                Cache.get('reference')['1999P&SS...47..951S'].append(bib)
                
            met = processor._compute_metrics(d)
            self.assertEqual(len(met['citations']), len(d['citations']), 'citations check')
            self.assertEqual(met['refereed_citation_num'], len(refereed) - 1)
            self.assertEqual(met['refereed_citations'], refereed[1:])
            rn_citation_data = {"cityear": 1998, "pubyear": 1997, "auth_norm": 0.20000000298023224,
                                "bibcode": "1998PPGeo..22..553A", "ref_norm": 0.20000000298023224}
            rn_citation_data1 = {"cityear": 1999, "pubyear": 1997, "auth_norm": 0.20000000298023224,
                                 "bibcode": "1999P&SS...47..951S", "ref_norm": 0.02083333395421505}
            self.compare_citation_data(met['rn_citation_data'][0], rn_citation_data)
            self.compare_citation_data(met['rn_citation_data'][1], rn_citation_data1)
            
            y = int(d['canonical'][:4])
            today = datetime.today()
            age = max(1.0, today.year - y + 1)
            self.assertAlmostEqual(met['an_refereed_citations'], len(met['refereed_citations'])/float(age), 5)

    def compare_citation_data(self, a, b):
        self.assertEqual(a['bibcode'], b['bibcode'])
        self.assertEqual(a['pubyear'], b['pubyear'])
        self.assertEqual(a['cityear'], b['cityear'])
        self.assertAlmostEqual(a['auth_norm'], b['auth_norm'])
        self.assertAlmostEqual(a['ref_norm'], b['ref_norm'])

    def test_compute_bibgroup_facet(self):
        p = Processor()
        self.assertEqual({}, p._compute_bibgroup_facet({}))
        self.assertEqual({'bibgroup_facet': ['a']}, p._compute_bibgroup_facet({'bibgroup': ['a']}))
        self.assertEqual({'bibgroup_facet': ['a', 'b']}, p._compute_bibgroup_facet({'bibgroup': ['a', 'b']}))
        self.assertEqual({'bibgroup_facet': ['a', 'b']}, p._compute_bibgroup_facet({'bibgroup': ['a', 'b', 'a']}))

    def test_compute_identifier(self):
        p = Processor()
        d = {'bibcode': '2013MNRAS.435.1904M',
             'deleted': ['2013MNRAS.tmp.2206M'],
             'doi': ['10.1093/mnras/stt1379'],
             'preprint': ['1307.6556'],
             'pub2arxiv': ['2013arXiv1307.6556M']}
        a = p._compute_identifier(d)
        self.assertEqual({'identifier': ['2013MNRAS.435.1904M', '2013MNRAS.tmp.2206M',
                                         '10.1093/mnras/stt1379', 'arxiv:1307.6556', '2013arXiv1307.6556M']},
                         a)

        d = {'bibcode': 'bib',
             'deleted': ['deleted1', 'deleted2'],
             'doi': ['doia', 'doib'],
             'preprint': ['preprintA', 'preprintB', 'preprintC'],
             'pub2arxiv': ['arxivFoo', 'arxivBar']}
        a = p._compute_identifier(d)
        self.assertEqual({'identifier': ['bib',
                                         'deleted1', 'deleted2',
                                         'doia', 'doib',
                                         'arxiv:preprintA', 'arxiv:preprintB', 'arxiv:preprintC',
                                         'arxivFoo', 'arxivBar']},
                         a)
        d = {'bibcode': 'bib',
             'deleted': [],
             'doi': [],
             'preprint': [],
             'pub2arxiv': []}
        a = p._compute_identifier(d)
        self.assertEqual({'identifier': ['bib']}, a)
        d = {'bibcode': 'bib'}
        a = p._compute_identifier(d)
        self.assertEqual({'identifier': ['bib']}, a)
        
