import { useState } from "react";
import axios from "axios";
import Router from "next/router";

export default function Register(){
  const [form, setForm] = useState({first_name:'', last_name:'', email:'', password:'', mobile:''});
  const [profile, setProfile] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    const fd = new FormData();
    Object.keys(form).forEach(k => fd.append(k, form[k]));
    if(profile) fd.append("profile_pic", profile);

    try{
      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE}/auth/register`, fd, {
        headers: {"Content-Type": "multipart/form-data"}
      });
      Router.push("/otp-verify?email="+encodeURIComponent(form.email));
    }catch(err){
      alert(err.response?.data?.message || err.message);
    }
  }

  return (
    <div className="container" style={{maxWidth:600}}>
      <h2>Register</h2>
      <form onSubmit={submit}>
        <input placeholder="First name" value={form.first_name} onChange={e=>setForm({...form, first_name:e.target.value})} required/>
        <input placeholder="Last name" value={form.last_name} onChange={e=>setForm({...form, last_name:e.target.value})} required/>
        <input placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} required/>
        <input placeholder="Mobile" value={form.mobile} onChange={e=>setForm({...form, mobile:e.target.value})}/>
        <input type="password" placeholder="Password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} required/>
        <input type="file" accept="image/*" onChange={e=>setProfile(e.target.files[0])}/>
        <button type="submit">Register</button>
      </form>
    </div>
  );
}
