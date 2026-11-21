namespace TechAsset.Application.Exceptions;

/// <summary>
/// Credenciales inválidas o cuenta inactiva. El middleware responde 401 con un
/// mensaje genérico para no revelar si el correo existe.
/// </summary>
public class CredencialesInvalidasException : Exception
{
    public CredencialesInvalidasException(string mensaje = "Correo o contraseña incorrectos.")
        : base(mensaje)
    {
    }
}
