#!/usr/bin/env python3

"""
Variance.py prints "Hello world!"

Usage:
    python3 Variance.py
"""

import re
import argparse
import pandas as pd
from typing import cast, List
from dataclasses import dataclass

@dataclass
class AASubstitution:
    full_name: str
    protein: str
    ref_allele: str
    codon: int
    alt_allele: str


def parse_amino_acid_subs(mutation: str) -> AASubstitution:

    assert "_" in mutation, f"Gene/protein name is not parseable in the mutation {mutation} via the '_' symbol as expected."
    # write assertion about our assumption that there's only one underscore
    ref, codon_str, alt = re.match(r"([a-zA-Z]+)(\d+)([a-zA-Z]+)", mutation.split("_")[1]).groups()
    new_sub = AASubstitution(
        full_name=mutation,
        protein=mutation.split("_")[0],
        ref_allele=ref,
        codon=cast(int, codon_str),
        alt_allele=alt
    )

    return new_sub

def process_mutation_cell(s: str, b: bool = True) -> List[AASubstitution]:

    if pd.isna(s) or s is None:
        return None
        
    muts = s.strip('()').split(',')

    if b == False:
        return muts
    
    mut_strings = s.strip('()').split(',')
    substitutions = [parse_amino_acid_subs(mut) for mut in mut_strings]

    return substitutions

def parse_cmd_line_args():
    parser =  argparse.ArgumentParser()
    parser.add_argument(
        '--input_file', 
        '-i',
        type = str,
        required = True,
        help = 'File to read from.'
    )
    
    parser.add_argument(
        '--output_file', 
        '-o',
        type = str,
        required = True,
        help = 'File to read to.'
    )
    args = parser.parse_args()
    return args.input_file,  args.output_file



def main() -> None:
    """
        Assembles a dataframe highlighting highest locations of mutations
        and mutation type
    
    Args:
        No arguments
    
    Returns:
        None
    """
    
    input_file, output_file = parse_cmd_line_args()

    original = pd.read_csv(input_file, delimiter = '\t', na_values=["", "()", "NA", "unknown"])

    mutations = original[['AA Substitutions']]
    mutations = mutations['AA Substitutions'].apply(process_mutation_cell)
    mutations = mutations.explode('AA Substitutions').to_frame()
    mutations = mutations['AA Substitutions'].apply(lambda x: pd.Series([x.full_name, x.protein, x.ref_allele, x.codon, x.alt_allele] if x else [None, None, None, None, None]))
    mutations.columns = ['Name', 'Protein',  'Reference', 'Codon', 'Mutation']
    mutations = mutations.dropna()
    mutations = mutations.groupby(['Name', 'Protein',  'Reference', 'Codon', 'Mutation']).size().reset_index(name = 'Count')
    mutations = mutations.sort_values(by = ['Count'], ascending = False)

    mutations.to_excel(output_file, index  = False)
    print(mutations)





if __name__ == "__main__":
    main()
