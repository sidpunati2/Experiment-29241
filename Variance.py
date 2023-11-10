#!/usr/bin/env python3

"""
Variance.py prints "Hello world!"

Usage:
    python3 Variance.py
"""

def main() -> None:
    """
        Assembles a dataframe highlighting highest locations of mutations
        and mutation type
    
    Args:
        No arguments
    
    Returns:
        None
    """

    import pandas as pd
    
    def parse(s: str, b: bool = True) -> []:
        hold = []
        current = []
        abuild = None
        nbuild = None

        if s == '()' or s == None:
            return [[None, None, None, None]]
        
        muts = s.strip('()').split(',')

        if b == False:
            return muts

        for mut in muts:
            current.append(mut)
            for v in mut:
                if v == '_':
                    current.append(abuild)
                    abuild = None
                elif v.isalpha():
                    if abuild == None:
                        abuild = v
                        continue
                    if nbuild != None:
                        current.append(abuild)
                        abuild = v
                        nbuild = None
                        continue
                    abuild = abuild + v
                elif v.isdigit():
                    if nbuild == None:
                        nbuild = v
                        abuild = abuild + v
                        continue
                    nbuild = nbuild + v
                    abuild = abuild + v
            current.append(abuild)
            hold.append(current)
            current = []
            abuild = None

        return hold
        
    original = pd.read_csv('africa_high_distance_candidates.tsv', delimiter = '\t')
    dic = {}

    mutations = original[['AA Substitutions']]
    mutations['mutations'] = mutations['AA Substitutions'].apply(parse)

    for i in range(len(mutations['mutations'])):
        for mut in mutations['mutations'][i]:
                print(mut)
                name, pro, orig, sub = mut
                if name not in dic.keys():
                    break





if __name__ == "__main__":
    main()
