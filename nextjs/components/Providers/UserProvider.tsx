"use client";


import { Provider } from "react-redux";
import {useStore} from '@/contexts/store'
import {PersistGate} from 'redux-persist/integration/react'
import {persistStore} from 'redux-persist'

export function UserProvider({ children }: { children: React.ReactNode }) {
  const store = useStore()
  const persistor = persistStore(store)
  return (
      <Provider store={store}>
        <PersistGate persistor={persistor}>
          {children}
        </PersistGate>
      </Provider>
  )
}
