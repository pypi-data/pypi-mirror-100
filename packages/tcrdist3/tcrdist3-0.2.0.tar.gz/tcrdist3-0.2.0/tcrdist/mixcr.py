# mixcr.py
import os 
import numpy as np
import pandas as pd
import re

def mixcr_to_tcrdist3(chain:str, 
                      organism:str, 
                      seqs_fn:str = None, 
                      clones_fn:str = None):
    """
    Converts .clns.txt or .result.txt outputs from mixcr to tcrdist formatted input. 

    Parameters 
    ----------
    chain : str
        'alpha', 'beta', 'gamma', or 'delta'
    organism : str
        'human' or 'mouse"
    seqs_fn : str or None
        path to mixcr parses sequences files which can contain duplicates
    clones_fn : str or None
        path to mixcr parsed clones file (.clns.txt), clones have a clone_id and count

    Returns
    -------
    df : pd.DataFrame
        DataFrame with column names specified in notes. 
    Notes
    -----
    A seq_fn or clones_fn may be passed as input but not both.

    Columns of output `df` are:

    "v_[abgd]_gene", "d_[abgd]_gene:, "j_[abgd]_gene", 
    "cdr3_d_nucseq", "cdr3_d_nucseq" where [abgd] matches the 
    chain argument. 
    
    If clones_fn is specifed, the df returned will contain 
    "clone_id" and "count" columns                                           
    """
    if seqs_fn is not None and clones_fn is not None:
        raise ValueError ("one of seq_fn or clones_fn must be left blank")
    if seqs_fn is None and clones_fn is None:
        raise ValueError ("one of seq_fn or clones_fn must be provided")
        
    
    gene_names = {  'alpha': ['v_a_gene','d_a_gene','j_a_gene',"cdr3_a_nucseq","cdr3_a_aa"],
                    'beta' : ['v_b_gene','d_b_gene','j_b_gene',"cdr3_b_nucseq","cdr3_b_aa"],
                    'gamma': ['v_g_gene','d_g_gene','j_g_gene',"cdr3_g_nucseq","cdr3_g_aa"],
                    'delta': ['v_d_gene','d_d_gene','j_d_gene',"cdr3_d_nucseq","cdr3_d_aa"]}
    
    if chain not in gene_names.keys():
        raise KeyError ("chain must be 'alpha','beta','gamma', or 'delta'")
    
    if seqs_fn is not None:
        seqs_df   = pd.read_csv(seqs_fn, "\t")
        seqs_df   = seqs_df[['allVHitsWithScore','allDHitsWithScore', 'allJHitsWithScore', 'nSeqCDR3','aaSeqCDR3']].copy()
        for k in ['allVHitsWithScore','allDHitsWithScore', 'allJHitsWithScore']:
            # cleanup see function defintioins above (take only the top hit and convert allele *00 to *01)
            seqs_df[k] = seqs_df[k].apply(_take_top_mixcr_gene_hit).\
                apply(_allele_00_to_01).\
                apply(_change_TRAVDV_to_TRAVdashDV)

        seqs_df   = seqs_df.rename(columns = {  'allVHitsWithScore' : gene_names[chain][0],                    
                                                'allDHitsWithScore' : gene_names[chain][1], 
                                                'allJHitsWithScore' : gene_names[chain][2],
                                                'nSeqCDR3'          : gene_names[chain][3],
                                                'aaSeqCDR3'         : gene_names[chain][4]})
        df = seqs_df.copy()

    elif clones_fn is not None:
        clones_df = pd.read_csv(clones_fn, "\t")
        clones_df = clones_df[['cloneId', 'cloneCount','allVHitsWithScore','allDHitsWithScore', 'allJHitsWithScore', 'nSeqCDR3','aaSeqCDR3']].copy()
        for k in ['allVHitsWithScore','allDHitsWithScore', 'allJHitsWithScore']:
            # cleanup see function defintioins above (take only the top hit and convert allele *00 to *01)
            clones_df[k] = clones_df[k].apply(_take_top_mixcr_gene_hit).\
                apply(_allele_00_to_01).\
                apply(_change_TRAVDV_to_TRAVdashDV)

        clones_df = clones_df.rename(columns = {    'cloneId'           : "clone_id",
                                                    'cloneCount'        : "count",
                                                    'allVHitsWithScore' : gene_names[chain][0],                    
                                                    'allDHitsWithScore' : gene_names[chain][1], 
                                                    'allJHitsWithScore' : gene_names[chain][2],
                                                    'nSeqCDR3'          : gene_names[chain][3],
                                                    'aaSeqCDR3'         : gene_names[chain][4]})
        df = clones_df.copy()
    
    return(df)


