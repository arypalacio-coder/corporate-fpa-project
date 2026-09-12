*# Arquitectura del Modelo Dimensional y Especificación DAX*



*## 1. Topología del Esquema en Estrella (Star Schema)*



*Todas las relaciones deben configurarse con cardinalidad de \*\*Uno a Varios (1:\*)\*\* y dirección de filtro cruzado \*\*Única (Single)\*\* desde las dimensiones hacia las tablas de hechos:*



*| Dimensión Origen (1) | Clave Primaria | Tabla Hechos Destino (\*) | Clave Foránea | Dirección de Filtro |*

*| :--- | :--- | :--- | :--- | :--- |*

*| `dim\_chart\_of\_accounts` | `account\_id` | `fct\_general\_ledger\_daily` | `account\_id` | Single (Dim -> Fact) |*

*| `dim\_chart\_of\_accounts` | `account\_id` | `fct\_budget\_allocations\_monthly` | `account\_id` | Single (Dim -> Fact) |*

*| `dim\_cost\_center` | `cost\_center\_id` | `fct\_general\_ledger\_daily` | `cost\_center\_id` | Single (Dim -> Fact) |*

*| `dim\_cost\_center` | `cost\_center\_id` | `fct\_budget\_allocations\_monthly` | `cost\_center\_id` | Single (Dim -> Fact) |*

*| `dim\_entity` | `entity\_id` | `fct\_general\_ledger\_daily` | `entity\_id` | Single (Dim -> Fact) |*

*| `dim\_fiscal\_calendar` | `date` | `fct\_general\_ledger\_daily` | `transaction\_date` | Single (Dim -> Fact) |*

*| `dim\_fiscal\_calendar` | `first\_day\_of\_month` | `fct\_budget\_allocations\_monthly` | `budget\_month` | Single (Dim -> Fact) |*



*---*



*## 2. Catálogo de Medidas DAX Principales*



*### 2.1 Métricas Base de Ejecución y Presupuesto*



*```dax*

*// Monto Real Base*

*Actual Amount =* 

*SUM(fct\_general\_ledger\_daily\[net\_amount])*



*// Monto Presupuestado Base*

*Budget Amount =* 

*SUM(fct\_budget\_allocations\_monthly\[budgeted\_amount])
// Ajuste de Signos por Naturaleza Contable (Ingreso +, Costo/Gasto -)*

*Actual Polarized =* 

*SUMX(*

&#x20;   *dim\_chart\_of\_accounts,*

&#x20;   *\[Actual Amount] \* dim\_chart\_of\_accounts\[display\_polarity\_factor]*

*)*



*// Presupuesto Polarizado*

*Budget Polarized =* 

*SUMX(*

&#x20;   *dim\_chart\_of\_accounts,*

&#x20;   *\[Budget Amount] \* dim\_chart\_of\_accounts\[display\_polarity\_factor]*

*)
// Desviación Presupuestaria Absoluta*

*Budget Variance Absolute =* 

*\[Actual Amount] - \[Budget Amount]*



*// Desviación Presupuestaria Relativa (%)*

*Budget Variance % =* 

*DIVIDE(*

&#x20;   *\[Budget Variance Absolute],*

&#x20;   *ABS(\[Budget Amount]),*

&#x20;   *BLANK()*

*)
// Acumulado Anual a la Fecha (YTD) - Real*

*Actual YTD =* 

*TOTALYTD(*

&#x20;   *\[Actual Amount],*

&#x20;   *dim\_fiscal\_calendar\[date]*

*)*



*// Acumulado Anual a la Fecha (YTD) - Presupuesto*

*Budget YTD =* 

*TOTALYTD(*

&#x20;   *\[Budget Amount],*

&#x20;   *dim\_fiscal\_calendar\[date]*

*)*



*// Desviación YTD (%)*

*Budget Variance YTD % =* 

*DIVIDE(*

&#x20;   *\[Actual YTD] - \[Budget YTD],*

&#x20;   *ABS(\[Budget YTD]),*

&#x20;   *BLANK()*

*)*

