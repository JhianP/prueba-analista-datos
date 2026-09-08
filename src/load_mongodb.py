from pathlib import Path
import pandas as pd
from pymongo import MongoClient, ASCENDING


# ---------------------------
# CONFIGURACIÓN
# ---------------------------

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ecommerce_db"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


# ---------------------------
# FUNCIÓN DE LIMPIEZA
# ---------------------------

def limpiar_dataframe(df):
    # Corrige el error de escritura del dataset
    if "coustomer_key" in df.columns:
        df = df.rename(columns={"coustomer_key": "customer_key"})

    # Convierte NaN a None para MongoDB
    df = df.astype(object).where(pd.notnull(df), None)

    return df


# ---------------------------
# FUNCIÓN PARA CARGAR CSV
# ---------------------------

def cargar_csv(
    archivo,
    coleccion,
    encoding="utf-8",
    chunksize=None
):
    ruta = DATA_DIR / archivo

    print(f"\nCargando {archivo} -> {coleccion}")

    collection = db[coleccion]

    # Permite volver a ejecutar el script sin duplicar datos
    collection.delete_many({})

    total_insertados = 0

    if chunksize:

        for chunk in pd.read_csv(
            ruta,
            encoding=encoding,
            chunksize=chunksize
        ):
            chunk = limpiar_dataframe(chunk)

            registros = chunk.to_dict("records")

            if registros:
                collection.insert_many(registros)
                total_insertados += len(registros)

                print(
                    f"  Insertados: {total_insertados:,}",
                    end="\r"
                )

    else:

        df = pd.read_csv(
            ruta,
            encoding=encoding
        )

        df = limpiar_dataframe(df)

        registros = df.to_dict("records")

        if registros:
            collection.insert_many(registros)
            total_insertados = len(registros)

    print(
        f"\nOK - {coleccion}: "
        f"{total_insertados:,} documentos"
    )


# ---------------------------
# CARGA DE DIMENSIONES
# ---------------------------

cargar_csv(
    "customer_dim.csv",
    "customers",
    encoding="latin1"
)

cargar_csv(
    "item_dim.csv",
    "items",
    encoding="latin1"
)

cargar_csv(
    "store_dim.csv",
    "stores"
)

cargar_csv(
    "time_dim.csv",
    "times"
)

cargar_csv(
    "Trans_dim.csv",
    "payments"
)


# ---------------------------
# CARGA DE TABLA DE HECHOS
# ---------------------------

cargar_csv(
    "fact_table.csv",
    "sales",
    chunksize=50000
)


# ---------------------------
# CREACIÓN DE ÍNDICES
# ---------------------------

db.customers.create_index(
    [("customer_key", ASCENDING)],
    unique=True
)

db.items.create_index(
    [("item_key", ASCENDING)],
    unique=True
)

db.stores.create_index(
    [("store_key", ASCENDING)],
    unique=True
)

db.times.create_index(
    [("time_key", ASCENDING)],
    unique=True
)

db.payments.create_index(
    [("payment_key", ASCENDING)],
    unique=True
)

db.sales.create_index("customer_key")
db.sales.create_index("item_key")
db.sales.create_index("store_key")
db.sales.create_index("time_key")
db.sales.create_index("payment_key")


print("\n--------------------------------")
print("CARGA FINALIZADA CORRECTAMENTE")
print("--------------------------------")

print("\nConteo final:")

for nombre in [
    "customers",
    "items",
    "stores",
    "times",
    "payments",
    "sales"
]:
    print(
        nombre,
        db[nombre].count_documents({})
    )

client.close()