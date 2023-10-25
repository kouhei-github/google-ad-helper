"use client";

import {RootState, useStore} from '@/contexts/store'
import Link from 'next/link'
import {useSelector} from 'react-redux'
import {useEffect} from 'react'
import { useRouter } from 'next/navigation';

export function UserProfile() {
  const user = useSelector((state: RootState) => state.user)
  const store = useStore()
  const Router = useRouter()

  const signout = () => {
    store.dispatch({type: 'SIGNOUT'})
    Router.replace('/signin')
  }
  return (
      <>
        {user.user.id === 0 ?
            <>
              <Link href={"/signin"} className={"cursor-pointer flex items-center space-x-4"}>
                <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><path d="M217.9 105.9L340.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L217.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1L32 320c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM352 416l64 0c17.7 0 32-14.3 32-32l0-256c0-17.7-14.3-32-32-32l-64 0c-17.7 0-32-14.3-32-32s14.3-32 32-32l64 0c53 0 96 43 96 96l0 256c0 53-43 96-96 96l-64 0c-17.7 0-32-14.3-32-32s14.3-32 32-32z"/></svg>
                <span className={"font-[900] text-[12px] tracking-widest"}>ログイン</span>
              </Link>
              <Link href={"/signup"} className={"flex items-center space-x-4"}>
                <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><path d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z"/></svg>
                <span className={"font-[900] text-[12px] tracking-widest"}>新規登録</span>
              </Link>
            </> :
            <>
              <Link href={"/profile"} className={"flex items-center space-x-4"}>
                <span className={"font-[900] text-[12px] tracking-widest"}>{user.user.name}<small className={"ml-2"}>さん</small></span>
              </Link>
              <div className={"flex items-center space-x-4 cursor-pointer"} onClick={() => signout()}>
                <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><path d="M448 256c0-106-86-192-192-192S64 150 64 256s86 192 192 192 192-86 192-192z"/></svg>
                <span className={"font-[900] text-[12px] tracking-widest"}>ログアウト</span>
              </div>
            </>
        }
      </>
  );
}
