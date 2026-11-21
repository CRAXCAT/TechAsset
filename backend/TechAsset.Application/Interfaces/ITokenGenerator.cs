using TechAsset.Domain.Entities;

namespace TechAsset.Application.Interfaces;

/// <summary>
/// Abstracción de generación de tokens. Application no conoce JWT: solo pide
/// un token para el usuario autenticado.
/// </summary>
public interface ITokenGenerator
{
    (string Token, DateTime ExpiraUtc) Generar(Usuario usuario);
}
