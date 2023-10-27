"use client";


import { Provider } from "react-redux";
import {useStore} from '@/contexts/store'
import {PersistGate} from 'redux-persist/integration/react'
import {persistStore} from 'redux-persist'
import {useEffect} from "react";


export function UserProvider({ children }: { children: React.ReactNode }) {
  const store = useStore()
  const persistor = persistStore(store)
  useEffect(() => {
     import("zenn-embed-elements"); // 数式をブラウザでレンダリングできるようにします
   }, []);
  return (
      <Provider store={store}>
        <PersistGate persistor={persistor}>
          {children}
        </PersistGate>
      </Provider>
  )
}
