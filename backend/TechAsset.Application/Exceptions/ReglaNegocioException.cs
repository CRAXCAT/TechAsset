namespace TechAsset.Application.Exceptions;

/// <summary>
/// Se produce cuando una entrada es válida en formato pero infringe una regla del negocio.
/// El middleware la traduce a HTTP 409 con un mensaje comprensible para el usuario.
/// </summary>
public class ReglaNegocioException : Exception
{
    public ReglaNegocioException(string mensaje)
        : base(mensaje)
    {
    }
}
