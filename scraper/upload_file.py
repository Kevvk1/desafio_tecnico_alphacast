from alphacast import Alphacast



def upload_file(alphacast_api_key, df, repo_id, dataset_name, description):

    alphacast = Alphacast(alphacast_api_key) 

    try:
        dataset = alphacast.datasets.create(dataset_name,repo_id,description)

        dataset_id = dataset["id"]

        #Inicializo columnas (definir entidades y fecha)
        alphacast.datasets.dataset(dataset_id).initialize_columns(
            dateColumnName="Date",
            entitiesColumnNames=["Region", "Product", "Unit"],
            dateFormat="%Y-%m-%d"
        )

        #Subo los datos desde el DataFrame
        alphacast.datasets.dataset(dataset_id).upload_data_from_df(
            df,
            deleteMissingFromDB=False,       # No borra lo anterior que no está en este df
            onConflictUpdateDB=True,         # Actualiza si el dato ya existe (por fecha + entidades)
            uploadIndex=False
        )

        print(f"✅ Dataset '{dataset['name']}' subido correctamente.")
        return dataset
    
    except Exception as e:
        print(f"❌ Error al subir el dataset: {e}")
        return None



