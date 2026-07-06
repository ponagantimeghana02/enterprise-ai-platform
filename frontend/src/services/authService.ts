import api from "../api/axios";

export const authService = {

  login(data: any) {
    return api.post("/login", data);
  },

  logout() {
    return api.post("/logout");
  },

  refreshToken() {
    return api.post("/refresh-token");
  },

};