# TechAsset

Sistema de gestión de inventario y préstamo de equipos tecnológicos para **Innovatech Solutions S.A.C.**  
Caso práctico integrador · Construcción de Software · UPLA 2026-II

**Repositorio:** https://github.com/CRAXCAT/TechAsset

## Descripción

TechAsset centraliza el registro de usuarios, equipos y préstamos, aplica las 10 reglas de negocio del caso y
ofrece un portal público de inicio, consultas, filtros, reportes, exportación CSV, solicitudes con aprobación,
auditoría de movimientos y un dashboard con seis indicadores. Incluye autenticación real con BCrypt, JWT, roles
y contraseña temporal.

- **Frontend:** React 19 · Vite 8 · React Router · CSS propio (tema claro/oscuro y responsive)
- **Backend:** ASP.NET Core 10 · Entity Framework Core 10 · BCrypt.Net-Next · JWT Bearer
- **Base de datos:** PostgreSQL 18 (`TechAssetDB`)
- **Pruebas:** 50 escenarios de API · 12 comprobaciones de integridad · 40 capturas · 6 diagramas
- **Informe:** 60 páginas, 50 tablas y 45 figuras en `docs/`

## Estructura

```
TechAsset/
├─ backend/
│  ├─ TechAsset.Domain/          Entidades y catálogo
│  ├─ TechAsset.Application/     DTO, filtros, interfaces, servicios y reglas
│  ├─ TechAsset.Infrastructure/  DbContext, repositorios, UnitOfWork, BCrypt, JWT y migraciones
│  ├─ TechAsset.API/             Controladores, middleware, Swagger y Program.cs
│  └─ TechAsset.slnx
├─ frontend/
│  ├─ src/components/            layout, ui y RutaPrivada
│  ├─ src/pages/                 Inicio (portal), Login, Dashboard, Usuarios, Equipos, Solicitudes, NuevaSolicitud, Préstamos, Reportes, Movimientos
│  ├─ src/hooks/                 10 hooks de datos y contextos
│  ├─ src/services/              api, auth, usuarios, equipos, préstamos, solicitudes, movimientos y reportes
│  └─ src/utils/                 catálogos, formato y validaciones
└─ docs/
   ├─ capturas/                  40 evidencias de interfaz
   ├─ figuras/                   diagramas y logotipos
   ├─ scripts/                   datos, pruebas, capturas e informe
   ├─ pruebas-api.json           resultados de los 50 escenarios
   ├─ pruebas-integridad.json    resultados de las 12 comprobaciones en PostgreSQL
   ├─ Informe_TechAsset_KevinCcente.pdf
   └─ Informe_TechAsset_KevinCcente.docx
```

## Requisitos

- .NET SDK 10
- Node.js 20 o superior
- PostgreSQL 18 en `localhost:5432`
- Python 3.12 (opcional, para reproducir pruebas, capturas e informe)

## Configuración

La cadena de conexión y la clave JWT se encuentran en `backend/TechAsset.API/appsettings.json`:

```json
"ConnectionStrings": {
  "DefaultConnection": "Host=localhost;Port=5432;Database=TechAssetDB;Username=postgres;Password=postgres"
}
```

## Ejecución

```powershell
# Backend
cd backend
dotnet restore
dotnet ef database update --project TechAsset.Infrastructure --startup-project TechAsset.API
dotnet run --project TechAsset.API --launch-profile http
# API:     http://localhost:5143
# Swagger: http://localhost:5143/swagger

# Frontend (otra terminal)
cd frontend
npm install
npm run dev
# Portal:  http://localhost:5173/
# Panel:   http://localhost:5173/panel
# Login:   http://localhost:5173/login
```

La API aplica la migración `InitialCreate` al iniciar y crea el administrador inicial si la base está vacía.
El portal público está en `/`; las rutas `/panel`, `/usuarios`, `/equipos`, `/prestamos` y `/reportes` requieren sesión.

## Cuentas de demostración

| Cuenta | Correo | Contraseña | Rol |
|---|---|---|---|
| Administrador inicial | `admin@innovatech.pe` | `Admin.2026*` | Administrador |
| Kevin Ccente | `kevin.ccente@innovatech.pe` | `Tech.2026*` | Administrador |
| Lucía Paredes | `lucia.paredes@innovatech.pe` | `Tech.2026*` | Responsable |
| Pedro Ccahuana | `pedro.ccahuana@innovatech.pe` | `Tech.2026*` | Responsable |
| Rosa Quispe | `rosa.quispe@innovatech.pe` | `Tech.2026*` | Colaborador |
| Diego Flores | `diego.flores@innovatech.pe` | `Temporal.2026*` | Colaborador (cambio obligatorio) |

## Datos y pruebas

```powershell
cd docs

python scripts/reiniciar_datos.py    # limpia y recarga 18 equipos, 13 usuarios, 17 préstamos y 4 solicitudes
python scripts/pruebas_api.py         # 50 escenarios; escribe pruebas-api.json
python scripts/pruebas_integridad.py  # 12 comprobaciones de integridad en PostgreSQL
python scripts/capturas.py            # 23 capturas de interfaz
python scripts/capturas_prestamo.py   # recaptura el alta de préstamo y reportes
python scripts/capturas_altas.py      # 2 capturas de alta de usuario y equipo
python scripts/capturas_portal.py     # portal público, login y versión móvil
python scripts/capturas_solicitudes.py # 12 capturas de solicitudes, aprobación y auditoría
python scripts/figuras.py             # 6 diagramas
python scripts/informe_techasset.py   # genera el DOCX
python scripts/exportar_pdf_techasset.py  # exporta el PDF con índice, enlaces y marcadores
```

> `capturas.py` crea un préstamo temporal y `capturas_solicitudes.py` una solicitud y una aprobación. Ejecute
> `reiniciar_datos.py` después de las capturas para volver al conjunto base de 17 préstamos y 4 solicitudes.

## Reglas de negocio

| Código | Regla |
|---|---|
| RN-01 | Un equipo solo puede estar asociado a un préstamo activo. |
| RN-02 | No se presta un equipo en Mantenimiento. |
| RN-03 | No se presta un equipo en Baja. |
| RN-04 | La fecha de devolución debe ser posterior a la del préstamo. |
| RN-05 | Todo préstamo registra un responsable. |
| RN-06 | No se elimina un equipo con historial de préstamos. |
| RN-07 | El código patrimonial es único. |
| RN-08 | El correo del usuario es único. |
| RN-09 | Solo el Administrador deshabilita usuarios. |
| RN-10 | Toda devolución registra observaciones. |
| RN-11 | Una sola solicitud pendiente por equipo. |
| RN-12 | Una solicitud aprobada exige un préstamo; pendiente o rechazada no lo admite. |
| RN-13 | El Colaborador solo consulta su propio historial. |
| RN-14 | Solo Administración y Tecnología consultan la auditoría. |

## Informe

- `docs/Informe_TechAsset_KevinCcente.pdf` — versión final con índice clicable, enlaces y marcadores.
- `docs/Informe_TechAsset_KevinCcente.docx` — versión editable con hipervínculos internos.