def remove_entries_with_invalid_vgene(df, chain:str,organism:str):
    """
    Uses _validate_gene_names to remove cells, or clones rows that lack a valid v_gene name
    
    This is based on checking gene name against:
    repertoire_db.RefGeneSet(db_file = "gammadelta_db.tsv" OR "alphabesta_db.tsv).all_genes

    It also removes genes not associated with the specified chain 

    Reports any gene names deemed invalid

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame produced by mixcr.mixcr_to_tcrdist2
    chain : str
        'alpha', 'beta', 'gamma', or 'delta'
    organism : str
        'human' or 'mouse"
    

    Returns 
    -------
    df : pd.DataFrame
        a copied subset of the orginal dataframe containing only those rows with valid v gene names
    """ 
    gene_names = {  'alpha': ['v_a_gene','d_a_gene','j_a_gene'],
                    'beta' : ['v_b_gene','d_b_gene','j_b_gene'],
                    'gamma': ['v_g_gene','d_g_gene','j_g_gene'],
                    'delta': ['v_d_gene','d_d_gene','j_d_gene']}
    
    v = _validate_gene_names(series = df[gene_names[chain][0]], chain = chain, organism = organism)
    n_invalid_v_names = df[v == False].shape[0]
    invalid_names =df[v == False][gene_names[chain][0]].unique()

    if n_invalid_v_names > 0:
        sys.stderr.write(f"Because of invalid v_gene names, dropping {n_invalid_v_names} with names:\n")
        for n in invalid_names:
            sys.stderr.write(f"{n}\n")
    
    return df[v].copy()

def _valid_cdr3(cdr3):
    """
    Examples
    --------
    >>> _valid_cdr3("AAAA")
    True
    >>> _valid_cdr3("AA.A")
    False
    """
    amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    valid = np.all([aa in amino_acids for aa in cdr3])
    return valid

def remove_entries_with_invalid_cdr3(df, chain:str):

    chain_names = { 'alpha': 'cdr3_a_aa',
                    'beta' : 'cdr3_b_aa',
                    'gamma': 'cdr3_g_aa',
                    'delta': 'cdr3_d_aa',}
   
    cdr3_x_aa = chain_names[chain]
    print(cdr3_x_aa)
    v = df[cdr3_x_aa].apply(lambda x : _valid_cdr3(x))

    n_invalid_cdr3 = df[v == False].shape[0]
    invalid_names =df[v == False][cdr3_x_aa].unique()
   
    warnings.warn(f"Because of invalid cdr3a names, dropping {n_invalid_cdr3}: {invalid_names}\n")
   
    return df[v].copy()
    
def _change_TRAVDV_to_TRAVdashDV(s:str):
    """
    Reconciles mixcr name like TRAV29/DV5*01 to tcrdist2 name TRAV29DV5*01
    
    Parameters
    ----------
    s : str
    
    Examples
    --------
    >>> _change_TRAVDV_to_TRAVdashDV('TRAV29DV5*01')
    'TRAV29/DV5*01'
    >>> _change_TRAVDV_to_TRAVdashDV('TRAV38-2DV8*01')
    'TRAV38-2/DV8*01'
    >>> _change_TRAVDV_to_TRAVdashDV('TRDV*01')
    'TRDV*01'

    Notes
    -----
    This reconciles such gene names to match the tcrdist2 reference db.

    see database for more details: repertoire_db.RefGeneSet(db_file = "gammadelta_db.tsv").all_genes
    """
    if isinstance(s, str):
        m = re.match(pattern = "(TRAV[0-9]+)(DV.*)", string = s)
        m2 = re.match(pattern = "(TRAV[0-9]+-[1-2])(DV.*)", string = s)
        if m:
            new_s = "/".join(m.groups())
            return(new_s)
        elif m2:
            new_s = "/".join(m2.groups())
            return(new_s)
        else:
            return(s)   
    else:
        return(np.NaN)

def _allele_00_to_01(s:str):
    """
    Converts gene names from X*00 to X*01

    Parameters
    ----------
    s : str

    Example
    -------
    >>> _allele_00_to_01('TRDD3*00')
    'TRDD3*01'
    """
    if isinstance(s, str):
        allele01 = s.replace("*00","*01")
    else:
        allele01 = np.NaN   
    return(allele01)

def _take_top_mixcr_gene_hit(s):
    """
    Parameters 
    ----------
    
    s : str

    Examples
    --------
    >> _take_top_mixcr_gene_hit('TRDD3*00(45),TRDD2*00(40)')
    'TRDD3*00'
    >> _take_top_mixcr_gene_hit('TRDD3*00(45)')
    'TRDD3*00'
    >> _take_top_mixcr_gene_hit(None)
    None

    Tests
    -----
    assert _take_top_mixcr_gene_hit('TRDD3*00(45),TRDD2*00(40)') == 'TRDD3*00'
    assert _take_top_mixcr_gene_hit('TRDD3*00(45)') == 'TRDD3*00'
    assert isinstance(_take_top_mixcr_gene_hit(np.NaN),float)
    assert _take_top_mixcr_gene_hit(np.NaN) is np.NaN
    """
    if isinstance(s, str):
        top_hit = s.split(",")[0].split("(")[0]
    else:
        top_hit = np.NaN   
    return(top_hit)
