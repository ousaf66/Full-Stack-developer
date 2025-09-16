import {useState} from "react";
import axios from "axios";
import {useRouter} from "next/router";

export default function OTPVerify(){
  const router = useRouter();
  const email = router.query.email || "";
  const [otp, setOtp] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try{
      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE}/auth/verify-otp`, {email, otp});
      alert("Verified! You can now login.");
      router.push("/login");
    }catch(err){
      alert(err.response?.data?.message || err.message);
    }
  }

  return (
    <div className="container" style={{maxWidth:600}}>
      <h2>Verify OTP</h2>
      <p>OTP sent to <b>{email}</b></p>
      <form onSubmit={submit}>
        <input value={otp} onChange={e=>setOtp(e.target.value)} placeholder="Enter OTP" required/>
        <button>Verify</button>
      </form>
    </div>
  );
}
