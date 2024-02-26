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
    // <div className={"w-full bg-white p-3 flex items-center justify-between"}>
    //   <div className={"w-full flex items-center"}>
    //     <Link href={"/"} className={"w-max"}>
    //       <img src={"https://dev-to-uploads.s3.amazonaws.com/uploads/logos/resized_logo_UQww2soKuUsjaOGNB38o.png"}
    //            alt={"dev"} className={"w-11 h-8"}/>
    //     </Link>
    //     <div className={"relative ml-5 md:w-2/3 w-full mx-auto"}>
    //       <input type="text" placeholder={"Search..."} className={"border border-[#333333] text-[#333333] w-full px-2 py-1 text-left"}/>
    //       <button className={"absolute top-1/2 right-0 transform -translate-y-1/2 w-max px-2 h-full group hover:bg-purple-200"}>
    //         <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"
    //              className="group-hover:fill-purple-500" focusable="false"
    //         >
    //           <path
    //             d="m18.031 16.617 4.283 4.282-1.415 1.415-4.282-4.283A8.96 8.96 0 0 1 11 20c-4.968 0-9-4.032-9-9s4.032-9 9-9 9 4.032 9 9a8.96 8.96 0 0 1-1.969 5.617zm-2.006-.742A6.977 6.977 0 0 0 18 11c0-3.868-3.133-7-7-7-3.868 0-7 3.132-7 7 0 3.867 3.132 7 7 7a6.977 6.977 0 0 0 4.875-1.975l.15-.15z"></path>
    //         </svg>
    //       </button>
    //     </div>
    //   </div>
    //
    //   <div className={"flex items-center justify-end w-1/3 md:w-full md:space-x-5 space-x-3"}>
    //     <Link href={"#"} className={"rounded-lg text-[#5A66E4] border border-[#5A66E4] md:px-3 md:py-2 md:block hidden"}>
    //       投稿する
    //     </Link>
    //     <div className={"cursor-pointer relative"}>
    //       <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" role="img"
    //            aria-labelledby="adk6gw2638o5dl0puuxzy1ykufo6t5wf" className="md:w-7 w-5 h-5 md:h-full"><title
    //         id="adk6gw2638o5dl0puuxzy1ykufo6t5wf">Notifications</title>
    //         <path d="M20 17h2v2H2v-2h2v-7a8 8 0 1116 0v7zm-2 0v-7a6 6 0 10-12 0v7h12zm-9 4h6v2H9v-2z"></path>
    //       </svg>
    //       <p className={"absolute md:-top-2 -top-3 rounded right-0 md:w-[0.8rem] w-3 h-5 md:h-5 bg-red-600 text-white flex items-center justify-center"}>7</p>
    //     </div>
    //     <button>
    //       <img src={"https://dev-to-uploads.s3.amazonaws.com/uploads/logos/resized_logo_UQww2soKuUsjaOGNB38o.png"}
    //            alt={"dev"} className={"w-9 h-9 rounded-full object-cover border border-black"}/>
    //     </button>
    //   </div>
    // </div>
  )
}
