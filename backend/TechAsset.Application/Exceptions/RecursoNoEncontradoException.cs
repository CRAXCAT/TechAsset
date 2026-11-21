namespace TechAsset.Application.Exceptions;

/// <summary>
/// Se produce cuando el recurso solicitado no existe. El middleware la traduce a HTTP 404.
/// </summary>
public class RecursoNoEncontradoException : Exception
{
    public RecursoNoEncontradoException(string mensaje)
        : base(mensaje)
    {
    }
}
