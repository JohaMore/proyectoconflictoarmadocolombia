# Análisis de Datos para Evidenciar el Conflicto Armado en Colombia

## Introducción

El conflicto armado en Colombia es uno de los eventos sociopolíticos más complejos y prolongados en la historia reciente de América Latina. Comprender su dinámica, impacto y consecuencias requiere un enfoque analítico basado en datos. La analítica de datos permite procesar grandes volúmenes de información, identificar patrones, y generar visualizaciones que facilitan la interpretación y toma de decisiones fundamentadas.

Este proyecto utiliza herramientas avanzadas de análisis de datos y visualización para explorar y exponer información relevante sobre el conflicto armado en Colombia. Al combinar datos geográficos, temporales y categóricos, buscamos proporcionar una perspectiva más clara y accesible de la situación.

## Descripción

El propósito principal de este proyecto es emplear técnicas de analítica de datos para:

1. **Visualizar patrones espaciales y temporales:** Utilizando datos geográficos y temporales para mapear la distribución del conflicto.
2. **Identificar tendencias clave:** Analizar la evolución del conflicto a lo largo del tiempo para comprender cómo han cambiado las dinámicas.
3. **Explorar relaciones complejas:** Identificar factores asociados con el conflicto, como su impacto en la población civil, desplazamientos y violaciones a los derechos humanos.

Para lograr estos objetivos, se integran diversas bibliotecas de Python especializadas en análisis de datos, visualización y manejo de datos geoespaciales. Algunas de las herramientas clave incluyen:

- **Streamlit:** Para construir una interfaz interactiva y accesible para los usuarios.
- **Pandas y Plotly:** Para el manejo y visualización de datos tabulares.
- **Folium y Geopandas:** Para representar información geográfica en mapas interactivos.
- **WordCloud y Matplotlib:** Para resaltar patrones textuales y generar visualizaciones complementarias.

Este enfoque basado en datos no solo busca aportar valor académico, sino también generar conciencia y facilitar la comprensión de uno de los mayores desafíos históricos de Colombia.

## Instalación de Librerías para el Proyecto

Este documento describe cómo instalar las librerías necesarias para ejecutar un proyecto que utiliza las siguientes bibliotecas de Python:

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import geopandas as gpd
from streamlit_folium import st_folium
import unidecode
from wordcloud import WordCloud
import matplotlib.pyplot as plt
```

### Requisitos Previos

Asegúrate de tener instalado Python 3.8 o superior. Puedes verificar tu versión de Python ejecutando:

```bash
python --version
```

Se recomienda el uso de un entorno virtual para instalar las dependencias y evitar conflictos con otras bibliotecas instaladas en tu sistema.

### Pasos de Instalación

1. **Crear un Entorno Virtual (Opcional)**

   En la terminal, crea un nuevo entorno virtual:

   ```bash
   python -m venv nombre_entorno
   ```

   Activa el entorno virtual:

   - En Windows:
     ```bash
     nombre_entorno\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source nombre_entorno/bin/activate
     ```

2. **Actualizar `pip`**

   Asegúrate de tener la versión más reciente de `pip`:

   ```bash
   pip install --upgrade pip
   ```

3. **Instalar las Librerías**

   Ejecuta el siguiente comando para instalar todas las bibliotecas necesarias:

   ```bash
   pip install streamlit pandas plotly folium geopandas streamlit-folium unidecode wordcloud matplotlib
   ```

   Si encuentras errores relacionados con `geopandas`, puedes instalar dependencias adicionales necesarias para su correcto funcionamiento. En sistemas basados en Debian/Ubuntu, ejecuta:

   ```bash
   sudo apt-get install libspatialindex-dev
   ```

4. **Verificar la Instalación**

   Puedes verificar que las bibliotecas se hayan instalado correctamente ejecutando el siguiente script:

   ```python
   import streamlit as st
   import pandas as pd
   import plotly.express as px
   import folium
   import geopandas as gpd
   from streamlit_folium import st_folium
   import unidecode
   from wordcloud import WordCloud
   import matplotlib.pyplot as plt

   print("Todas las librerías se instalaron correctamente.")
   ```

5. **Ejecutar el Proyecto**

   Una vez que las librerías estén instaladas, ejecuta tu aplicación Streamlit con el siguiente comando:

   ```bash
   streamlit run nombre_archivo.py
   ```

   Asegúrate de reemplazar `nombre_archivo.py` con el nombre del archivo Python de tu proyecto.

### Notas Adicionales

- **Problemas de Instalación en `geopandas`**: Si encuentras problemas durante la instalación de `geopandas`, consulta la documentación oficial: [Geopandas Installation Guide](https://geopandas.org/en/stable/getting_started/install.html).

- **Entornos Virtuales**: Si decides no usar un entorno virtual, las bibliotecas se instalarán globalmente, lo que puede ocasionar conflictos con otras bibliotecas en tu sistema.

- **Compatibilidad del Sistema Operativo**: Algunas bibliotecas, como `folium` y `geopandas`, pueden requerir dependencias específicas del sistema operativo.

---

Con estos pasos, tu entorno debería estar configurado y listo para ejecutar el proyecto. Si tienes preguntas o problemas durante la instalación, no dudes en buscar ayuda en la documentación oficial de las librerías o en foros de soporte.

