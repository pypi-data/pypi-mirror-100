"""This list is adapted from `<https://github.com/computationalstylistics/tidystopwords>`_
which in turn is based on UniversalDependencies treebanks.
"""

STOPS = [
    "ϣⲁ",  # lemma: ϣⲁ, UD_pos: ADP
    "ϣⲁⲣⲟ",  # lemma: ϣⲁ, UD_pos: ADP
    "ϣⲁⲣⲱ",  # lemma: ϣⲁ, UD_pos: ADP
    "ϩⲁ",  # lemma: ϩⲁ, UD_pos: ADP
    "ϩⲁϩⲧⲏ",  # lemma: ϩⲁϩⲧⲛ, UD_pos: ADP
    "ϩⲁⲣⲁⲧ",  # lemma: ϩⲁⲣⲁⲧ, UD_pos: ADP
    "ϩⲁⲣⲟ",  # lemma: ϩⲁ, UD_pos: ADP
    "ϩⲁⲣⲱ",  # lemma: ϩⲁ, UD_pos: ADP
    "ϩⲁⲧⲉ",  # lemma: ϩⲁⲧⲉ, UD_pos: ADP
    "ϩⲁⲧⲉ",  # lemma: ϩⲁϩⲧⲛ, UD_pos: ADP
    "ϩⲁⲧⲛ",  # lemma: ϩⲁⲧⲛ, UD_pos: ADP
    "ϩⲓ",  # lemma: ϩⲓ, UD_pos: ADP
    "ϩⲓϫⲙ",  # lemma: ϩⲓϫⲛ, UD_pos: ADP
    "ϩⲓϫⲛ",  # lemma: ϩⲓϫⲛ, UD_pos: ADP
    "ϩⲓϫⲱ",  # lemma: ϩⲓϫⲛ, UD_pos: ADP
    "ϩⲓⲣⲙ",  # lemma: ϩⲓⲣⲛ, UD_pos: ADP
    "ϩⲓⲧⲙ",  # lemma: ϩⲓⲧⲛ, UD_pos: ADP
    "ϩⲓⲧⲛ",  # lemma: ϩⲓⲧⲛ, UD_pos: ADP
    "ϩⲓⲧⲟⲟⲧ",  # lemma: ϩⲓⲧⲟⲟⲧ, UD_pos: ADP
    "ϩⲓⲧⲟⲟⲧ",  # lemma: ϩⲓⲧⲛ, UD_pos: ADP
    "ϩⲓⲧⲟⲩⲱ",  # lemma: ϩⲓⲧⲟⲩⲛ, UD_pos: ADP
    "ϩⲓⲱ",  # lemma: ϩⲓ, UD_pos: ADP
    "ϩⲓⲱⲱ",  # lemma: ϩⲓ, UD_pos: ADP
    "ϩⲙ",  # lemma: ϩⲛ, UD_pos: ADP
    "ϩⲙ",  # lemma: ϩⲙ, UD_pos: ADP
    "ϩⲛ",  # lemma: ϩⲛ, UD_pos: ADP
    "ϫⲓⲛ",  # lemma: ϫⲓⲛ, UD_pos: ADP
    "ⲁϫⲛ",  # lemma: ⲁϫⲛ, UD_pos: ADP
    "ⲉ",  # lemma: ⲉ, UD_pos: ADP
    "ⲉ",  # lemma: ⲉⲣⲉ, UD_pos: ADP
    "ⲉ",  # lemma: ⲉⲣⲉ_ⲛⲧⲟⲟⲩ, UD_pos: ADP
    "ⲉϩⲟⲩⲉ",  # lemma: ⲉϩⲟⲩⲉ, UD_pos: ADP
    "ⲉϫⲙ",  # lemma: ⲉϫⲛ, UD_pos: ADP
    "ⲉϫⲛ",  # lemma: ⲉϫⲛ, UD_pos: ADP
    "ⲉϫⲱ",  # lemma: ⲉϫⲛ, UD_pos: ADP
    "ⲉⲣⲁⲧ",  # lemma: ⲉⲣⲁⲧ, UD_pos: ADP
    "ⲉⲣⲟ",  # lemma: ⲉ, UD_pos: ADP
    "ⲉⲣⲱ",  # lemma: ⲉ, UD_pos: ADP
    "ⲉⲧⲃⲉ",  # lemma: ⲉⲧⲃⲉ, UD_pos: ADP
    "ⲉⲧⲃⲏⲏⲧ",  # lemma: ⲉⲧⲃⲉ, UD_pos: ADP
    "ⲉⲧⲟⲟⲧ",  # lemma: ⲉⲧⲛ, UD_pos: ADP
    "ⲕⲁⲧⲁ",  # lemma: ⲕⲁⲧⲁ, UD_pos: ADP
    "ⲙ",  # lemma: ⲛ, UD_pos: ADP
    "ⲙ",  # lemma: ⲙ, UD_pos: ADP
    "ⲙⲙⲟ",  # lemma: ⲛ, UD_pos: ADP
    "ⲙⲙⲟ",  # lemma: ⲙⲙⲟ, UD_pos: ADP
    "ⲙⲙⲱ",  # lemma: ⲛ, UD_pos: ADP
    "ⲙⲛ",  # lemma: ⲙⲛ, UD_pos: ADP
    "ⲙⲛⲛⲥⲁ",  # lemma: ⲙⲛⲛⲥⲁ, UD_pos: ADP
    "ⲙⲛⲛⲥⲱ",  # lemma: ⲙⲛⲛⲥⲁ, UD_pos: ADP
    "ⲛ",  # lemma: ⲛ, UD_pos: ADP
    "ⲛ",  # lemma: ⲙ, UD_pos: ADP
    "ⲛ",  # lemma: ⲡ, UD_pos: ADP
    "ⲛ",  # lemma: ⲙ̄, UD_pos: ADP
    "ⲛ",  # lemma: ⲛⲁ, UD_pos: ADP
    "ⲛϩⲏⲧ",  # lemma: ϩⲛ, UD_pos: ADP
    "ⲛϩⲏⲧ",  # lemma: ϩⲏⲧ, UD_pos: ADP
    "ⲛϩⲏⲧ",  # lemma: ⲛϩⲏⲧ, UD_pos: ADP
    "ⲛⲁ",  # lemma: ⲛⲁ, UD_pos: ADP
    "ⲛⲁ",  # lemma: ⲙ, UD_pos: ADP
    "ⲛⲁ",  # lemma: ⲛ, UD_pos: ADP
    "ⲛⲁϩⲣⲁ",  # lemma: ⲛⲁϩⲣⲛ, UD_pos: ADP
    "ⲛⲏ",  # lemma: ⲛⲁ, UD_pos: ADP
    "ⲛⲙ",  # lemma: ⲙⲛ, UD_pos: ADP
    "ⲛⲙⲙ",  # lemma: ⲙⲛ, UD_pos: ADP
    "ⲛⲙⲙ",  # lemma: ⲛⲙⲙ, UD_pos: ADP
    "ⲛⲙⲙⲁ",  # lemma: ⲙⲛ, UD_pos: ADP
    "ⲛⲙⲙⲏ",  # lemma: ⲙⲛ, UD_pos: ADP
    "ⲛⲛⲁϩⲣⲙ",  # lemma: ⲛⲛⲁϩⲣⲛ, UD_pos: ADP
    "ⲛⲛⲁϩⲣⲙ",  # lemma: ⲛⲁϩⲣⲛ, UD_pos: ADP
    "ⲛⲛⲁϩⲣⲛ",  # lemma: ⲛⲛⲁϩⲣⲛ, UD_pos: ADP
    "ⲛⲛⲁϩⲣⲛ",  # lemma: ⲛⲁϩⲣⲛ, UD_pos: ADP
    "ⲛⲥⲁ",  # lemma: ⲛⲥⲁ, UD_pos: ADP
    "ⲛⲥⲱ",  # lemma: ⲛⲥⲁ, UD_pos: ADP
    "ⲛⲧⲉ",  # lemma: ⲛⲧⲉ, UD_pos: ADP
    "ⲛⲧⲟⲟⲧ",  # lemma: ⲛⲧⲛ, UD_pos: ADP
    "ⲟⲩⲃⲉ",  # lemma: ⲟⲩⲃⲉ, UD_pos: ADP
    "ⲟⲩⲃⲏ",  # lemma: ⲟⲩⲃⲉ, UD_pos: ADP
    "ⲡⲁⲣⲁ",  # lemma: ⲡⲁⲣⲁ, UD_pos: ADP
    "ⲧⲟⲟⲧ",  # lemma: ⲧⲟⲟⲧ, UD_pos: ADP
    "ⲭⲱⲣⲓⲥ",  # lemma: ⲭⲱⲣⲓⲥ, UD_pos: ADP
    "ϣ",  # lemma: ϣ, UD_pos: AUX
    "ϣⲁ",  # lemma: ϣⲁⲣⲉ, UD_pos: AUX
    "ϣⲁ",  # lemma: ϣⲁ, UD_pos: AUX
    "ϣⲁⲛⲧ",  # lemma: ϣⲁⲛⲧⲉ, UD_pos: AUX
    "ϣⲁⲛⲧⲉ",  # lemma: ϣⲁⲛⲧⲉ, UD_pos: AUX
    "ϣⲁⲣⲉ",  # lemma: ϣⲁⲣⲉ, UD_pos: AUX
    "ⲁ",  # lemma: ⲁ, UD_pos: AUX
    "ⲁ",  # lemma: ⲛⲁ, UD_pos: AUX
    "ⲉϣ",  # lemma: ϣ, UD_pos: AUX
    "ⲉϣ",  # lemma: ⲉϣ, UD_pos: AUX
    "ⲉⲣϣⲁⲛ",  # lemma: ⲉⲣϣⲁⲛ, UD_pos: AUX
    "ⲉⲣⲉ",  # lemma: ⲉⲣⲉ, UD_pos: AUX
    "ⲙⲁ",  # lemma: ⲙⲉⲣⲉ, UD_pos: AUX
    "ⲙⲁ",  # lemma: ⲙⲉ, UD_pos: AUX
    "ⲙⲁⲣ",  # lemma: ⲙⲁⲣⲉ, UD_pos: AUX
    "ⲙⲁⲣⲉ",  # lemma: ⲙⲁⲣⲉ, UD_pos: AUX
    "ⲙⲉ",  # lemma: ⲙⲉⲣⲉ, UD_pos: AUX
    "ⲙⲉⲣⲉ",  # lemma: ⲙⲉ, UD_pos: AUX
    "ⲙⲙⲛ",  # lemma: ⲙⲛ, UD_pos: AUX
    "ⲙⲛ",  # lemma: ⲙⲛ, UD_pos: AUX
    "ⲙⲡ",  # lemma: ⲙⲡⲉ, UD_pos: AUX
    "ⲙⲡ",  # lemma: ⲙⲡ, UD_pos: AUX
    "ⲙⲡⲁⲧ",  # lemma: ⲙⲡⲁⲧⲉ, UD_pos: AUX
    "ⲙⲡⲁⲧⲉ",  # lemma: ⲙⲡⲁⲧⲉ, UD_pos: AUX
    "ⲙⲡⲉ",  # lemma: ⲙⲡⲉ, UD_pos: AUX
    "ⲙⲡⲣⲧⲣⲉ",  # lemma: ⲙⲡⲣⲧⲣⲉ, UD_pos: AUX
    "ⲛ",  # lemma: ⲛⲧⲉ, UD_pos: AUX
    "ⲛⲁ",  # lemma: ⲛⲁ, UD_pos: AUX
    "ⲛⲉ",  # lemma: ⲛⲉⲣⲉ, UD_pos: AUX
    "ⲛⲉ",  # lemma: ⲛⲉ, UD_pos: AUX
    "ⲛⲉⲣⲉ",  # lemma: ⲛⲉⲣⲉ, UD_pos: AUX
    "ⲛⲛ",  # lemma: ⲛⲛⲉ, UD_pos: AUX
    "ⲛⲛⲉ",  # lemma: ⲛⲛⲉ, UD_pos: AUX
    "ⲛⲧⲉ",  # lemma: ⲛⲧⲉ, UD_pos: AUX
    "ⲛⲧⲉⲣ",  # lemma: ⲛⲧⲉⲣⲉ, UD_pos: AUX
    "ⲛⲧⲉⲣⲉ",  # lemma: ⲛⲧⲉⲣⲉ, UD_pos: AUX
    "ⲟⲩⲛ",  # lemma: ⲟⲩⲛ, UD_pos: AUX
    "ⲧⲁⲣ",  # lemma: ⲧⲁⲣ, UD_pos: AUX
    "ⲧⲁⲣⲉ",  # lemma: ⲧⲁⲣⲉ, UD_pos: AUX
    "ⲩⲛ",  # lemma: ⲟⲩⲛ, UD_pos: AUX
    "ϩⲟⲧⲁⲛ",  # lemma: ϩⲟⲧⲁⲛ, UD_pos: CCONJ
    "ϩⲱⲥ",  # lemma: ϩⲱⲥ, UD_pos: CCONJ
    "ϩⲱⲥⲧⲉ",  # lemma: ϩⲱⲥⲧⲉ, UD_pos: CCONJ
    "ϫⲉ",  # lemma: ϫⲉ, UD_pos: CCONJ
    "ϫⲉⲕⲁⲁⲥ",  # lemma: ϫⲉⲕⲁⲁⲥ, UD_pos: CCONJ
    "ϫⲉⲕⲁⲁⲥ",  # lemma: ϫⲉⲕⲁⲥ, UD_pos: CCONJ
    "ϫⲉⲕⲁⲥ",  # lemma: ϫⲉⲕⲁⲥ, UD_pos: CCONJ
    "ϫⲉⲕⲁⲥ",  # lemma: ϫⲉⲕⲁⲁⲥ, UD_pos: CCONJ
    "ϫⲓ",  # lemma: ϫⲓ, UD_pos: CCONJ
    "ϫⲓⲛ",  # lemma: ϫⲓⲛ, UD_pos: CCONJ
    "ϫⲛ",  # lemma: ϫⲛ, UD_pos: CCONJ
    "ⲁⲗⲗⲁ",  # lemma: ⲁⲗⲗⲁ, UD_pos: CCONJ
    "ⲁⲩⲱ",  # lemma: ⲁⲩⲱ, UD_pos: CCONJ
    "ⲉϣϫⲉ",  # lemma: ⲉϣϫⲉ, UD_pos: CCONJ
    "ⲉϣⲱⲡⲉ",  # lemma: ⲉϣⲱⲡⲉ, UD_pos: CCONJ
    "ⲉⲓⲉ",  # lemma: ⲉⲓⲉ, UD_pos: CCONJ
    "ⲉⲓⲙⲏⲧⲓ",  # lemma: ⲉⲓⲙⲏⲧⲓ, UD_pos: CCONJ
    "ⲉⲓⲧⲉ",  # lemma: ⲉⲓⲧⲉ, UD_pos: CCONJ
    "ⲉⲛⲉ",  # lemma: ⲉⲛⲉ, UD_pos: CCONJ
    "ⲉⲡⲉⲓⲇⲏ",  # lemma: ⲉⲡⲉⲓⲇⲏ, UD_pos: CCONJ
    "ⲏ",  # lemma: ⲏ, UD_pos: CCONJ
    "ⲕⲁⲓ",  # lemma: ⲕⲁⲓ, UD_pos: CCONJ
    "ⲕⲁⲛ",  # lemma: ⲕⲁⲛ, UD_pos: CCONJ
    "ⲙⲉⲛ",  # lemma: ⲙⲉⲛ, UD_pos: CCONJ
    "ⲙⲏ",  # lemma: ⲙⲏ, UD_pos: CCONJ
    "ⲙⲏⲡⲟⲧⲉ",  # lemma: ⲙⲏⲡⲟⲧⲉ, UD_pos: CCONJ
    "ⲙⲏⲧⲓ",  # lemma: ⲙⲏⲧⲓ, UD_pos: CCONJ
    "ⲙⲙⲟⲛ",  # lemma: ⲙⲙⲟⲛ, UD_pos: CCONJ
    "ⲟⲩⲇⲉ",  # lemma: ⲟⲩⲇⲉ, UD_pos: CCONJ
    "ⲟⲩⲧⲉ",  # lemma: ⲟⲩⲧⲉ, UD_pos: CCONJ
    "ⲡⲗⲏⲛ",  # lemma: ⲡⲗⲏⲛ, UD_pos: CCONJ
    "ϩⲉⲛ",  # lemma: ⲟⲩ, UD_pos: DET
    "ϩⲛ",  # lemma: ϩⲛ, UD_pos: DET
    "ϭⲉ",  # lemma: ϭⲉ, UD_pos: DET
    "ϯ",  # lemma: ⲡⲓ, UD_pos: DET
    "ϯ",  # lemma: ϯ, UD_pos: DET
    "ⲕⲉ",  # lemma: ⲕⲉ, UD_pos: DET
    "ⲙ",  # lemma: ⲡ, UD_pos: DET
    "ⲙ",  # lemma: ⲛ, UD_pos: DET
    "ⲛ",  # lemma: ⲡ, UD_pos: DET
    "ⲛ",  # lemma: ⲛ, UD_pos: DET
    "ⲛⲁ",  # lemma: ⲡⲁ, UD_pos: DET
    "ⲛⲁ",  # lemma: ⲡⲉ, UD_pos: DET
    "ⲛⲁ",  # lemma: ⲛⲁ, UD_pos: DET
    "ⲛⲁⲓ",  # lemma: ⲡⲁⲓ, UD_pos: DET
    "ⲛⲁⲓ",  # lemma: ⲛⲁⲓ, UD_pos: DET
    "ⲛⲉ",  # lemma: ⲡ, UD_pos: DET
    "ⲛⲉ",  # lemma: ⲛⲉⲣⲉ, UD_pos: DET
    "ⲛⲉ",  # lemma: ⲛ, UD_pos: DET
    "ⲛⲉϥ",  # lemma: ⲡⲉϥ, UD_pos: DET
    "ⲛⲉⲓ",  # lemma: ⲡⲉⲓ, UD_pos: DET
    "ⲛⲉⲕ",  # lemma: ⲡⲉⲕ, UD_pos: DET
    "ⲛⲉⲛ",  # lemma: ⲡⲉⲛ, UD_pos: DET
    "ⲛⲉⲥ",  # lemma: ⲡⲉⲥ, UD_pos: DET
    "ⲛⲉⲧⲛ",  # lemma: ⲡⲉⲧⲛ, UD_pos: DET
    "ⲛⲉⲩ",  # lemma: ⲡⲉⲩ, UD_pos: DET
    "ⲛⲏ",  # lemma: ⲡⲏ, UD_pos: DET
    "ⲛⲓ",  # lemma: ⲡⲓ, UD_pos: DET
    "ⲛⲟⲩ",  # lemma: ⲡⲟⲩ, UD_pos: DET
    "ⲟⲩ",  # lemma: ⲟⲩ, UD_pos: DET
    "ⲟⲩ",  # lemma: ⲛⲧⲟⲟⲩ, UD_pos: DET
    "ⲡ",  # lemma: ⲡ, UD_pos: DET
    "ⲡⲁ",  # lemma: ⲡⲁ, UD_pos: DET
    "ⲡⲁⲓ",  # lemma: ⲡⲁⲓ, UD_pos: DET
    "ⲡⲉ",  # lemma: ⲡ, UD_pos: DET
    "ⲡⲉ",  # lemma: ⲡⲉ, UD_pos: DET
    "ⲡⲉϥ",  # lemma: ⲡⲉϥ, UD_pos: DET
    "ⲡⲉϥ",  # lemma: ⲡ, UD_pos: DET
    "ⲡⲉⲓ",  # lemma: ⲡⲉⲓ, UD_pos: DET
    "ⲡⲉⲕ",  # lemma: ⲡⲉⲕ, UD_pos: DET
    "ⲡⲉⲛ",  # lemma: ⲡⲉⲛ, UD_pos: DET
    "ⲡⲉⲥ",  # lemma: ⲡⲉⲥ, UD_pos: DET
    "ⲡⲉⲧⲛ",  # lemma: ⲡⲉⲧⲛ, UD_pos: DET
    "ⲡⲉⲩ",  # lemma: ⲡⲉⲩ, UD_pos: DET
    "ⲡⲏ",  # lemma: ⲡⲏ, UD_pos: DET
    "ⲡⲓ",  # lemma: ⲡⲓ, UD_pos: DET
    "ⲡⲓ",  # lemma: ⲡⲉⲓ, UD_pos: DET
    "ⲡⲟⲩ",  # lemma: ⲡⲟⲩ, UD_pos: DET
    "ⲡⲱⲕ",  # lemma: ⲡⲱⲕ, UD_pos: DET
    "ⲡⲱⲧⲛ",  # lemma: ⲡⲱⲧⲛ, UD_pos: DET
    "ⲧ",  # lemma: ⲡ, UD_pos: DET
    "ⲧ",  # lemma: ⲧ, UD_pos: DET
    "ⲧⲁ",  # lemma: ⲡⲁ, UD_pos: DET
    "ⲧⲁⲓ",  # lemma: ⲡⲁⲓ, UD_pos: DET
    "ⲧⲉ",  # lemma: ⲡ, UD_pos: DET
    "ⲧⲉϥ",  # lemma: ⲡⲉϥ, UD_pos: DET
    "ⲧⲉⲓ",  # lemma: ⲡⲉⲓ, UD_pos: DET
    "ⲧⲉⲕ",  # lemma: ⲡⲉⲕ, UD_pos: DET
    "ⲧⲉⲛ",  # lemma: ⲡⲉⲛ, UD_pos: DET
    "ⲧⲉⲥ",  # lemma: ⲡⲉⲥ, UD_pos: DET
    "ⲧⲉⲧⲛ",  # lemma: ⲡⲉⲧⲛ, UD_pos: DET
    "ⲧⲉⲩ",  # lemma: ⲡⲉⲩ, UD_pos: DET
    "ⲧⲟⲩ",  # lemma: ⲡⲟⲩ, UD_pos: DET
    "ⲩ",  # lemma: ⲟⲩ, UD_pos: DET
    "ⲩ",  # lemma: ⲛⲧⲟⲟⲩ, UD_pos: DET
    "ϥ",  # lemma: ⲛⲧⲟϥ, UD_pos: PRON
    "ϩⲱ",  # lemma: ϩⲱⲱ_ⲁⲛⲟⲕ, UD_pos: PRON
    "ϯ",  # lemma: ⲁⲛⲟⲕ, UD_pos: PRON
    "ϯ",  # lemma: ϯ, UD_pos: PRON
    "ⲁ",  # lemma: ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲁ",  # lemma: ⲁ, UD_pos: PRON
    "ⲁ",  # lemma: ⲛⲧⲟ, UD_pos: PRON
    "ⲁϣ",  # lemma: ⲁϣ, UD_pos: PRON
    "ⲁⲛⲅ",  # lemma: ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲁⲛⲟⲕ",  # lemma: ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲁⲛⲟⲛ",  # lemma: ⲁⲛⲟⲛ, UD_pos: PRON
    "ⲁⲟⲩⲏⲣ",  # lemma: ⲁⲟⲩⲏⲣ, UD_pos: PRON
    "ⲁⲣ",  # lemma: ⲁ_ⲛⲧⲟ, UD_pos: PRON
    "ⲅ",  # lemma: ⲛⲧⲟⲕ, UD_pos: PRON
    "ⲅ",  # lemma: ⲅ, UD_pos: PRON
    "ⲉ",  # lemma: ⲛⲧⲟ, UD_pos: PRON
    "ⲉϥ",  # lemma: ⲉϥ, UD_pos: PRON
    "ⲉϥϣⲁⲛ",  # lemma: ⲉⲣϣⲁⲛ_ⲛⲧⲟϥ, UD_pos: PRON
    "ⲉϥⲉ",  # lemma: ⲉⲣⲉ_ⲛⲧⲟϥ, UD_pos: PRON
    "ⲉⲓ",  # lemma: ⲉⲓ, UD_pos: PRON
    "ⲉⲓ",  # lemma: ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲉⲓϣⲁⲛ",  # lemma: ⲉⲣϣⲁⲛ_ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲉⲓⲉ",  # lemma: ⲉⲣⲉ_ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲉⲕϣⲁⲛ",  # lemma: ⲉⲣϣⲁⲛ_ⲛⲧⲟⲕ, UD_pos: PRON
    "ⲉⲕⲉ",  # lemma: ⲉⲕⲉ, UD_pos: PRON
    "ⲉⲛϣⲁⲛ",  # lemma: ⲉⲣϣⲁⲛ_ⲁⲛⲟⲛ, UD_pos: PRON
    "ⲉⲛⲉ",  # lemma: ⲉⲛⲉ, UD_pos: PRON
    "ⲉⲛⲉ",  # lemma: ⲉⲣⲉ_ⲁⲛⲟⲛ, UD_pos: PRON
    "ⲉⲣ",  # lemma: ⲉⲣⲉ_ⲛⲧⲟ, UD_pos: PRON
    "ⲉⲣⲉ",  # lemma: ⲉⲣⲉ_ⲛⲧⲟ, UD_pos: PRON
    "ⲉⲣⲉ",  # lemma: ⲉⲣⲉ, UD_pos: PRON
    "ⲉⲣⲟ",  # lemma: ⲉ_ⲛⲧⲟ, UD_pos: PRON
    "ⲉⲥ",  # lemma: ⲉⲥ, UD_pos: PRON
    "ⲉⲧⲉⲧⲛϣⲁⲛ",  # lemma: ⲉⲧⲉⲧⲛϣⲁⲛ, UD_pos: PRON
    "ⲉⲧⲉⲧⲛϣⲁⲛ",  # lemma: ⲉⲣϣⲁⲛ_ⲛⲧⲱⲧⲛ, UD_pos: PRON
    "ⲉⲧⲉⲧⲛⲉ",  # lemma: ⲉⲣⲉ_ⲛⲧⲱⲧⲛ, UD_pos: PRON
    "ⲉⲩϣⲁⲛ",  # lemma: ⲉⲣϣⲁⲛ_ⲛⲧⲟⲟⲩ, UD_pos: PRON
    "ⲉⲩⲉ",  # lemma: ⲉⲣⲉ_ⲛⲧⲟⲟⲩ, UD_pos: PRON
    "ⲓ",  # lemma: ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲕ",  # lemma: ⲛⲧⲟⲕ, UD_pos: PRON
    "ⲕ",  # lemma: ⲕ, UD_pos: PRON
    "ⲕ",  # lemma: ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲙⲙⲟ",  # lemma: ⲛ_ⲛⲧⲟ, UD_pos: PRON
    "ⲛ",  # lemma: ⲁⲛⲟⲛ, UD_pos: PRON
    "ⲛ",  # lemma: ⲡⲉ, UD_pos: PRON
    "ⲛ",  # lemma: ⲡ, UD_pos: PRON
    "ⲛ",  # lemma: ⲛ, UD_pos: PRON
    "ⲛ",  # lemma: ⲛⲧⲉ, UD_pos: PRON
    "ⲛϩⲏⲧ",  # lemma: ϩⲛ, UD_pos: PRON
    "ⲛϩⲏⲧ",  # lemma: ϩⲛ_ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲛⲉ",  # lemma: ⲡⲉ, UD_pos: PRON
    "ⲛⲉⲣ",  # lemma: ⲛⲉⲣⲉ_ⲛⲧⲟ, UD_pos: PRON
    "ⲛⲓⲙ",  # lemma: ⲛⲓⲙ, UD_pos: PRON
    "ⲛⲧⲉⲧⲛ",  # lemma: ⲛⲧⲱⲧⲛ, UD_pos: PRON
    "ⲛⲧⲉⲧⲛ",  # lemma: ⲛⲧⲉⲧⲛ, UD_pos: PRON
    "ⲛⲧⲕ",  # lemma: ⲛⲧⲟⲕ, UD_pos: PRON
    "ⲛⲧⲟ",  # lemma: ⲛⲧⲟ, UD_pos: PRON
    "ⲛⲧⲟϥ",  # lemma: ⲛⲧⲟϥ, UD_pos: PRON
    "ⲛⲧⲟⲕ",  # lemma: ⲛⲧⲟⲕ, UD_pos: PRON
    "ⲛⲧⲟⲟⲩ",  # lemma: ⲛⲧⲟⲟⲩ, UD_pos: PRON
    "ⲛⲧⲟⲥ",  # lemma: ⲛⲧⲟⲥ, UD_pos: PRON
    "ⲛⲧⲱⲧⲛ",  # lemma: ⲛⲧⲱⲧⲛ, UD_pos: PRON
    "ⲟⲩ",  # lemma: ⲟⲩ, UD_pos: PRON
    "ⲟⲩ",  # lemma: ⲛⲧⲟⲟⲩ, UD_pos: PRON
    "ⲟⲩⲏⲣ",  # lemma: ⲟⲩⲏⲣ, UD_pos: PRON
    "ⲡ",  # lemma: ⲡⲉ, UD_pos: PRON
    "ⲡ",  # lemma: ⲡ, UD_pos: PRON
    "ⲡⲉ",  # lemma: ⲡⲉ, UD_pos: PRON
    "ⲣⲁⲧ",  # lemma: ⲣⲁⲧ_ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲣⲱ",  # lemma: ⲣⲟ, UD_pos: PRON
    "ⲥ",  # lemma: ⲛⲧⲟⲥ, UD_pos: PRON
    "ⲥϥ",  # lemma: ⲛⲧⲟϥ, UD_pos: PRON
    "ⲥϥ",  # lemma: ⲥϥ, UD_pos: PRON
    "ⲥⲉ",  # lemma: ⲛⲧⲟⲟⲩ, UD_pos: PRON
    "ⲥⲉ",  # lemma: ⲥⲉ, UD_pos: PRON
    "ⲥⲟⲩ",  # lemma: ⲛⲧⲟⲟⲩ, UD_pos: PRON
    "ⲧ",  # lemma: ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲧ",  # lemma: ⲡⲉ, UD_pos: PRON
    "ⲧⲁ",  # lemma: ⲛⲧⲉ_ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲧⲁ",  # lemma: ⲁⲛⲟⲕ, UD_pos: PRON
    "ⲧⲁ",  # lemma: ⲁⲛⲟⲕ_ⲛⲧⲉ, UD_pos: PRON
    "ⲧⲁ",  # lemma: ⲡⲁ, UD_pos: PRON
    "ⲧⲉ",  # lemma: ⲡⲉ, UD_pos: PRON
    "ⲧⲉ",  # lemma: ⲛⲧⲟ, UD_pos: PRON
    "ⲧⲉⲧ",  # lemma: ⲛⲧⲱⲧⲛ, UD_pos: PRON
    "ⲧⲉⲧ",  # lemma: ⲧⲉⲧ, UD_pos: PRON
    "ⲧⲉⲧⲛ",  # lemma: ⲛⲧⲱⲧⲛ, UD_pos: PRON
    "ⲧⲉⲧⲛ",  # lemma: ⲧⲉⲧⲛ, UD_pos: PRON
    "ⲧⲏⲩⲧⲛ",  # lemma: ⲛⲧⲱⲧⲛ, UD_pos: PRON
    "ⲧⲛ",  # lemma: ⲁⲛⲟⲛ, UD_pos: PRON
    "ⲧⲛ",  # lemma: ⲛⲧⲱⲧⲛ, UD_pos: PRON
    "ⲧⲱⲛ",  # lemma: ⲧⲱⲛ, UD_pos: PRON
    "ⲩ",  # lemma: ⲛⲧⲟⲟⲩ, UD_pos: PRON
    "ⲉ",  # lemma: ⲉⲣⲉ, UD_pos: SCONJ
    "ⲉ",  # lemma: ⲉⲧⲉⲣⲉ, UD_pos: SCONJ
    "ⲉ",  # lemma: ⲉ, UD_pos: SCONJ
    "ⲉ",  # lemma: ⲉⲧⲉ, UD_pos: SCONJ
    "ⲉⲛⲧ",  # lemma: ⲉⲧⲉⲣⲉ, UD_pos: SCONJ
    "ⲉⲣⲉ",  # lemma: ⲉⲣⲉ, UD_pos: SCONJ
    "ⲉⲧ",  # lemma: ⲉⲧⲉⲣⲉ, UD_pos: SCONJ
    "ⲉⲧ",  # lemma: ⲉⲧ, UD_pos: SCONJ
    "ⲉⲧ",  # lemma: ⲉⲧⲉ, UD_pos: SCONJ
    "ⲉⲧⲉ",  # lemma: ⲉⲧⲉⲣⲉ, UD_pos: SCONJ
    "ⲉⲧⲉ",  # lemma: ⲉⲧⲉ, UD_pos: SCONJ
    "ⲉⲧⲉⲣⲉ",  # lemma: ⲉⲧⲉⲣⲉ, UD_pos: SCONJ
    "ⲛⲧ",  # lemma: ⲉⲧⲉⲣⲉ, UD_pos: SCONJ
]
