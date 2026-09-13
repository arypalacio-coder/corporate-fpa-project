*# DICCIONARIO DE DATOS FINANCIEROS (DATA DICTIONARY)*



*\*\*Proyecto:\*\* Corporate FP\&A Data \& Reporting Architecture*  

*\*\*Modelo:\*\* Esquema en Estrella (Star Schema) para Consolidación y Reporting*  



*---*



*## 1. Tablas de Hechos (Fact Tables)*



*### `fct\_general\_ledger\_monthly`*

*Almacena las transacciones consolidadas del libro mayor agrupadas mensualmente para la medición de ingresos y gastos operativos.*



*| Columna | Tipo de Dato | Restricción | Descripción / Regla Contable |*

*| :--- | :--- | :--- | :--- |*

*| `Date` | DATE | FK | Clave de enlace con `dim\_fiscal\_calendar\[Date]` (primer día del mes). |*

*| `account\_id` | VARCHAR | FK | Clave de cuenta contable asociada a `dim\_chart\_of\_accounts\[account\_id]`. |*

*| `debit\_amount` | DECIMAL(18,4) | >= 0 | Monto total acumulado en el debe (debit). |*

*| `credit\_amount` | DECIMAL(18,4) | >= 0 | Monto total acumulado en el haber (credit). |*

*| `amount` | DECIMAL(18,4) | NOT NULL | Saldo neto contable (`debit\_amount - credit\_amount`). |*



*---*



*### `fct\_budget\_allocations\_monthly`*

*Registra la asignación presupuestaria operativa y de ingresos aprobada por la dirección financiera.*



*| Columna | Tipo de Dato | Restricción | Descripción / Regla de Negocio |*

*| :--- | :--- | :--- | :--- |*

*| `Date` | DATE | FK | Primer día del mes presupuestado (enlace con `dim\_fiscal\_calendar`). |*

*| `account\_id` | VARCHAR | FK | Código de cuenta presupuestaria en `dim\_chart\_of\_accounts`. |*

*| `budget\_amount` | DECIMAL(18,4) | NOT NULL | Cifra objetivo planificada para el ejercicio fiscal. |*



*---*



*### `fct\_balance\_sheet\_monthly`*

*Contiene los saldos de cierre de balance general necesarios para el cálculo de liquidez, NWC y ratios operativos.*



*| Columna | Tipo de Dato | Restricción | Descripción / Regla de Negocio |*

*| :--- | :--- | :--- | :--- |*

*| `Date` | DATE | FK | Fecha de corte del balance (enlace con `dim\_fiscal\_calendar`). |*

*| `account\_id` | VARCHAR | FK | Código de cuenta de balance en `dim\_balance\_accounts`. |*

*| `ending\_balance` | DECIMAL(18,4) | NOT NULL | Saldo patrimonial al cierre del mes de reporte. |*



*---*



*## 2. Tablas de Dimensión (Dimension Tables)*



*### `dim\_chart\_of\_accounts`*

*Catálogo maestro de cuentas del estado de resultados (P\&L) con normalización de polaridad contable.*



*| Columna | Tipo de Dato | Restricción | Descripción / Regla de Negocio |*

*| :--- | :--- | :--- | :--- |*

*| `account\_id` | VARCHAR | PK | Identificador único de cuenta contable. |*

*| `account\_name` | VARCHAR | NOT NULL | Descripción textual formal de la partida. |*

*| `category` | VARCHAR | NOT NULL | Clasificación funcional (Revenue, COGS, OPEX, etc.). |*

*| `display\_polarity\_factor` | INTEGER | IN (-1, 1) | Factor multiplicador para garantizar consistencia algebraica en visualización. |*



*---*



*### `dim\_fiscal\_calendar`*

*Dimensión temporal conformada para inteligencia de tiempo (YTD, Prior Year, variaciones).*



*| Columna | Tipo de Dato | Restricción | Descripción |*

*| :--- | :--- | :--- | :--- |*

*| `Date` | DATE | PK | Fecha calendario continua sin discontinuidades. |*

*| `Year` | INTEGER | NOT NULL | Año fiscal correspondiente. |*

*| `Month` | INTEGER | IN (1-12) | Número del mes calendario. |*

*| `MonthName` | VARCHAR | NOT NULL | Nombre del mes (e.g., Enero, Febrero). |*

*| `Quarter` | VARCHAR | NOT NULL | Trimestre fiscal (Q1, Q2, Q3, Q4). |*

