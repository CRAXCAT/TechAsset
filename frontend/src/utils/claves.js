export function esClaveSegura(clave) {
  return (
    typeof clave === "string" &&
    clave.length >= 8 &&
    /[A-Z]/.test(clave) &&
    /[a-z]/.test(clave) &&
    /\d/.test(clave) &&
    /[^A-Za-z0-9]/.test(clave)
  );
}
