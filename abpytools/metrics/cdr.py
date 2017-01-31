from abpytools import AntibodyCollection
import numpy as np


class CDR:

    def __init__(self, antibodies=None):
        # expect a string which is a path to a FASTA file
        if isinstance(antibodies, str):
            self.antibodies = AntibodyCollection(path=antibodies)
            self.antibodies.load()
        # can also be a AntibodyCollection object
        elif isinstance(antibodies, AntibodyCollection):
            self.antibodies = antibodies
            # check if AntibodyCollection has been loaded (should have n_ab > 0)
            # TODO come up with a more elegant way to check if .load() method has been called
            if self.antibodies.n_ab == 0:
                self.antibodies.load()
        else:
            raise IOError("Unexpected file type")

        self._cdrs = self.antibodies.cdr_index()
        self._framework = None
        self._sequence = self.antibodies.sequences()

    def cdr_length(self):
        """
        method to obtain cdr_lengths
        :return: m by n matrix with CDR lengths, where m is the number of antibodies in AntibodyCollection and n is
        three, corresponding to the three CDRs.
        """
        cdr_length_matrix = np.zeros((len(self._cdrs), 3))

        for m, antibody in enumerate(self._cdrs):
            for n, cdr in enumerate(['CDR1','CDR2','CDR3']):
                cdr_length_matrix[m,n] = len(antibody[cdr])

        return cdr_length_matrix

    def cdr_sequences(self):
        """
        method that returns sequences of each cdr
        :return: list of dictionaries with keys 'CDR1', 'CDR2' and 'CDR3' containing a string with the respective amino
        acid sequence
        """
        cdr_sequences = list()

        for sequence, antibody in zip(self._sequence, self._cdrs):
            dict_i = dict()
            for cdr in ['CDR1', 'CDR2', 'CDR3']:
                seq_i = list()
                indices = antibody[cdr]
                for i in indices:
                    seq_i.append(sequence[i])
                dict_i[cdr] = ''.join(seq_i)
            cdr_sequences.append(dict_i)

        return cdr_sequences

    def framework_length(self):
        pass

    def framework_sequences(self):
        pass
