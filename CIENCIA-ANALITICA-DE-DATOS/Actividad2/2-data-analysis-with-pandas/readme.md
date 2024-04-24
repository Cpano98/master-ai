# README.md

## Resumen de la actividad: Análisis de datos de calidad del aire en Londres (2017) usando Pandas en Python

### Datos
El conjunto de datos `LaqnData.csv` contiene mediciones por hora de cinco contaminantes del aire recopilados en Londres durante 2017.

### Análisis realizado

1. **Carga de datos y exploración inicial**
   - Carga de datos en un DataFrame `air_df`.
   - Inspección de la estructura y contenido del DataFrame.

2. **Limpieza de datos**
   - Cálculo del porcentaje de valores faltantes.
   - Eliminación de columnas que no aportan valor informativo: 'Provisional or Ratified', 'Site', y 'Units'.

3. **Exploración de datos**
   - Conteo de valores por categoría para la columna `Species`.
   - Promedio del valor por contaminante usando `groupby()`.

4. **Transformación de datos**
   - Cambio del formato largo al formato ancho usando `pivot()`, donde `ReadingDateTime` se convierte en índice y cada contaminante en una columna.

5. **Estadísticas descriptivas**
   - Uso de `describe()` para obtener estadísticas descriptivas del DataFrame transformado `pvt_df`.

6. **Identificación de valores extremos**
   - Búsqueda de los valores máximo y mínimo para NO2 y PM10, respectivamente.
   - Cálculo de la mediana para NO y el primer cuartil para PM2.5.

7. **Visualización de datos**
   - Histogramas para cada columna de `pvt_df` para identificar la variabilidad de los contaminantes.

8. **Manipulación adicional de datos**
   - Separación de la columna `ReadingDateTime` en 'Date' y 'Time'.
   - Establecimiento de un nuevo índice compuesto por 'Month', 'Day', 'Time', 'Species'.

9. **Comparación con la estructura pivotada**
   - Verificación de la igualdad entre la estructura actual y la obtenida a través de `unstack()`.

### Conclusión

Se realizó un análisis exhaustivo de los datos de calidad del aire, lo que permitió identificar patrones, valores extremos y características de cada contaminante.