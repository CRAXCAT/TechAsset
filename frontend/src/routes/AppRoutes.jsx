import { Navigate, Route, Routes } from "react-router-dom";
import RutaPorRol from "../components/RutaPorRol.jsx";
import RutaPrivada from "../components/RutaPrivada.jsx";
import AppLayout from "../layouts/AppLayout.jsx";
import CambiarClave from "../pages/CambiarClave.jsx";
import Dashboard from "../pages/Dashboard.jsx";
import Equipos from "../pages/Equipos.jsx";
import Inicio from "../pages/Inicio.jsx";
import Login from "../pages/Login.jsx";
import Movimientos from "../pages/Movimientos.jsx";
import NoEncontrada from "../pages/NoEncontrada.jsx";
import NuevaSolicitud from "../pages/NuevaSolicitud.jsx";
import NuevoPrestamo from "../pages/NuevoPrestamo.jsx";
import Prestamos from "../pages/Prestamos.jsx";
import Reportes from "../pages/Reportes.jsx";
import Solicitudes from "../pages/Solicitudes.jsx";
import Usuarios from "../pages/Usuarios.jsx";

const GESTION = ["Administrador", "Responsable"];

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Inicio />} />
      <Route path="login" element={<Login />} />

      <Route
        path="cambiar-clave"
        element={
          <RutaPrivada>
            <CambiarClave />
          </RutaPrivada>
        }
      />

      <Route
        element={
          <RutaPrivada>
            <AppLayout />
          </RutaPrivada>
        }
      >
        <Route path="panel" element={<Dashboard />} />
        <Route
          path="usuarios"
          element={
            <RutaPorRol roles={GESTION}>
              <Usuarios />
            </RutaPorRol>
          }
        />
        <Route path="equipos" element={<Equipos />} />
        <Route path="solicitudes" element={<Solicitudes />} />
        <Route path="solicitudes/nueva" element={<NuevaSolicitud />} />
        <Route path="prestamos" element={<Prestamos />} />
        <Route
          path="prestamos/nuevo"
          element={
            <RutaPorRol roles={GESTION}>
              <NuevoPrestamo />
            </RutaPorRol>
          }
        />
        <Route
          path="reportes"
          element={
            <RutaPorRol roles={GESTION}>
              <Reportes />
            </RutaPorRol>
          }
        />
        <Route
          path="movimientos"
          element={
            <RutaPorRol roles={GESTION}>
              <Movimientos />
            </RutaPorRol>
          }
        />
        <Route path="inicio" element={<Navigate to="/panel" replace />} />
        <Route path="*" element={<NoEncontrada />} />
      </Route>
    </Routes>
  );
}
