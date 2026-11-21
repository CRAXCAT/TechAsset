using Microsoft.EntityFrameworkCore;
using TechAsset.Domain.Entities;

namespace TechAsset.Infrastructure.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    public DbSet<Usuario> Usuarios => Set<Usuario>();
    public DbSet<Equipo> Equipos => Set<Equipo>();
    public DbSet<Prestamo> Prestamos => Set<Prestamo>();
    public DbSet<Solicitud> Solicitudes => Set<Solicitud>();
    public DbSet<Movimiento> Movimientos => Set<Movimiento>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        var usuario = modelBuilder.Entity<Usuario>();
        usuario.ToTable("Usuarios", t =>
        {
            t.HasCheckConstraint("CK_Usuarios_Rol", "\"Rol\" IN ('Administrador','Responsable','Colaborador')");
            t.HasCheckConstraint("CK_Usuarios_CorreoMinusculas", "\"Correo\" = lower(\"Correo\")");
        });
        usuario.HasKey(u => u.Id);
        usuario.Property(u => u.Nombres).HasMaxLength(100).IsRequired();
        usuario.Property(u => u.Apellidos).HasMaxLength(100).IsRequired();
        usuario.Property(u => u.Correo).HasMaxLength(150).IsRequired();
        usuario.Property(u => u.Area).HasMaxLength(100).IsRequired();
        usuario.Property(u => u.Rol).HasMaxLength(30).IsRequired();
        usuario.Property(u => u.PasswordHash).HasMaxLength(300).IsRequired();
        usuario.Property(u => u.Activo).HasDefaultValue(true);
        usuario.Property(u => u.DebeCambiarPassword).HasDefaultValue(false);
        usuario.HasIndex(u => u.Correo).IsUnique();
        usuario.HasIndex(u => u.Area);

        var equipo = modelBuilder.Entity<Equipo>();
        equipo.ToTable("Equipos", t =>
        {
            t.HasCheckConstraint("CK_Equipos_Estado", "\"Estado\" IN ('Disponible','Prestado','Mantenimiento','Baja')");
            t.HasCheckConstraint("CK_Equipos_CodigoMayusculas", "\"CodigoPatrimonial\" = upper(\"CodigoPatrimonial\")");
        });
        equipo.HasKey(e => e.Id);
        equipo.Property(e => e.CodigoPatrimonial).HasMaxLength(50).IsRequired();
        equipo.Property(e => e.Nombre).HasMaxLength(100).IsRequired();
        equipo.Property(e => e.Categoria).HasMaxLength(50).IsRequired();
        equipo.Property(e => e.Marca).HasMaxLength(50).IsRequired();
        equipo.Property(e => e.Estado).HasMaxLength(30).IsRequired();
        equipo.HasIndex(e => e.CodigoPatrimonial).IsUnique();
        equipo.HasIndex(e => e.Estado);

        var prestamo = modelBuilder.Entity<Prestamo>();
        prestamo.ToTable("Prestamos", t =>
        {
            t.HasCheckConstraint("CK_Prestamos_Estado", "\"Estado\" IN ('Activo','Devuelto')");
            t.HasCheckConstraint("CK_Prestamos_Fechas", "\"FechaDevolucion\" > \"FechaPrestamo\"");
        });
        prestamo.HasKey(p => p.Id);
        prestamo.Property(p => p.Observacion).HasMaxLength(300).IsRequired();
        prestamo.Property(p => p.ObservacionDevolucion).HasMaxLength(300);
        prestamo.Property(p => p.Estado).HasMaxLength(30).IsRequired();
        prestamo.HasIndex(p => new { p.EquipoId, p.Estado });
        prestamo.HasIndex(p => new { p.UsuarioId, p.FechaPrestamo });
        prestamo
            .HasIndex(p => p.EquipoId)
            .IsUnique()
            .HasFilter("\"Estado\" = 'Activo'")
            .HasDatabaseName("IX_Prestamos_EquipoActivo");

        prestamo
            .HasOne(p => p.Usuario)
            .WithMany(u => u.Prestamos)
            .HasForeignKey(p => p.UsuarioId)
            .OnDelete(DeleteBehavior.Restrict);

        prestamo
            .HasOne(p => p.Equipo)
            .WithMany(e => e.Prestamos)
            .HasForeignKey(p => p.EquipoId)
            .OnDelete(DeleteBehavior.Restrict);

        prestamo
            .HasOne(p => p.Responsable)
            .WithMany(u => u.PrestamosResponsable)
            .HasForeignKey(p => p.ResponsableId)
            .OnDelete(DeleteBehavior.Restrict);

        var solicitud = modelBuilder.Entity<Solicitud>();
        solicitud.ToTable("Solicitudes", t =>
        {
            t.HasCheckConstraint("CK_Solicitudes_Estado", "\"Estado\" IN ('Pendiente','Aprobada','Rechazada')");
            t.HasCheckConstraint(
                "CK_Solicitudes_Aprobacion",
                "(\"Estado\" = 'Aprobada' AND \"PrestamoId\" IS NOT NULL) OR (\"Estado\" <> 'Aprobada' AND \"PrestamoId\" IS NULL)");
        });
        solicitud.HasKey(s => s.Id);
        solicitud.Property(s => s.Motivo).HasMaxLength(300).IsRequired();
        solicitud.Property(s => s.ObservacionRevision).HasMaxLength(300);
        solicitud.Property(s => s.Estado).HasMaxLength(30).IsRequired();
        solicitud.HasIndex(s => s.Estado);
        solicitud.HasIndex(s => s.UsuarioId);
        solicitud.HasIndex(s => s.EquipoId);
        solicitud.HasIndex(s => s.FechaRegistro);
        solicitud
            .HasIndex(s => s.EquipoId)
            .IsUnique()
            .HasFilter("\"Estado\" = 'Pendiente'")
            .HasDatabaseName("IX_Solicitudes_EquipoPendiente");
        solicitud
            .HasIndex(s => s.PrestamoId)
            .IsUnique()
            .HasFilter("\"PrestamoId\" IS NOT NULL")
            .HasDatabaseName("IX_Solicitudes_Prestamo");

        solicitud
            .HasOne(s => s.Usuario)
            .WithMany(u => u.Solicitudes)
            .HasForeignKey(s => s.UsuarioId)
            .OnDelete(DeleteBehavior.Restrict);

        solicitud
            .HasOne(s => s.Equipo)
            .WithMany(e => e.Solicitudes)
            .HasForeignKey(s => s.EquipoId)
            .OnDelete(DeleteBehavior.Restrict);

        solicitud
            .HasOne(s => s.Prestamo)
            .WithOne(p => p.Solicitud)
            .HasForeignKey<Solicitud>(s => s.PrestamoId)
            .OnDelete(DeleteBehavior.Restrict);

        solicitud
            .HasOne(s => s.RevisadoPor)
            .WithMany(u => u.SolicitudesRevisadas)
            .HasForeignKey(s => s.RevisadoPorId)
            .OnDelete(DeleteBehavior.Restrict);

        var movimiento = modelBuilder.Entity<Movimiento>();
        movimiento.ToTable("Movimientos");
        movimiento.HasKey(m => m.Id);
        movimiento.Property(m => m.Entidad).HasMaxLength(30).IsRequired();
        movimiento.Property(m => m.Accion).HasMaxLength(30).IsRequired();
        movimiento.Property(m => m.Detalle).HasMaxLength(300).IsRequired();
        movimiento.Property(m => m.UsuarioNombre).HasMaxLength(150);
        movimiento.HasIndex(m => m.Fecha);
        movimiento.HasIndex(m => new { m.Entidad, m.EntidadId });
    }
}
