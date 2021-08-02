from pathlib import Path

from datetime import datetime
import networkx as nx
import pandas as pd

def read_konect_timestamp(stamp):
    return datetime.fromtimestamp(float(stamp))
    

def load_konect(path):
    with open(path) as f:
        non_comment = filter(lambda x: not x.startswith('%'), f)
        return nx.parse_edgelist(non_comment, create_using=nx.DiGraph, data=[('weight', float), ('time', read_konect_timestamp)])


def load_dataset(dataset_name: str):
    '''
    This function is responsible of receiving the dataset name and access the right folder, read and create the graph.
    Args:
        dataset_name: str - the name of the graph dataset

    Returns:
        graph_nx: networkx - graph of the dataset with all needed attributes
        folder_path: str - the path to the dataset folder, in order to dump files in it
    '''
    folder_path = Path("../data") / dataset_name
    dump_folder = folder_path / "dump"

    if dataset_name == 'PPI':
        graph_path = folder_path / "interactions_with_dates.csv"
        graph_df = pd.read_csv(graph_path, sep=',', usecols=[
                               'id1', 'id2', 'discovery date'])
        graph_df = graph_df[~pd.isnull(graph_df['discovery date'])]
        graph_df['time'] = graph_df['discovery date'].map(
            lambda x: eval(x).year)
        graph_df.rename({'id1': 'from', 'id2': 'to'},
                        axis='columns', inplace=True)
        graph_nx = nx.from_pandas_edgelist(graph_df, 'from', 'to', edge_attr=[
                                           'time'], create_using=nx.Graph())
    elif dataset_name.endswith('_konect'):
        datafile = f'out.{dataset_name[:-len("_konect")]}'
        graph_nx = load_konect(folder_path / datafile)
    else:
        raise Exception('dataset not available')

    dump_folder.mkdir(exist_ok=True)

    return graph_nx, dump_folder


def df2graph(graph_df, source, target, time, create_using=nx.Graph()):
    return nx.from_pandas_edgelist(graph_df, source, target, edge_attr=[time], create_using=create_using)
