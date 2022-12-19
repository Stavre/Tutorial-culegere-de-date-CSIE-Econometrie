import eurostat
import pandas as pd

def getEurostatDatasets(keyword=None, save=False):
    """keyword: string, used for searching datasets"""
    # get a list of all eurostat datasets
    toc_df = eurostat.get_toc_df()
    result = toc_df
    if keyword is not None:
        result = eurostat.subset_toc_df(toc_df, keyword)

    if save:
        result.to_csv('eurostat_datasets_searchword'+keyword+".csv")

    return result

def getEurostatDataset(code: str, save_with_name=None, with_labels=True ):
    """
    :param code: str - dataset's code, can be found on eurostat website
    :param save_with_name: - if given, the pandas dataframe will be saved as a csv file : save_with_name.csv
    :return: a pandas dataframe containing the dataset
    """
    df = eurostat.get_data_df(code, flags=False, verbose=True)
    metadata = dict()
    columns = eurostat.get_pars(code)

    df['geo'] = df['geo\TIME_PERIOD']

    if with_labels:

        for column in columns:
            # print(column, eurostat.get_dic(code, column))
            column_metadata = list(zip(*eurostat.get_dic(code, column)))
            for index, value in enumerate(column_metadata[0]):
                metadata[value] = column_metadata[1][index]

            df[column + '(Expanded)'] = df[column].map(metadata)

    if save_with_name is not None:
        df.to_csv(save_with_name+".csv", index=False)
    return df

def wide_to_long(dataframe: pd.DataFrame, value_vars, var_name,  value_name): #df.melt
    '''
    id_vars[tuple, list, or ndarray, optional] : Column(s) to use as identifier variables.
    value_vars[tuple, list, or ndarray, optional]: Column(s) to unpivot. If not specified, uses all columns that are not set as id_vars.
    var_name[scalar]: Name to use for the ‘variable’ column. If None it uses frame.columns.name or ‘variable’.
    value_name[scalar, default ‘value’]: Name to use for the ‘value’ column.
    col_level[int or string, optional]: If columns are a MultiIndex then use this level to melt
    '''
    # df_long = pd.melt(df_wide, value_vars=year_list,value_name='Avg. Price ($)', ignore_index=False)
    id_vars = [x for x in dataframe.columns if x not in value_vars]
    return pd.melt(dataframe, id_vars=id_vars,  value_vars=value_vars, var_name=var_name, value_name=value_name, ignore_index=False)


def long_to_wide(dataframe: pd.DataFrame, cols, values):
    '''
    :param dataframe: dataframe to convert from long to wide
    :param cols: Column    to    use    to    make    new    frame’s    columns
    :param values: Column(s)    to    use    for populating new frame’s values
    :return:
    '''
    return pd.pivot(dataframe,  columns=cols, values=values)


# download a dataset
code = 'AACT_EAA01'
df = getEurostatDataset(code, save_with_name=code)


cols = ['freq', 'unit', 's_adj', 'na_item', 'geo\TIME_PERIOD']

cols_for_pivoting = [x for x in df.columns if x not in cols]
f = wide_to_long(df, cols_for_pivoting, 'year', 'Value')
f.to_csv(code + 'query_melt.csv', index=False)

# pentru join (ca în SQL) vezi https://pandas.pydata.org/docs/user_guide/merging.html#database-style-dataframe-or-named-series-joining-merging
# pentru a schimba structura datelor vezi https://pandas.pydata.org/docs/user_guide/reshaping.html#reshaping-by-melt
# și https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html#pandas.DataFrame.pivot

