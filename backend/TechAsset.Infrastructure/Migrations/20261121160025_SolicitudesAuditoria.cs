using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace TechAsset.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class SolicitudesAuditoria : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Movimientos",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    Fecha = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    Entidad = table.Column<string>(type: "character varying(30)", maxLength: 30, nullable: false),
                    EntidadId = table.Column<Guid>(type: "uuid", nullable: false),
                    Accion = table.Column<string>(type: "character varying(30)", maxLength: 30, nullable: false),
                    Detalle = table.Column<string>(type: "character varying(300)", maxLength: 300, nullable: false),
                    UsuarioId = table.Column<Guid>(type: "uuid", nullable: true),
                    UsuarioNombre = table.Column<string>(type: "character varying(150)", maxLength: 150, nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Movimientos", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Solicitudes",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uuid", nullable: false),
                    FechaPrestamo = table.Column<DateOnly>(type: "date", nullable: false),
                    FechaDevolucion = table.Column<DateOnly>(type: "date", nullable: false),
                    Motivo = table.Column<string>(type: "character varying(300)", maxLength: 300, nullable: false),
                    Estado = table.Column<string>(type: "character varying(30)", maxLength: 30, nullable: false),
                    ObservacionRevision = table.Column<string>(type: "character varying(300)", maxLength: 300, nullable: true),
                    UsuarioId = table.Column<Guid>(type: "uuid", nullable: false),
                    EquipoId = table.Column<Guid>(type: "uuid", nullable: false),
                    PrestamoId = table.Column<Guid>(type: "uuid", nullable: true),
                    RevisadoPorId = table.Column<Guid>(type: "uuid", nullable: true),
                    FechaRegistro = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    FechaRevision = table.Column<DateTime>(type: "timestamp with time zone", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Solicitudes", x => x.Id);
                    table.CheckConstraint("CK_Solicitudes_Aprobacion", "(\"Estado\" = 'Aprobada' AND \"PrestamoId\" IS NOT NULL) OR (\"Estado\" <> 'Aprobada' AND \"PrestamoId\" IS NULL)");
                    table.CheckConstraint("CK_Solicitudes_Estado", "\"Estado\" IN ('Pendiente','Aprobada','Rechazada')");
                    table.ForeignKey(
                        name: "FK_Solicitudes_Equipos_EquipoId",
                        column: x => x.EquipoId,
                        principalTable: "Equipos",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_Solicitudes_Prestamos_PrestamoId",
                        column: x => x.PrestamoId,
                        principalTable: "Prestamos",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_Solicitudes_Usuarios_RevisadoPorId",
                        column: x => x.RevisadoPorId,
                        principalTable: "Usuarios",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_Solicitudes_Usuarios_UsuarioId",
                        column: x => x.UsuarioId,
                        principalTable: "Usuarios",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.AddCheckConstraint(
                name: "CK_Usuarios_CorreoMinusculas",
                table: "Usuarios",
                sql: "\"Correo\" = lower(\"Correo\")");

            migrationBuilder.AddCheckConstraint(
                name: "CK_Usuarios_Rol",
                table: "Usuarios",
                sql: "\"Rol\" IN ('Administrador','Responsable','Colaborador')");

            migrationBuilder.CreateIndex(
                name: "IX_Prestamos_EquipoActivo",
                table: "Prestamos",
                column: "EquipoId",
                unique: true,
                filter: "\"Estado\" = 'Activo'");

            migrationBuilder.AddCheckConstraint(
                name: "CK_Prestamos_Estado",
                table: "Prestamos",
                sql: "\"Estado\" IN ('Activo','Devuelto')");

            migrationBuilder.AddCheckConstraint(
                name: "CK_Prestamos_Fechas",
                table: "Prestamos",
                sql: "\"FechaDevolucion\" > \"FechaPrestamo\"");

            migrationBuilder.AddCheckConstraint(
                name: "CK_Equipos_CodigoMayusculas",
                table: "Equipos",
                sql: "\"CodigoPatrimonial\" = upper(\"CodigoPatrimonial\")");

            migrationBuilder.AddCheckConstraint(
                name: "CK_Equipos_Estado",
                table: "Equipos",
                sql: "\"Estado\" IN ('Disponible','Prestado','Mantenimiento','Baja')");

            migrationBuilder.CreateIndex(
                name: "IX_Movimientos_Entidad_EntidadId",
                table: "Movimientos",
                columns: new[] { "Entidad", "EntidadId" });

            migrationBuilder.CreateIndex(
                name: "IX_Movimientos_Fecha",
                table: "Movimientos",
                column: "Fecha");

            migrationBuilder.CreateIndex(
                name: "IX_Solicitudes_EquipoPendiente",
                table: "Solicitudes",
                column: "EquipoId",
                unique: true,
                filter: "\"Estado\" = 'Pendiente'");

            migrationBuilder.CreateIndex(
                name: "IX_Solicitudes_Estado",
                table: "Solicitudes",
                column: "Estado");

            migrationBuilder.CreateIndex(
                name: "IX_Solicitudes_FechaRegistro",
                table: "Solicitudes",
                column: "FechaRegistro");

            migrationBuilder.CreateIndex(
                name: "IX_Solicitudes_Prestamo",
                table: "Solicitudes",
                column: "PrestamoId",
                unique: true,
                filter: "\"PrestamoId\" IS NOT NULL");

            migrationBuilder.CreateIndex(
                name: "IX_Solicitudes_RevisadoPorId",
                table: "Solicitudes",
                column: "RevisadoPorId");

            migrationBuilder.CreateIndex(
                name: "IX_Solicitudes_UsuarioId",
                table: "Solicitudes",
                column: "UsuarioId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Movimientos");

            migrationBuilder.DropTable(
                name: "Solicitudes");

            migrationBuilder.DropCheckConstraint(
                name: "CK_Usuarios_CorreoMinusculas",
                table: "Usuarios");

            migrationBuilder.DropCheckConstraint(
                name: "CK_Usuarios_Rol",
                table: "Usuarios");

            migrationBuilder.DropIndex(
                name: "IX_Prestamos_EquipoActivo",
                table: "Prestamos");

            migrationBuilder.DropCheckConstraint(
                name: "CK_Prestamos_Estado",
                table: "Prestamos");

            migrationBuilder.DropCheckConstraint(
                name: "CK_Prestamos_Fechas",
                table: "Prestamos");

            migrationBuilder.DropCheckConstraint(
                name: "CK_Equipos_CodigoMayusculas",
                table: "Equipos");

            migrationBuilder.DropCheckConstraint(
                name: "CK_Equipos_Estado",
                table: "Equipos");
        }
    }
}
