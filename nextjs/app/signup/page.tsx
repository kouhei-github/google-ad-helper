"use client"
import { useRouter } from "next/navigation";
import React from "react";
const apiUrl = "http://localhost:8000/api/auth";

const SignUpComponent: React.FC = () => {
  const [name, setName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [message, setMessage] = React.useState("");
  const router = useRouter();
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(name, email, password);
    
    fetch(`${apiUrl}/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        email,
        password,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {          
          setMessage(data.error);
        }
        else {
          router.push("/signin");
        }
      })
      
  };

  return (
    <div className="flex flex-col justify-center items-center">
      <h1 className="text-3xl font-bold mb-4">Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Name"
          className="mb-4 border border-gray-300 rounded-md p-2 w-full"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          className="mb-4 border border-gray-300 rounded-md p-2 w-full"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          className="mb-4 border border-gray-300 rounded-md p-2 w-full"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md"
        >
          Sign Up
        </button>
      </form>
      {message && (
        <div className="my-3 text-red-500">{message}</div>
      )}
    </div>
  );
};

export default SignUpComponent;
