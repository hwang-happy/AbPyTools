from src.utils.downloads import Download
import re
import numpy as np
import json


class Antibody:
    """
    TODO: write description
    """

    def __init__(self, sequence='', name='', numbering=None):
        self.raw_sequence = sequence
        self.sequence = sequence.replace('-', '')
        self.name = name
        self.numbering = numbering
        self.hydrophobicity_matrix = np.array([])
        self.chain = ''

    def apply_numbering(self, server='abysis', numbering_scheme='chothia'):

        available_numbering_schemes = ['chothia', 'chothia_ext', 'kabath']
        available_servers = ['abysis']

        assert numbering_scheme.lower() in available_numbering_schemes, \
            "Unknown Numbering scheme: {}. \
            Numbering schemes available: {}".format(numbering_scheme,
                                                    ', '.join(available_numbering_schemes))

        assert server in available_servers, "Unknown server: {}. \
            Available servers: {}".format(server, ' ,'.join(available_servers))

        self.numbering = get_ab_numbering(self.sequence, server, numbering_scheme)

        if self.numbering[0][0] == 'H':
            self.chain = 'Heavy'
        elif self.numbering[0][0] == 'L':
            self.chain = 'Light'
        else:
            self.chain = ''
            self.numbering = 'NA'
            print('Could not apply numbering scheme on provided sequence')

    def calculate_hydrophobicity(self, hydrophobicity_scores):

        # check if all the required parameters are in order
        available_hydrophobicity_scores = ['kd', 'ww', 'hh', 'mf', 'ew']

        if isinstance(hydrophobicity_scores, str):
            assert hydrophobicity_scores in available_hydrophobicity_scores, \
                "Chosen hydrophobicity scores ({}) not available. \
                Available hydrophobicity scores: {}".format(
                    hydrophobicity_scores, ' ,'.join(available_hydrophobicity_scores)
                )

        if self.chain == 'Light':
            self.hydrophobicity_matrix = np.zeros(138)
        elif self.chain == 'Heavy':
            self.hydrophobicity_matrix = np.zeros(158)
        else:
            self.hydrophobicity_matrix = 'NA'
            print('Could not calculate the hydrophobicity matrix of the \
                  the provided sequence')
            return

        # get the dictionary with the hydrophobicity scores
        self.aa_hydrophobicity_scores = get_aa_hydrophobicity_scores(hydrophobicity_scores)

        for i, amino_acid in enumerate(self.raw_sequence):
            if amino_acid not in self.aa_hydrophobicity_scores.values():
                self.hydrophobicity_matrix[i] = 0
            else:
                self.hydrophobicity_matrix[i] = self.aa_hydrophobicity_scores[amino_acid.upper()]


def get_ab_numbering(sequence, server, numbering_scheme):
    # check which server to use to get numbering
    if server.lower() == 'abysis':
        # find out which numbering scheme to use
        if numbering_scheme.lower() == 'chothia':
            scheme = '-c'
        elif numbering_scheme.lower() == 'chotia_ext':
            scheme = '-a'
        else:
            scheme = '-k'

        url = 'http://www.bioinf.org.uk/cgi-bin/abnum/abnum.pl?plain=1&aaseq={}&scheme={}'.format(sequence,
                                                                                                  scheme)

        query = Download(url, verbose=False)

        numbering_table = query.download().html

        parsed_numbering_table = re.findall('[\S| ]+', numbering_table)

        numbering = [x[:-2] for x in parsed_numbering_table]

        # TODO: add more server options
    else:
        numbering = ['']

    return numbering

def get_aa_hydrophobicity_scores(hydrophobicity_scores):

    with open('../../data/Hydrophobicity.json') as f:
        hydrophobicity_data = json.load(f)

    return hydrophobicity_data["hydrophobicity"][hydrophobicity_scores+'hydrophobicity']