import {useEffect, useState} from "react";
import axios from "axios";

export default function Dashboard(){
  const [users,setUsers] = useState([]);
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : "";

  useEffect(()=>{
    if(!token) return;
    axios.get(`${process.env.NEXT_PUBLIC_API_BASE}/admin/users`, {headers: {Authorization: `Bearer ${token}`}})
      .then(r=>setUsers(r.data.users))
      .catch(e=>{ console.error(e); alert("Error fetching users"); });
  },[])

  return (
    <div className="container">
      <h2>Admin Dashboard</h2>
      <table className="table">
        <thead><tr><th>id</th><th>email</th><th>first</th><th>last</th><th>role</th><th>active</th></tr></thead>
        <tbody>
          {users.map(u=>(
            <tr key={u.id}>
              <td>{u.id}</td><td>{u.email}</td><td>{u.first_name}</td><td>{u.last_name}</td><td>{u.role}</td><td>{u.is_active? "Yes":"No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
