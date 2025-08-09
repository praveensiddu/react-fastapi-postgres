import React from "react";
import UsersList from "./UsersList";

export default function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>FastAPI + React CRUD</h1>
      <UsersList />
    </div>
  );
}
