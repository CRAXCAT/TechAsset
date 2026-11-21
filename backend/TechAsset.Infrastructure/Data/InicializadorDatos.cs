using Microsoft.EntityFrameworkCore;
using TechAsset.Application.Interfaces;
using TechAsset.Domain.Entities;
using TechAsset.Infrastructure.Data;

namespace TechAsset.Infrastructure.Data;

/// <summary>
/// Crea el administrador inicial cuando la base de datos está vacía.
/// </summary>
public static class InicializadorDatos
{
    public const string CorreoAdministrador = "admin@innovatech.pe";
    public const string ClaveAdministrador = "Admin.2026*";

    public static async Task CrearAdministradorAsync(AppDbContext context, IPasswordHasher hasher)
    {
        if (await context.Usuarios.AnyAsync())
        {
            return;
        }

        context.Usuarios.Add(new Usuario
        {
            Id = Guid.NewGuid(),
            Nombres = "Administrador",
            Apellidos = "TechAsset",
            Correo = CorreoAdministrador,
            Area = "Sistemas",
            Rol = "Administrador",
            Activo = true,
            PasswordHash = hasher.Hashear(ClaveAdministrador),
            DebeCambiarPassword = false,
            FechaRegistro = DateTime.UtcNow
        });

        await context.SaveChangesAsync();
    }
}
