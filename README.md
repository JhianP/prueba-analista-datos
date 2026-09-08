# Prueba Técnica - Analista Junior de Datos y Automatización

Solución desarrollada para la prueba técnica del puesto de **Analista Junior de Datos y Automatización**.

El proyecto implementa un flujo analítico completo a partir de archivos CSV, utilizando **MongoDB** como base de datos, **Python** para la carga y validación de información, **MongoDB Aggregation Pipeline** para los cálculos y **Jupyter Notebook** para el análisis y las visualizaciones.

## Objetivo

Construir una solución reproducible que permita:

- Cargar información proveniente de archivos CSV.
- Modelar los datos en MongoDB.
- Validar calidad e integridad de los datos.
- Realizar análisis mediante Aggregation Pipeline.
- Obtener indicadores de negocio.
- Generar visualizaciones.
- Consumir una API pública.
- Proponer endpoints para consumo de indicadores.
- Documentar hallazgos y decisiones técnicas.

## Flujo de la solución

```text
CSV
 ↓
Python
 ↓
Validación de datos
 ↓
MongoDB
 ↓
Aggregation Pipeline
 ↓
Pandas
 ↓
Matplotlib
 ↓
Análisis y hallazgos
```

## Tecnologías utilizadas

- Python
- MongoDB
- MongoDB Compass
- PyMongo
- Pandas
- Jupyter Notebook
- Matplotlib
- Requests
- Git
- GitHub
- Mermaid

## Estructura del proyecto

```text
prueba-analista-datos/
│
├── data/
│   ├── customer_dim.csv
│   ├── fact_table.csv
│   ├── item_dim.csv
│   ├── store_dim.csv
│   ├── time_dim.csv
│   └── Trans_dim.csv
│
├── src/
│   └── load_mongodb.py
│
├── notebooks/
│   └── analisis_ecommerce.ipynb
│
├── docs/
│   └── modelo_mongodb.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Dataset

El análisis utiliza seis archivos CSV correspondientes a un dataset de comercio electrónico:

- `fact_table.csv`: transacciones de ventas.
- `customer_dim.csv`: información de clientes.
- `item_dim.csv`: información de productos.
- `store_dim.csv`: información de tiendas.
- `time_dim.csv`: información temporal.
- `Trans_dim.csv`: información sobre métodos de pago.

Cantidad aproximada de registros cargados:

| Colección | Registros |
|---|---:|
| sales | 1,000,000 |
| customers | 9,191 |
| items | 264 |
| stores | 726 |
| times | 99,999 |
| payments | 39 |

## Modelo de datos

Se utilizó un modelo analítico similar a un **esquema estrella**.

La colección central es:

```text
sales
```

La colección `sales` mantiene referencias hacia:

```text
customers
items
stores
times
payments
```

Las relaciones principales son:

```text
customers.customer_key ← sales.customer_key

items.item_key ← sales.item_key

stores.store_key ← sales.store_key

times.time_key ← sales.time_key

