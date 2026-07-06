import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { authService } from "../services/authService";
import { tokenStorage } from "../utils/token";
import { AuthState, LoginRequest } from "../types/auth";

const initialState: AuthState = {
  user: null,
  accessToken: tokenStorage.getAccessToken(),
  refreshToken: tokenStorage.getRefreshToken(),
  authenticated: !!tokenStorage.getAccessToken(),
  loading: false,
  error: null,
};

export const loginUser = createAsyncThunk(
  "auth/login",
  async (data: LoginRequest, thunkAPI) => {
    try {
      const response = await authService.login(data);
      return response.data;
    } catch (err: any) {
      return thunkAPI.rejectWithValue(
        err.response?.data?.message || "Login Failed"
      );
    }
  }
);

export const logoutUser = createAsyncThunk(
  "auth/logout",
  async () => {
    await authService.logout();
  }
);

const authSlice = createSlice({
  name: "auth",

  initialState,

  reducers: {
    clearError(state) {
      state.error = null;
    },

    setSessionExpired(state) {
      state.authenticated = false;
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;

      tokenStorage.clearTokens();
    },
  },

  extraReducers(builder) {
    builder

      .addCase(loginUser.pending, (state) => {
        state.loading = true;
      })

      .addCase(loginUser.fulfilled, (state, action) => {
        state.loading = false;

        state.user = action.payload.user;

        state.accessToken = action.payload.accessToken;

        state.refreshToken = action.payload.refreshToken;

        state.authenticated = true;

        tokenStorage.setTokens(
          action.payload.accessToken,
          action.payload.refreshToken
        );
      })

      .addCase(loginUser.rejected, (state, action: any) => {
        state.loading = false;

        state.error = action.payload;
      })

      .addCase(logoutUser.fulfilled, (state) => {
        tokenStorage.clearTokens();

        state.user = null;

        state.accessToken = null;

        state.refreshToken = null;

        state.authenticated = false;
      });
  },
});

export const { clearError, setSessionExpired } =
  authSlice.actions;

export default authSlice.reducer;