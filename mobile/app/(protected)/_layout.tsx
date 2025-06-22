import { HeaderShownContext } from "@react-navigation/elements";
import { Redirect, Stack } from "expo-router";
import { useContext } from 'react';
import { AuthContext } from "../utils/authContext";

export default function ProtectedLayout() {
  const authState = useContext(AuthContext)

  if (!authState.isReady) {
    return null;
  }

  if (!authState.isLoggedIn) {
    return <Redirect href={'/login'} />
  }
  return <Stack screenOptions={{headerShown: false}} />;
}
