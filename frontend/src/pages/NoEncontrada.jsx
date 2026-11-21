import { Link } from "react-router-dom";
import { IconoInicio, IconoLaptop } from "../components/ui/Iconos.jsx";

export default function NoEncontrada() {
  return (
    <div className="pagina pagina--centrada">
      <div className="no-encontrada">
        <p className="no-encontrada__codigo">404</p>
        <h1 className="no-encontrada__titulo">La página solicitada no existe</h1>
        <p className="no-encontrada__mensaje">
          La dirección no corresponde a ninguna ruta de TechAsset. Use el menú lateral o los siguientes accesos.
        </p>
        <div className="no-encontrada__acciones">
          <Link to="/panel" className="boton boton--primario">
            <IconoInicio tamano={18} />
            <span>Volver al panel</span>
          </Link>
          <Link to="/equipos" className="boton boton--secundario">
            <IconoLaptop tamano={18} />
            <span>Ver inventario</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
