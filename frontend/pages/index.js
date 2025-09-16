export default function Home(){
  return (
    <div className="container">
      <h1>Galvan AI — Auth Demo</h1>
      <p>Use the links to register, login, and (if Super Admin) manage users.</p>
      <div><a href="/register">Register</a> | <a href="/login">Login</a></div>
    </div>
  )
}
