using System.Net;
using System.Text.Json;
using TechAsset.Application.Exceptions;

namespace TechAsset.API.Middleware;

/// <summary>
/// Convierte las excepciones de la aplicación en respuestas JSON uniformes.
/// Así el frontend recibe siempre el campo "mensaje", sin importar el módulo.
/// </summary>
public class ManejadorErroresMiddleware
{
    private readonly RequestDelegate siguiente;
    private readonly ILogger<ManejadorErroresMiddleware> logger;

    public ManejadorErroresMiddleware(RequestDelegate siguiente, ILogger<ManejadorErroresMiddleware> logger)
    {
        this.siguiente = siguiente;
        this.logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await siguiente(context);
        }
        catch (CredencialesInvalidasException ex)
        {
            await EscribirRespuestaAsync(context, HttpStatusCode.Unauthorized, ex.Message);
        }
        catch (AccesoDenegadoException ex)
        {
            await EscribirRespuestaAsync(context, HttpStatusCode.Forbidden, ex.Message);
        }
        catch (ReglaNegocioException ex)
        {
            await EscribirRespuestaAsync(context, HttpStatusCode.Conflict, ex.Message);
        }
        catch (RecursoNoEncontradoException ex)
        {
            await EscribirRespuestaAsync(context, HttpStatusCode.NotFound, ex.Message);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Error no controlado al procesar {Metodo} {Ruta}", context.Request.Method, context.Request.Path);
            await EscribirRespuestaAsync(
                context,
                HttpStatusCode.InternalServerError,
                "Ocurrió un error inesperado al procesar la solicitud. Intente nuevamente en unos segundos.");
        }
    }

    private static async Task EscribirRespuestaAsync(HttpContext context, HttpStatusCode codigo, string mensaje)
    {
        if (context.Response.HasStarted)
        {
            return;
        }

        context.Response.Clear();
        context.Response.StatusCode = (int)codigo;
        context.Response.ContentType = "application/json";

        var cuerpo = JsonSerializer.Serialize(new { mensaje, codigo = (int)codigo });
        await context.Response.WriteAsync(cuerpo);
    }
}
