using BCrypt.Net;
using TechAsset.Application.Interfaces;

namespace TechAsset.Infrastructure.Security;

/// <summary>
/// Implementación del hash con BCrypt: genera una sal aleatoria y aplica un
/// factor de coste, por lo que dos usuarios con la misma clave obtienen hashes
/// distintos y la clave original no puede recuperarse.
/// </summary>
public class PasswordHasher : IPasswordHasher
{
    public string Hashear(string clave) => BCrypt.Net.BCrypt.HashPassword(clave, workFactor: 11);

    public bool Verificar(string clave, string hash)
    {
        if (string.IsNullOrWhiteSpace(hash))
        {
            return false;
        }

        try
        {
            return BCrypt.Net.BCrypt.Verify(clave, hash);
        }
        catch (SaltParseException)
        {
            return false;
        }
    }
}
