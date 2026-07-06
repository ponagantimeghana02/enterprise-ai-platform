import { useDispatch, useSelector } from "react-redux";

import type {
  RootState,
  AppDispatch,
} from "../store";

export const useAppDispatch =
  () => useDispatch<AppDispatch>();

export const useAppSelector = useSelector;

export function useAuth() {
  const auth = useSelector(
    (state: RootState) => state.auth
  );

  return auth;
}