payments.payment_key ← sales.payment_key
```

Las relaciones se utilizan mediante `$lookup` dentro de MongoDB Aggregation Pipeline.

El diagrama completo del modelo se encuentra en:

```text
docs/modelo_mongodb.md
```

## Colecciones MongoDB

| Colección | Descripción |
|---|---|
| `sales` | Transacciones de ventas |
| `customers` | Información de clientes |
| `items` | Información de productos |
| `stores` | Información de tiendas |
| `times` | Dimensión temporal |
| `payments` | Información de métodos de pago |

## Decisión de modelado

Se decidió mantener las principales entidades en colecciones independientes y utilizar `sales` como colección central.

Esto permite:

- Evitar duplicar información descriptiva en cada venta.
- Mantener las dimensiones de manera independiente.
- Facilitar el análisis de grandes cantidades de transacciones.
- Realizar relaciones mediante `$lookup`.
- Optimizar consultas utilizando índices.

Algunos atributos pequeños y poco cambiantes podrían ser embebidos en un escenario futuro si esto mejorara el rendimiento de las consultas.

## Carga de datos

La carga de los archivos CSV se realiza mediante:

```text
src/load_mongodb.py
```

El script:

- Lee los archivos CSV.
- Corrige algunos nombres de campos.
- Maneja valores nulos.
- Inserta los registros en MongoDB.
- Procesa `fact_table.csv` por bloques.
- Crea índices.
- Valida la cantidad de documentos cargados.

La base de datos utilizada es:

```text
ecommerce_db
```

## Calidad de datos

Durante la exploración se validaron:

- Valores nulos.
- Claves duplicadas.
- Integridad entre las colecciones.
- Correspondencia entre las claves de `sales` y las dimensiones.
- Cantidad de documentos después de la carga.

Se encontraron algunos valores nulos en atributos descriptivos.

Estos valores fueron conservados debido a que no afectan las claves utilizadas para relacionar las colecciones.

También se verificó que no existan claves huérfanas entre `sales` y:

- `customers`
- `items`
- `stores`
- `times`
- `payments`

## Indicadores analizados

Se calcularon los siguientes indicadores:

- Venta total.
- Número de transacciones.
- Clientes únicos.
- Ticket promedio.
- Evolución mensual de ventas.
- Comparación de tiendas.
- Comparación de productos.
- Análisis por método de pago.

Los principales cálculos se realizaron directamente en **MongoDB Aggregation Pipeline**.

Pandas fue utilizado principalmente para organizar los resultados agregados y generar visualizaciones.

## Indicadores generales

Los resultados obtenidos fueron:

| Indicador | Resultado |
|---|---:|
| Venta total | $105,401,435.75 |
| Número de transacciones | 1,000,000 |
| Clientes únicos | 9,191 |
| Ticket promedio | $105.40 |

## Evolución de ventas

Las ventas fueron agrupadas por año y mes utilizando la relación entre:

```text
sales
   ↓ time_key
