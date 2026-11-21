namespace TechAsset.Application.Exceptions;

/// <summary>
/// Se produce cuando el rol autenticado no tiene permiso para la operación.
/// El middleware la traduce a HTTP 403.
/// </summary>
public class AccesoDenegadoException : Exception
{
    public AccesoDenegadoException(string mensaje)
        : base(mensaje)
    {
    }
}
