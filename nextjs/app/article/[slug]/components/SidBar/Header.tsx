"use client"
import Link from "next/link";

export const Header = () => {
  return (
    <div className={"w-full bg-white p-3 flex items-center justify-between"}>
      <div className={"w-full flex items-center"}>
        <Link href={"/"} className={"w-max"}>
          <p className={"md:w-26 w-28 object-cover font-extrabold bg-black text-white h-8 flex items-center justify-center px-1"}>Geek Snipe</p>
        </Link>
        <div className={"relative ml-5 md:w-1/2 w-full mx-auto"}>
          <input type="text" placeholder={"Search..."}
                 className={"border border-[#333333] text-[#333333] w-full px-2 py-1 text-left"}/>
          <button
            className={"absolute top-1/2 right-0 transform -translate-y-1/2 w-max px-2 h-full group hover:bg-purple-200"}>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"
                 className="group-hover:fill-purple-500" focusable="false"
            >
              <path
                d="m18.031 16.617 4.283 4.282-1.415 1.415-4.282-4.283A8.96 8.96 0 0 1 11 20c-4.968 0-9-4.032-9-9s4.032-9 9-9 9 4.032 9 9a8.96 8.96 0 0 1-1.969 5.617zm-2.006-.742A6.977 6.977 0 0 0 18 11c0-3.868-3.133-7-7-7-3.868 0-7 3.132-7 7 0 3.867 3.132 7 7 7a6.977 6.977 0 0 0 4.875-1.975l.15-.15z"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}
