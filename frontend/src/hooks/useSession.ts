import { useEffect } from "react";

import { tokenStorage } from "../utils/token";

import { useAppDispatch } from "./useAuth";

import { setSessionExpired } from "../store/authSlice";

export default function useSession() {
  const dispatch = useAppDispatch();

  useEffect(() => {
    const timer = setInterval(() => {
      const token =
        tokenStorage.getAccessToken();

      if (!token) {
        dispatch(setSessionExpired());
      }
    }, 30000);

    return () => clearInterval(timer);
  }, []);
}