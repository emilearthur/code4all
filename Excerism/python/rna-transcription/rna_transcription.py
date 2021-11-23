def to_rna(dna_strand):
    _factor = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
    output = []

    for strand in dna_strand:
        for key, value in _factor.items():
            if str(strand) == str(key):
                output.append(value)

    return ''.join([str(_n) for _n in output])
