import {useState} from 'react';
import axios from 'axios';

export default function Forgot(){
  const [email, setEmail] = useState('');
  const submit = async (e)=>{
    e.preventDefault();
    try{
      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE}/auth/forgot-password`, {email});
      alert('If account exists, a reset link will be sent to your email');
    }catch(err){
      alert(err.response?.data?.message || err.message);
    }
  }
  return (
    <div className="container" style={{maxWidth:600}}>
      <h2>Forgot Password</h2>
      <form onSubmit={submit}>
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Your email" required/>
        <button>Send Reset Link</button>
      </form>
    </div>
  )
}