times
```

La relación se realizó mediante `$lookup`.

Posteriormente, los resultados agregados fueron enviados a Pandas para generar una visualización con Matplotlib.

## Comparación de tiendas

Las ventas fueron agrupadas por `store_key`.

Posteriormente se realizó un `$lookup` con la colección `stores` para obtener información descriptiva de cada tienda.

Se analizaron:

- Venta total.
- Número de transacciones.
- Ticket promedio.

Finalmente se identificaron las tiendas con mayores ventas.

## Comparación de productos

Las ventas fueron agrupadas por `item_key`.

Posteriormente se relacionó el resultado con la colección `items`.

Se analizaron:

- Venta total.
- Unidades vendidas.
- Número de transacciones.

Dentro del ranking analizado, **Red Bull 12oz** presentó la mayor venta total.

## Métodos de pago

Se analizaron las ventas según el tipo de pago.

Los métodos presentes en el dataset incluyen:

```text
card
mobile
cash
```

Las operaciones mediante tarjeta representan una proporción considerablemente mayor de las ventas frente a los demás métodos.

## Hallazgos principales

### 1. Alta concentración de ventas mediante tarjeta

El método `card` concentra una proporción considerable de las ventas.

Esto resulta relevante porque una alta dependencia de este canal hace importante mantener la estabilidad y disponibilidad de los servicios relacionados con pagos mediante tarjeta.

### 2. Red Bull 12oz lidera el ranking de productos

Dentro del análisis realizado, **Red Bull 12oz** presenta la mayor venta total.

Sin embargo, antes de recomendar aumentar inventario o realizar promociones sería necesario analizar información adicional como:

- Margen de ganancia.
- Costo.
- Inventario.
- Rotación.
- Disponibilidad.
- Comportamiento por tienda.

### 3. Existen variaciones mensuales en las ventas

La evolución mensual muestra diferencias entre periodos.

Los valores extremos al inicio y final del periodo deben interpretarse con precaución, debido a que podrían corresponder a meses incompletos y no necesariamente a una disminución real del negocio.

## Consumo de API pública

Como parte de la solución se realizó una petición HTTP GET a:

```text
DummyJSON Products API
```

Se solicitaron campos como:

- ID.
- Producto.
- Categoría.
- Precio.
- Rating.

La respuesta obtenida en formato JSON fue convertida posteriormente a un DataFrame utilizando Pandas.

Esta información se utilizó únicamente para demostrar el consumo de una fuente externa y no fue integrada con el dataset principal.

## Endpoints propuestos

Se proponen dos endpoints para permitir que aplicaciones externas consuman indicadores sin acceder directamente a todas las transacciones.

### Endpoint 1 - Resumen general de ventas

```text
GET /api/v1/sales/summary
```

Parámetros:

```text
start_date
end_date
```

Ejemplo:

```text
GET /api/v1/sales/summary?start_date=2020-01-01&end_date=2020-12-31
```

El endpoint devolvería:

- Venta total.
- Número de transacciones.
- Clientes únicos.
- Ticket promedio.

Ejemplo de respuesta:

```json
{
  "start_date": "2020-01-01",
  "end_date": "2020-12-31",
  "venta_total": 15350000.50,
  "transacciones": 145620,
  "clientes_unicos": 8120,
  "ticket_promedio": 105.41
}
```

### Endpoint 2 - Productos con mayores ventas

```text
GET /api/v1/products/top
```

Parámetros:

```text
limit
start_date
end_date
```

Ejemplo:

```text
GET /api/v1/products/top?limit=10&start_date=2020-01-01&end_date=2020-12-31
```

El endpoint devolvería:

- Código del producto.
- Nombre.
- Venta total.
- Unidades vendidas.
- Número de transacciones.

Ejemplo de respuesta:

```json
{
  "productos": [
    {
      "item_key": "I001",
      "producto": "Red Bull 12oz",
      "venta_total": 1300000.50,
      "unidades_vendidas": 25200,
      "transacciones": 10500
    }
  ]
}
```

## ¿Por qué utilizar endpoints?

Utilizar endpoints en lugar de proporcionar acceso directo a las transacciones permite:

- Controlar los datos disponibles.
- Reducir el volumen de información transferida.
- Centralizar la lógica de cálculo.
- Evitar que diferentes aplicaciones calculen indicadores de manera distinta.
- Implementar autenticación.
- Implementar caché.
- Aplicar controles de acceso.
- Mejorar la seguridad de la base de datos.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
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

Ejecutar las celdas en orden.

## Escalabilidad

Si la base tuviera aproximadamente 20 millones de transacciones se considerarían las siguientes mejoras:

- Crear y revisar índices según los campos más consultados.
- Utilizar proyecciones para obtener únicamente campos necesarios.
- Mantener cálculos pesados dentro de MongoDB.
- Evitar cargar millones de registros completos en Pandas.
- Analizar los Aggregation Pipelines mediante planes de ejecución.
- Precalcular indicadores utilizados frecuentemente.
- Implementar procesos batch.
- Utilizar caché para consultas recurrentes.
- Evaluar sharding si el crecimiento del volumen lo requiere.

## Automatización futura

Si el análisis tuviera que realizarse diariamente, no se mantendría únicamente como un notebook manual.

Se propondría automatizar:

```text
Carga de datos
      ↓
Validación
      ↓
MongoDB
      ↓
Aggregation Pipelines
      ↓
Indicadores
      ↓
API / Dashboard
```

También podrían implementarse:

- Ejecuciones programadas.
- Alertas ante errores de calidad.
- Indicadores precalculados.
- Actualizaciones automáticas de dashboards.
- Registros de ejecución y auditoría.


## Autor

**Jhian Pierre Castro Arce**