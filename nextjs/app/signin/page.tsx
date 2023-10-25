"use client"
import { useDispatch, useSelector,  } from 'react-redux'
import { useRouter } from "next/navigation";
import {FC, FormEvent, useEffect, useState} from "react";
import { userSlice } from '@/contexts/userStore';
const apiUrl = "http://localhost:8000/api/auth";

type Response = {
    access_token: string
    refresh_token: string
    token_type: string
}

const SignInComponent: FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [message, setMessage] = useState("");
  const dispatch = useDispatch()
  const router = useRouter();
  
  useEffect(() => {
    const handleReset = () => {
      dispatch(userSlice.actions.reset())
    }
    handleReset()
  }, [])
  
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const headers = {
      'Content-Type': 'application/json',
    };
    const res = await fetch(
        `${apiUrl}/login`,
        { method: "POST", headers: headers, body: JSON.stringify({email, password})}
    )

    if(res.status !== 201) {
      setMessage("Credentials are incorrect.");
      throw new Error('Credentials are incorrect.');
    } 

    const data: Response = await res.json()
    const randomIdNumber = Math.floor(Math.random() * 100000000) 
    // TODO: save token in localStorage
    dispatch(
      userSlice.actions.updateUser({
        name: 'ラミン',
        age: 36,
        email: email,
        token: data.access_token,
        id: randomIdNumber,
        history: [],
      })
    )
    // TODO: redirect to homepage
    router.replace("/");
  };

  return (
    <div className="flex flex-col justify-center items-center">
      <h1 className="text-3xl font-bold mb-4">Sign In</h1>
      <form onSubmit={handleSubmit}>
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
        <div className="flex items-center mb-4">
          <input
            type="checkbox"
            name="rememberMe"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
            className="mr-2"
          />
          <label className="mr-8">Remember Me</label>
          <a href="/forgot-password" className="ml-4　">Forgot Password?</a>
        </div>
        <div className="my-3">
      </div>
        <button
          type="submit"
          className="bg-blue-400 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded-md"
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSubmit(e);
            }
          }}
        >
          Sign In
        </button>
      </form>
      {message && (
        <div className="my-3 text-red-500">{message}</div>
      )
      }
    </div>
  );
};

export default SignInComponent;
