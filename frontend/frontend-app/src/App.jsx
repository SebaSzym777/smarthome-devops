import { useState } from "react";
import API_URL from "./config";

function App() {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("haslo123");
  const [token, setToken] = useState(null);
  const [devices, setDevices] = useState([]);
  const [error, setError] = useState("");

  const login = async () => {
    try {
      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (res.ok) {
        setToken(data.access_token);
        setError("");
      } else {
        setError(data.detail || "Błąd logowania");
      }
    } catch (err) {
      setError("Błąd połączenia z backendem");
    }
  };

  const getDevices = async () => {
    try {
      const res = await fetch(`${API_URL}/devices`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();

      if (res.ok) {
        setDevices(data);
        setError("");
      } else {
        setError(data.detail || "Błąd pobierania danych");
      }
    } catch (err) {
      setError("Błąd połączenia z backendem");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h2>Panel logowania test 2</h2>

      <input
        type="text"
        placeholder="Użytkownik"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />{" "}
      <br />
      <input
        type="password"
        placeholder="Hasło"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />{" "}
      <br />
      <button onClick={login}>Zaloguj</button>

      {token && (
        <div>
          <p style={{ color: "green" }}>Zalogowano! Token JWT ustawiony.</p>
          <button onClick={getDevices}>Pobierz urządzenia</button>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {devices.map((dev) => (
          <li key={dev.id}>
            <b>{dev.name}</b> – {dev.location}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
