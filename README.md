

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/JhianP/prueba-analista-datos.git
```

Ingresar al proyecto:

```bash
cd prueba-analista-datos
```

### 2. Instalar las dependencias

Ejecutar:

```bash
pip install -r requirements.txt
```

Las principales dependencias utilizadas son:

```text
pandas
pymongo
jupyter
matplotlib
requests
```

### 3. Iniciar MongoDB

MongoDB debe estar instalado y ejecutándose localmente.

La conexión utilizada es:

```text
mongodb://localhost:27017/
```

Puede utilizarse MongoDB Compass para verificar las colecciones y documentos cargados.

### 4. Cargar los CSV a MongoDB

Desde la carpeta principal del proyecto ejecutar:

```bash
python src/load_mongodb.py
```

El script creará la base:

```text
ecommerce_db
```

y las siguientes colecciones:

```text
customers
items
stores
times
payments
sales
```

### 5. Ejecutar Jupyter Notebook

Ejecutar:

```bash
jupyter notebook
```

Después abrir:

```text
notebooks/analisis_ecommerce.ipynb
```

## Autor

**Jhian Pierre Castro Arce**