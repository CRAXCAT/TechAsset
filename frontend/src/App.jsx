import { BrowserRouter } from "react-router-dom";
import { ProveedorNotificaciones } from "./context/ToastContext.jsx";
import { ProveedorAuth } from "./context/AuthContext.jsx";
import AppRoutes from "./routes/AppRoutes.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <ProveedorAuth>
        <ProveedorNotificaciones>
          <AppRoutes />
        </ProveedorNotificaciones>
      </ProveedorAuth>
    </BrowserRouter>
  );
}
