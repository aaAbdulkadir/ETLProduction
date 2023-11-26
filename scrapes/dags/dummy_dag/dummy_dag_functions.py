def extract(url: str, output_file: str) -> None:
    import pandas as pd
    import logging

    logger = logging.getLogger('extract')

    df = pd.read_html(url)[0]
    df.to_csv(output_file, index=False)

    logger.info(f'EXTRACTED {output_file}')

def transform(input_filename: str, output_filename: str) -> None:
    import pandas as pd
    import logging

    from dummy_dag_helper_functions import change_data_types

    logger = logging.getLogger('transform')

    df = pd.read_csv(input_filename)
    df = df[df['Player'] != 'Player'].iloc[:, :4]

    df = change_data_types(df)
    df.to_csv(output_filename, index=False)
    
    logger.info(f'TRANSFORMED {output_filename}')