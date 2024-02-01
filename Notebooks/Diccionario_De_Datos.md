# Diccionario de Datos para el Proyecto

## Google Maps

### Metadata de Sitios

La carpeta contiene 11 archivos .json con información del comercio, incluyendo localización, atributos y categorías. Algunos campos relevantes son:

- `name`: Nombre del comercio.
- `address`: Dirección completa.
- `latitude`, `longitude`: Coordenadas geográficas.
- `category`: Categoría del comercio.
- `avg_rating`: Calificación promedio.
- `num_of_reviews`: Número de reseñas.
- `price`: Rango de precios.
- `hours`: Horarios de atención.
- `MISC`: Información adicional (servicios, seguridad, accesibilidad, etc.).
- `state`: Estado y horario de cierre.
- `url`: Enlace a Google Maps.

### Reviews por Estados

Archivos .json que contienen reseñas de usuarios organizadas por estados. Campos principales:

- `user_id`: ID único del usuario.
- `name`: Nombre del usuario.
- `time`: Timestamp de la reseña.
- `rating`: Calificación otorgada.
- `text`: Texto de la reseña.
- `pics`: Enlaces a imágenes.
- `resp`: Respuesta del comercio (si aplica).
- `gmap_id`: ID de Google Maps.

## Dataset de Yelp!

### business.pkl

Información detallada de los negocios. Campos destacados:

- `business_id`: ID único del negocio.
- `name`: Nombre del negocio.
- `address`, `city`, `state`, `postal code`: Dirección y ubicación.
- `latitude`, `longitude`: Coordenadas geográficas.
- `stars`: Calificación en estrellas.
- `review_count`: Número de reseñas.
- `is_open`: Estado de apertura/cierre.
- `attributes`: Atributos del negocio.
- `categories`: Categorías del negocio.
- `hours`: Horarios de atención.

### review.json

Contiene reseñas completas de usuarios. Campos clave:

- `review_id`: ID único de la reseña.
- `user_id`, `business_id`: IDs de usuario y negocio.
- `stars`: Calificación en estrellas.
- `date`: Fecha de la reseña.
- `text`: Texto de la reseña.
- `useful`, `funny`, `cool`: Votos útiles, graciosos y cool.

### user.parquet

Datos del usuario, incluyendo información personal y estadísticas. Campos importantes:

- `user_id`: ID único del usuario.
- `name`: Nombre del usuario.
- `review_count`: Número de reseñas escritas.
- `yelping_since`: Fecha de registro en Yelp.
- `friends`: Lista de amigos.
- `average_stars`: Promedio de calificaciones.
- `elite`: Años como miembro élite.
- ...

### checkin.json

Registros de check-ins en negocios. Campos principales:

- `business_id`: ID único del negocio.
- `date`: Fechas de check-ins.

### tip.json

Consejos escritos por usuarios. Campos esenciales:

- `text`: Texto del consejo.
- `date`: Fecha del consejo.
- `compliment_count`: Número total de cumplidos.
- `business_id`, `user_id`: IDs de negocio y usuario.

Este README proporciona una visión general de los conjuntos de datos y su estructura para facilitar la comprensión y el uso en el proyecto.
