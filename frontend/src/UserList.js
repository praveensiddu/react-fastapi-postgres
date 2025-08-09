import React, { useEffect, useState } from "react";

export default function UsersList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Form state
  const [form, setForm] = useState({ username: "", email: "", full_name: "" });
  const [editingId, setEditingId] = useState(null);

  // Fetch all users
  const fetchUsers = () => {
    fetch("/users/")
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => console.error("Error fetching:", err));
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  // Form submit handler
  const handleSubmit = (e) => {
    e.preventDefault();
    const method = editingId ? "PUT" : "POST";
    const url = editingId ? `/users/${editingId}` : "/users/";

    fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    })
      .then((res) => res.json())
      .then(() => {
        setForm({ username: "", email: "", full_name: "" });
        setEditingId(null);
        fetchUsers();
      });
  };

  // Delete handler
  const handleDelete = (id) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;
    fetch(`/users/${id}`, { method: "DELETE" })
      .then(() => fetchUsers());
  };

  // Edit load
  const handleEdit = (user) => {
    setForm({
      username: user.username,
      email: user.email,
      full_name: user.full_name,
    });
    setEditingId(user.id);
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2>{editingId ? "Edit User" : "Add User"}</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Username"
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Full name"
          value={form.full_name}
          onChange={(e) => setForm({ ...form, full_name: e.target.value })}
          required
        />
        <button type="submit">{editingId ? "Update" : "Create"}</button>
        {editingId && (
          <button type="button" onClick={() => { setEditingId(null); setForm({ username: "", email: "", full_name: "" }); }}>
            Cancel
          </button>
        )}
      </form>

      <h2>User List</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>ID</th>
            <th>UserName</th>
            <th>Email</th>
            <th>Full Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.length > 0 ? (
            users.map((u) => (
              <tr key={u.id}>
                <td>{u.id}</td>
                <td>{u.username}</td>
                <td>{u.email}</td>
                <td>{u.full_name}</td>
                <td>
                  <button onClick={() => handleEdit(u)}>Edit</button>
                  <button onClick={() => handleDelete(u.id)}>Delete</button>
                </td>
              </tr>
            ))
          ) : (
            <tr><td colSpan="5">No users found</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
