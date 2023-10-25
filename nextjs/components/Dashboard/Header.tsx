"use client"
import Image from 'next/image'
import Link from 'next/link'
import {UserProfile} from '@/components/UserProfile'


export default function Header() {

  return (
      <header className={"header"}>
        <div className={"max-w-[914px] mx-auto flex items-center justify-between h-[50px] "}>
          <Link href={"/"}>
            <Image src={"/images/logo.webp"} alt={"ロゴ"} width={"150"} height={35} />
          </Link>
          <div className={"flex items-center justify-center space-x-5"}>
            <div id={"login"} className={"flex items-center justify-center space-x-5"}>
              <UserProfile />
            </div>

            <Link href={"/signIn"}>
              <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><path d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z"/></svg>
            </Link>
          </div>
        </div>
      </header>
  )
}
