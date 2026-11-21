using TechAsset.Application.Interfaces;
using TechAsset.Infrastructure.Data;

namespace TechAsset.Infrastructure.Data;

public class UnitOfWork : IUnitOfWork
{
    private readonly AppDbContext context;

    public UnitOfWork(AppDbContext context)
    {
        this.context = context;
    }

    public async Task<T> EjecutarAsync<T>(Func<Task<T>> operacion)
    {
        await using var transaccion = await context.Database.BeginTransactionAsync();

        try
        {
            var resultado = await operacion();
            await transaccion.CommitAsync();
            return resultado;
        }
        catch
        {
            await transaccion.RollbackAsync();
            throw;
        }
    }
}
