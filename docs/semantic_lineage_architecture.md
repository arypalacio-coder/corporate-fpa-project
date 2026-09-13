*# ARQUITECTURA DE LINAJE SEMÁNTICO Y MODELO DE DATOS*



*\*\*Proyecto:\*\* Corporate FP\&A Data \& Reporting Architecture*

*\*\*Propósito:\*\* Trazabilidad extremo a extremo desde transacciones SQL hasta el modelo tabular Power BI*



*---*



*## 1. Diagrama de Flujo del Pipeline Analítico*



*```text*

*\[Capa Transaccional / ERP]*

&#x20;      *│*

&#x20;      *▼*

*\[01\_staging] ───────► Ingesta y tipado estricto (SEC / Ledger Entries)*

&#x20;      *│*

&#x20;      *▼*

*\[02\_intermediate] ──► Deduplicación, reconciliación mensual y balance check*

&#x20;      *│*

&#x20;      *▼*

*\[03\_marts] ─────────► Capa de consumo dimensional (Esquema en Estrella)*

&#x20;      *│*

&#x20;      *├─► fct\_general\_ledger\_monthly*

&#x20;      *├─► fct\_budget\_allocations\_monthly*

&#x20;      *├─► fct\_balance\_sheet\_monthly*

&#x20;      *├─► dim\_fiscal\_calendar*

&#x20;      *├─► dim\_chart\_of\_accounts*

&#x20;      *└─► dim\_balance\_accounts*

&#x20;      *│*

&#x20;      *▼*

*\[Power BI / PBIP] ──► Motor VertiPaq / TMDL*

&#x20;      *│*

&#x20;      *└─► Medidas DAX de Control (EBITDA, NWC, DSO, Variance Bridge)
2. Definición de Capas y TransformacionesCapa 1: Staging (Extracción y Normalización Primaria)Ingesta de asientos contables crudos y tablas maestras.Conversión de tipos de datos, validación de fechas contables y claves foráneas.Capa 2: Intermediate (Lógica de Negocio y Reconciliación)Partida Doble: Verificación de balance cerrado por asiento y por período contable.Granularidad: Nivelación temporal mensual para acoplar la ejecución contable diaria con el presupuesto planificado.Capa 3: Marts (Modelo Dimensional)Estructuración en esquema en estrella puro.Dimensiones conformadas con relaciones 1:\* unidireccionales para garantizar integridad referencial y rendimiento en memoria.3. Matriz de Entidades y Llaves de EnlaceTabla Origen (Dimensión)Tabla Destino (Hechos)Clave de EnlaceCardinalidaddim\_fiscal\_calendarfct\_general\_ledger\_monthlyDate → Date1:\*dim\_fiscal\_calendarfct\_budget\_allocations\_monthlyFirstDayOfMonth → Date1:\*dim\_chart\_of\_accountsfct\_general\_ledger\_monthlyaccount\_id → account\_id1:\*dim\_chart\_of\_accountsfct\_budget\_allocations\_monthlyaccount\_id → account\_id1:\*dim\_balance\_accountsfct\_balance\_sheet\_monthlyaccount\_id → account\_id1:\*4. Consumo Semántico en Power BIAlmacenamiento: Formato modular PBIP + TMDL apto para integración y control de versiones vía Git.Filtrado: Direccionalidad estricta desde las dimensiones maestras hacia las tablas de hechos, evitando relaciones bidireccionales ambiguas.*

