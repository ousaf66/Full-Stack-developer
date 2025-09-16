import {useState} from 'react';
import axios from 'axios';
import {useRouter} from 'next/router';

export default function Reset(){
  const router = useRouter();
  const { token } = router.query;
  const [password, setPassword] = useState('');

  const submit = async (e)=>{
    e.preventDefault();
    try{
      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE}/auth/reset-password`, {token, password});
      alert('Password reset successful. You can login now.');
      router.push('/login');
    }catch(err){
      alert(err.response?.data?.message || err.message);
    }
  }

  return (
    <div className="container" style={{maxWidth:600}}>
      <h2>Reset Password</h2>
      <form onSubmit={submit}>
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="New password" required/>
        <button>Reset Password</button>
      </form>
    </div>
  )
}
