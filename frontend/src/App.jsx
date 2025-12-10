import { useEffect, useState } from "react";
import { fetchRfps, createRfp } from "./services/rfpApi";

function App() {
  const [rfps, setRfps] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const data = await fetchRfps();
      setRfps(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleAddMock = async () => {
    await createRfp({
      title: "Sample RFP " + (rfps.length + 1),
      portal: "MockPortal",
      due_date: new Date().toISOString().slice(0, 10),
      status: "NEW",
    });
    await load();
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>RFP Dashboard</h1>
      <button onClick={handleAddMock}>Add Mock RFP</button>
      {loading ? (
        <p>Loading…</p>
      ) : (
        <table border="1" cellPadding="8" style={{ marginTop: "1rem" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Portal</th>
              <th>Due date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {rfps.map((r) => (
              <tr key={r.id}>
                <td>{r.id}</td>
                <td>{r.title}</td>
                <td>{r.portal}</td>
                <td>{r.due_date}</td>
                <td>{r.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
