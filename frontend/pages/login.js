import axios from "axios";
import {useState} from "react";
import Router from "next/router";

export default function Login(){
  const [form, setForm] = useState({email:"", password:""});

  const submit = async (e) => {
    e.preventDefault();
    try{
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE}/auth/login`, form);
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);
      localStorage.setItem("user", JSON.stringify(res.data.user));
      if(res.data.user.role === "superadmin") Router.push("/admin/dashboard");
      else Router.push("/");
    }catch(err){
      alert(err.response?.data?.message || err.message);
    }
  }

  return (
    <div className="container" style={{maxWidth:600}}>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <input placeholder="Email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} required/>
        <input type="password" placeholder="Password" value={form.password} onChange={e=>setForm({...form,password:e.target.value})} required/>
        <button>Login</button>
      </form>
      <a href="/forgot-password">Forgot password?</a>
    </div>
  );
}
